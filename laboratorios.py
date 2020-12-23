import requests,json,csv
from bs4 import BeautifulSoup

pagina_inicial=requests.get("http://www.pr2.ufrj.br/laboratorios")

soup_inicial=BeautifulSoup(pagina_inicial.text,"html.parser")

lista=[]

for centro in soup_inicial.find(class_="text-justify").findAll("a")[1:]:
    pagina=requests.get(centro.get("href"))
    soup=BeautifulSoup(pagina.text,"html.parser")
    for lab in soup.find(id="accordion").findAll(class_="panel-default"):
        lab_info={}
        lab_info["Nome"]=lab.strong.get_text()
        for detalhes in lab.findAll("td"):
            lab_info[detalhes.strong.get_text()[:-1]]=detalhes.small.get_text()
        lab_info["Centro"]=centro.get_text()
        lista+=[lab_info]

with open("laboratorios.json","w",encoding="utf-8") as arq_json:
    json.dump(lista,arq_json,ensure_ascii=False)

with open("laboratorios.csv","w",encoding="utf-8",newline='') as arq_csv:
    dw=csv.DictWriter(arq_csv, lista[0].keys())
    dw.writeheader()
    dw.writerows(lista)
