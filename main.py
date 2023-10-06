import requests
import csv
import json
from bs4 import BeautifulSoup 

#página com o índice de estrelas
starsPage = requests.get('https://en.wikipedia.org/wiki/List_of_proper_names_of_stars')

#BeautifulSoup com a página
stars = BeautifulSoup(starsPage.content, 'html.parser')


#entries recebe linhas da tabela
entries = stars.select(".wikitable > tbody > tr")
i = 0

#remove o cabeçalho
entries = entries[1:]

#inicializa lista de estrelas, e lista de campos
stars_list = list()
fields_list = list()

#adiciona inicialmente os campos de nome e designação
fields_list.append("Modern name")
fields_list.append("Designation")

#itera pelas entradas
for entry in entries:

    i+=1
    
    #separa as colunas das linhas em constelação, designação e nome
    star = entry.select("td")
    constelation = star[0]
    designation = star[1]
    modern_name = star[2]

    print("Modern name: "+modern_name.get_text())
    print("Designation: "+designation.get_text())
    star_data = dict()
    star_data["Modern name"] = modern_name.get_text()
    star_data["Designation"] = designation.get_text()
    

    address = None
    
    # tenta encontrar a página da estrela na coluna de nome, 
    a = modern_name.find('a')
    if(a is not None and (not (a.has_attr('class') and "new" in a.attrs.get('class')))):

      address = a.attrs.get('href')
    else:
      a = designation.find('a')
      if(a is not None and (not (a.has_attr('class') and "new" in a.attrs.get('class')))):
        address = a.attrs.get('href')
      else:
         print("Não tem")
         

    #se há uma pagina para a estrela e há uma infobox na página
    # extrai as informações da info box
    if(address is not None):
      print("Address: "+ address)
      address = "https://en.wikipedia.org" + address
      star_page = BeautifulSoup(requests.get(address).content, 'html.parser')
      # procura por informações nas infoboxes
      infobox_list = star_page.select(".infobox")
      for infobox in infobox_list:
        try:
          if(infobox is not None):
          
            # procura pelas linhas da infobox 
            # filtrar por cabeçalhos específicos, que identificam uma informação de interesse
            infobox_entries = infobox.select("tr")
            for infobox_entry in infobox_entries:

              header = infobox_entry.select("th:first-child, td:first-child")
              if(header):
                data = infobox_entry.select("td:nth-child(2)")
                if(data):
                  header_text = header[0].text.strip()
                  data_text = data[0].get_text().strip()
                  print(header_text+": "+data_text+"\n")
                  star_data[header_text] = data_text
                  if(not (header_text in fields_list)):
                    fields_list.append(header_text)

                  #print(header[0].text)


        except:
          pass
      
      stars_list.append(star_data)

with open('Stars.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = fields_list)
    writer.writeheader()
    writer.writerows(stars_list)

      


      
      
    

   



