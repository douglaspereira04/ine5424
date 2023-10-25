import requests
import csv
import json
import re
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
#	cada entrada da lista stars_list é um dicionário, correspondente as informações de uma estrela. 
#	cada entrada de um dicionário corresponde à um campo da infobox.
#	fields_list é um lista que contém o conjunto de chaves distintas em todos os dicionários.
stars_list = list()
fields_list = list()

#adiciona inicialmente os campos de nome, designação e endereço
fields_list.append("Modern name")
fields_list.append("Designation")
fields_list.append("Address")

#adiciona o restante dos campos
#fields_list.append("Constellation")
#fields_list.append("Right ascension")
#fields_list.append("Declination")
#fields_list.append("Apparent magnitude (V)")
#fields_list.append("Spectral type")
#fields_list.append("Proper motion (μ)")
#fields_list.append("Parallax (π)")
#fields_list.append("Distance")
#fields_list.append("Absolute magnitude (MV)")
#fields_list.append("Mass")
#fields_list.append("Radius")
#fields_list.append("Temperature")

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
    # star_data é o dicionário correspondente à estrela atual, e depois da coleta dos dados será inserido em stars_list
    star_data = dict()
    star_data["Modern name"] = modern_name.get_text()
    star_data["Designation"] = designation.get_text()
    

    address = None
    
    # tenta encontrar a página da estrela na coluna de "Modern name", 
    a = modern_name.find('a')
    if(a is not None and (not (a.has_attr('class') and "new" in a.attrs.get('class')))):

      address = a.attrs.get('href')
    else:
      # tenta encontrar a página da estrela na coluna de "Designation", 
      a = designation.find('a')
      if(a is not None and (not (a.has_attr('class') and "new" in a.attrs.get('class')))):
        address = a.attrs.get('href')
      else:
         # não há página para essa estrela", 
         print("No data")
         

    # se foi encontrado o endereço
    if(address is not None):
      print("Address: "+ address)
      address = "https://en.wikipedia.org" + address
      star_page = BeautifulSoup(requests.get(address).content, 'html.parser')
      star_data["Address"] = address
      # carrega a página e procura por infoboxes
      infobox_list = star_page.select(".infobox")
      for infobox in infobox_list:
        # pra cada infobox carregada
        try:
          if(infobox is not None):
          
            # procura pelas linhas da infobox, tentando extrair qualquer informações de
            # entradas que estão na forma <th>header</th><td>data</td> ou <td>header</td><td>data</td>
            infobox_entries = infobox.select("tr")
            for infobox_entry in infobox_entries:

              header = infobox_entry.select("th:first-child, td:first-child")
              if(header):
                header_text = re.sub('\s+', ' ', header[0].get_text().strip()).strip()
                if(header_text):
                  data = infobox_entry.select("td:nth-child(2)")
                  if(data):
                    data_text = re.sub('\s+', ' ', data[0].get_text().strip())
                    data_text = re.sub("\[.*?\]","",data_text).strip()
                    print(header_text+": "+data_text+"\n")
                    # diciona o dado em star_data, se nao for vazio
                    if(data_text):
                      # se o header nao está na lista de campos, adiciona-o
                      if(header_text not in fields_list):
                        fields_list.append(header_text)
                      star_data[header_text] = data_text

        except:
          pass
      # salva as informações coletadas em stars_list
      stars_list.append(star_data)

#escreve toda stars_list no arquivo csv
with open('Stars.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = fields_list)
    writer.writeheader()
    writer.writerows(stars_list)

      


      
      
    

   



