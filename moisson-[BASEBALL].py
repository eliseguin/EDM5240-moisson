#coding:utf-8

#on importe les modules nécessaires pour faire le travail, dont le beautiful soup

import csv
import requests
from bs4 import BeautifulSoup

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

#puisque mon site est déjà en html, pas besoin de le transférer en éléments html

#Je fais un examen du code HTML de la page qui nous	intéresse.
# HTML = balise + attributs + valeurs + contenu (rappel)

#La base : chercher dans le html par balise avec la fonction .find()
#J'utilise l'élément <a>, si je veux trouver, par exemple, le titre du site (Baseball Québec Outaouais) 

# print(page.find("a"))

#à noter que j'aurais pu aussi écrire print(page.a), et ça aurait donné la même chose.

# print(page.a)

#si je veux trouver tous les éléments qui se trouvent dans les balises "a", je peux ajouter "_all" à find

# print(page.find_all("a"))

#Dans le code htlm, je peux vouloir sélectrionner des éléments avec un "id" particulier. Dans mon cas, il n'y en avait pas d'intéressant sur le site de Baseball Québec Outaouais
#Note : S’il y	a plusieurs	éléments <a> dans une page,	mais que seul celui	ou ceux dont le	id m'intéresse, j'écris id="le mot que je cherche"	
#BeautifulSoup me retourne le code html de ce que je cherche
#Dans ce cas, pas de id. mais le script aurait cette forme s'il y en avait. Il faut juste ajouter l'élément entre les guillemets (Mettre "a")
# print(page.find("div", id="art-main"))


#Chercher dans le HTML avec la classe ou class
#s'utilse s'il y a plusieurs éléments <td> dans la page, mais que c'est la classe "team-looser" qui m'intéresse. Dans ce cas, je veux trouver le nom de l'équipe
#perdante dans les données que j'ai.

# print(page.find_all("td", class_="team-looser"))


#chercher dans le HTML avec "name"
#S'utilise avec meta

# print(page.find("meta",	attrs={"name":"keywords"}))

# Pour récupérer le contenu, il faut utiliser la fonction .text
# J'ai éprouvé quelques difficultés avec cette fonction, car quand je voulais trouver avec find_all ET .text, ça me donnait une erreur. Je n'ai pas réussi à trouver de solution en ligne.

# print(page.find("a").text)
#pour trouver que le premier élément

# print(page.find("td").text)
#avec td (au-dessus)

#pour tous les trouver, j'aurais écrit comme suit : 
# print(page.find_all("td").text)
#mais ça ne fonctionne pas, ça considère le .text comme un attribut et non comme une fonction et je n'arrive pas à comprendre pourquoi. J'aimerais y revenir rapidement en classe si c'est possible.
#Toutefois, afin de trouver ce que je cherchais, j'ai réussi à trouver une formule semblable. On peut le trouver dans ma boucle finale.

#valeur des attributs: pour récupérer les hyperliens dans les balises <a>
# Note : BeautilfulSoup transforme un attribut et sa valeur en un petit dictionnaire (comme name). La clé est l’attribut et la valeur… la valeur.

# print(page.find("a")["href"]) 
#Dans le bash : donne le site de baseball outaouais sur lequel je suis 



#création d'une boucle pour travailler avec tous les éléments
# print(page.find_all("tr"))
#si je met .text, je vais avoir toute l'information "textuelle" avec laquelle je peux travailler.

# for ligne in page.find_all("tr"):
#     print(ligne.text)
    

#enchainer les fonctions : pour trouver du contenu dans une balise commune. Ici, je veux le contenu de la balise td, et donc j'ajoute la balise précise que je veux.

# print(page.find("td", class_="team-looser").text)
#Ce que j'ai : première équipe a avoir perdu = Hull Volant Hull
#Qui est donc la première équipe à avoir perdu une partie en 2016.

#si je veux voir toutes les fois ou pionniers la peche aparaissent, 

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

#Création de ma boucle ultime : traiter chaque élément.
for ligne in page.find_all("td"):
    # print(ligne.text)
    info=ligne.text
    resultat.append(info.strip())
resultat2=resultat[7:]
#J'enlève les 7 premières lignes, car elles ne me sont pas utiles. 

#J'enlève aussi ce qui ne m'est pas utile à traiter.
for inutile in resultat2:
    if inutile=="Section":
        resultat2.remove(inutile)
for inutile in resultat2:
    if inutile=="Moustique A":
        resultat2.remove(inutile)
for inutile in resultat2:
    if inutile=="":
        resultat2.remove(inutile)
        #bobo ici, il y a des vides, mais même avec ce code, je n'en retire que la moitié. J'ai donc la moitié de mes résultats qui écoutent ma commande...bizarre.
        #Mais je peux quand même travailler avec. Ci-dessous, un autre essai. 
for inutile in resultat2:
    if inutile=="\n":
        resultat2.remove(inutile)
n=-1

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
