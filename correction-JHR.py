#coding:utf-8

### MES COMMENTAIRES ET CORRECTIONS SONT MARQUÉS PAR TROIS DIÈSES

#on importe les modules nécessaires pour faire le travail, dont le beautiful soup

import csv
import requests
from bs4 import BeautifulSoup

### Idée originale!
### Je soupçonne que tu as déjà fait partie des Pionniers... :)

url="http://www.baseballoutaouais.com/index.php?page=stats&entity=category&action=display&catid=7"

# J'ai pris le site web de Baseball Québec Outaouais, aux résultats des parties 2016 de la catégorie Moustique A

#Je donne mon identité
entetes={
    "User-Agent":"Elizabeth Seguin",
    "From":"eliseguin@sympatico.ca"
}
#importation des derniers modules
contenu=requests.get(url, headers=entetes)

page=BeautifulSoup(contenu.text,"html.parser")

# print(page)

### [...] J'ai retiré ce qui semblaient être tes notes

# for i in page.find_all("td"):
    # if i.text.strip() == "Pionniers La Pêche":
        # print(i.find_next("a").text.strip())
        
#Création de listes (pour plus tard)
date=[]
visiteur=[]
local=[]
resultat=[]
score=[]

#Création d'autres boucles

#Ici, je veux avoir l'information principale, retrouvée dans le tableau du site web. Je pourrais travailler facilement avec ça, mais si je veux travailler avec des éléments en particulier
#Je vais devoir trouver comment traiter les éléments seuls. Mais pour l'instant, j'ai pas mal toutes les informations que je veux.
#Résultat : MA46Moustique ASection Pionniers La Pêche  0 - 6   Patriotes Gatineau Dim, 24 jul 14:30Sanscartier 3ABAG
#C'est tout collé, mais c'est tout là.
#MA46 = numéro de partie.....Moustique A = carégorie....0-6=score etc etc.

# for ligne in page.find_all("tr"):
#     ligne2=str(ligne.text)
#     # date.append(ligne2.strip())
#     print(ligne2)

#Si je veux trouver le nombre de caractères de chaque élément pour mieux les traiter, je peux:
    
# for ligne in page.find_all("tr"):
#     ligne2=str(ligne.text)
#     print(len(ligne2))
    
    #note à moi : les 3 ou 4 premiers caractères = numéro de partie
    
# si je veux trouver toutes les équipes perdantes, je peux faire ça : 
#MAIS! Puisqu'il y a un lien lié à chaque élément, qui est intégré au texte, c'est difficile à lire. 
# for visiteur in page.find_all("td"):
# 	print(page.find_all("td", class_="team-looser"))

# #Création de ma boucle ultime : traiter chaque élément.
# for ligne in page.find_all("td"):
#     # print(ligne.text)
#     info=ligne.text
#     resultat.append(info.strip())
# resultat2=resultat[7:]
#J'enlève les 7 premières lignes, car elles ne me sont pas utiles.

### En fait, ton premier essai (lignes 48-51) était le plus près du but.
### Voici le code que j'aurais fait:

for table in page.find_all("table", class_="stats-table")[1:]: ### Comme il y a deux éléments <table> de classe "stats-table", on peut procéder ainsi: «find_all» les prend les deux, et on prend le 2e ([1])
    for ligne in table.find_all("tr")[1:]: ### Ceci prend tous les <tr> qui s'y trouvent, sauf le premier
        ### On peut donc aller récupérer les items qui nous intéressent dans les <td> se trouvant dans chaque <tr>
        ### On peut commencer par créer une liste de tous les <td> de chaque <tr>
        items = ligne.find_all("td")

        ### On sait que la première équipe est le 5e item de la ligne
        equipe1 = items[4].text.strip()

        ### On sait que la 2e équipe est le 7e item
        equipe2 = items[6].text.strip()

        ### Le score est le 6e item
        score = items[5].text.strip()

        ### Etc...
        date = items[7].text.strip()
        heure = items[8].text.strip()
        lieu = items[9].text.strip()
        asso = items[10].text.strip()

        ### J'ai remarqué qu'il y a un lien dans la dernière colonne, à droite; je vais le chercher
        details = items[11].a["onclick"].split(",")
        lien = details[0][14:-1]
        hyperlien = "http://www.baseballoutaouais.com" + lien

        ### Je mets toutes mes infos dans une liste que j'appelle «partie», car il s'agit à chaque fois des infos relatives à une partie
        partie = [equipe1,equipe2,score,date,heure,lieu,asso,hyperlien]
        print(partie)

        ### Et je la mets dans un CSV

        marin = open("moustique-JHR.csv","a")
        gouin = csv.writer(marin)
        gouin.writerow(partie)

        ### VOILÀ!
        ### Tu pourrais appliquer cette recette pour ramasser toutes les infos de toutes les ligues
        ### Voire, recueillir encore plus d'infos en moissonnant les pages détaillées vers lesquelles mène l'hyperlien

# #J'enlève aussi ce qui ne m'est pas utile à traiter.
# for inutile in resultat2:
#     if inutile=="Section":
#         resultat2.remove(inutile)
# for inutile in resultat2:
#     if inutile=="Moustique A":
#         resultat2.remove(inutile)
# for inutile in resultat2:
#     if inutile=="":
#         resultat2.remove(inutile)
#         #bobo ici, il y a des vides, mais même avec ce code, je n'en retire que la moitié. J'ai donc la moitié de mes résultats qui écoutent ma commande...bizarre.
#         #Mais je peux quand même travailler avec. Ci-dessous, un autre essai. 
# for inutile in resultat2:
#     if inutile=="\n":
#         resultat2.remove(inutile)
# n=-1

#Note à moi, un match est au  9e élément.  

#Faire rouler ma boucle : Ici, je veux avoir seulement les dates des parties de l'année. Comme mentionné plus haut, cela ne fonctionne jusqu'à la moitié, mais ça reste traitable.
#le bobo vient des espaces que je n'ai pas pu enlever... mais c'est un peu complexe car dans le site, ces espaces sont des liens cliquables différents...
#bref, ici seulement les dates. 
#J'y suis allée avec le nombre d'éléments pour atteindre la "date", qui est 4, après avoir enlevé les trucs "inutiles"
# for index in range(len(resultat2)):
#     n=n+1
#     index=n*8+4
#     if index > 629:
#         break
#     #j'ai ajouté cela après que mon bash n'ait pas voulu traiter la réponse, car c'est comme si il roulait à l'infini. J'ai calculé le nombre de caractères
#     #maximum de mon tableau, puis j'ai fait en sorte que ma boucle arrête de chercher après l'avoir atteint.
#     #puis, j'ai trouvé mon résultat. 
#     date.append(resultat2[index])
# print(date)
    
#je répète la même chose pour trouver le nom des équipes visiteurs, par exemple    
# for index in range(len(resultat2)):
#     n=n+1
#     index=n*8+1
#     if index > 629:
#         break
#     # dates=resultat2[index]
#     visiteur.append(resultat2[index])
# print(visiteur)

# #Puis encore pour trouver les scores de la saison. 
# for index in range(len(resultat2)):
#     n=n+1
#     index=n*8+2
#     if index > 629:
#         break
#     # dates=resultat2[index]
#     score.append(resultat2[index])
# print(score)
# print(len(resultat2))
    
# print(resultat2[-1])

# YOUPI C'est fini!!

### GO LES PIONNIERS!
