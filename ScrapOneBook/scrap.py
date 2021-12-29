########### Nous allons recuperer mes données d'un seul livre #########################
#   http://books.toscrape.com/
#
#   csv file structure
#
#   product_page_url
#   universal_ product_code (upc)
#   title
#   price_including_tax
#   price_excluding_tax
#   number_available
#   product_description
#   category
#   review_rating
#   image_url
#
######### les modules à utilser ############
import requests,csv, os
# import de la bibliothéque Beautifullsoup
from bs4 import BeautifulSoup

def get_data(url):
    
    # Recuperer le contenu brut de la page
    html_brut = requests.get(url)
    
    # Pour savoir si un contenu a était renvoyé, on peut tester html_brut.ok  Ou html_brut.status_code = 200 
    if html_brut.ok:
        
        # Parser le code source enregistré dans html_brut : Changer le format de HTML vers un format facilement comprehensible par Python
        soup = BeautifulSoup(html_brut.content,'lxml')

        # on recupére les données dans un dictionnaire
        results= {"product_page_url":"",
                  "image_url":"",
                  "category":"","title":"","product_description":"","universal_ product_code (upc)":[],"price_excluding_tax":"",
                  "price_including_tax":"","number_available":"","review_rating":""}
        
        # URL de la page
        results['product_page_url'] = url
        # URL de l'image
        results["image_url"]= soup.findAll('img')[0].attrs['src']

        # Dans le source HTML recuperé, le titre du livre est défini 
        # on recupere les elements de la liste [breadcrumb]
        list = soup.find('ul', attrs={'class':'breadcrumb'})
    
        results['category'] = list.find_all('a')[2].string 

        # dans la classe [col-sm-6 product_main] et dans le tag [h1] 
        results['title'] = soup.find(class_='col-sm-6 product_main').h1.text
            
        # la description , c'est le 4ieme paragraphe [p]
        results['product_description'] = soup.select('p')[3].text
               
        # les reste des informations se trouve dans une table [table table-striped]
        table = soup.find('table', attrs={'class': 'table table-striped'})
        
        # 1iere tag td, UPC
        results['universal_ product_code (upc)'] = table.find_all('td')[0].string                
        
        # 3iéme balise td, Price (excl. tax)
        results['price_excluding_tax'] = table.find_all('td')[2].string 
        
        # 4iéme balise td, Price (incl. tax)
        results['price_including_tax'] = table.find_all('td')[3].string  

        # 6iéme balise td, Availability
        results['number_available'] = table.find_all('td')[5].string       
        
        # 7iéme balise td, Number of reviews     
        results['review_rating'] = table.find_all('td')[6].string
    return results

def to_csv(file_name,dict):
    
    # generer le fichier csv
    csv_headers = ["product_page_url","image_url","category","title","product_description", \
               "universal_ product_code (upc)","Product Type","price_excluding_tax", \
               "price_including_tax","number_available","review_rating"]

    # on crée le dossier csv/, s il n 'existe pas 
    os.makedirs("csv/", exist_ok=True)

    # créer le fichier dans le dossier csv
    with open("csv/"+file_name, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = csv_headers)
        writer.writeheader()
        writer.writerows(dict)

def get_img(url_img,name_img):
    
    url_site = 'http://books.toscrape.com'   
    # recuperer le chemin complet de l'image
    url_img = requests.compat.urljoin(url_site,url_img)
   

    # generer le nom de l'image (le nom du produit comme nom d'image)
    name_img = name_img+".jpg"

    # on crée  le dossier img/ s'il n'existe pas
    os.makedirs("img/", exist_ok=True)

    # pour sauvegarder les images dans le dossier img/ , on modife le chemin  
    name_img = 'img/'+name_img

    # telecharger l'image
    with open(name_img, 'wb') as f:
        f.write(requests.get(url_img).content)

def main():
    url_site = 'http://books.toscrape.com'   
    url_page = 'http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html'
    books = []
    # Récuperation des données sur le livre
    books.append(get_data(url_page))
    # Extraction des données du livre dans un fichier csv
    to_csv('Onebook.csv',books)
    
    # Extraction l'image associée au livre
    get_img(books[0].get("image_url"),books[0].get("title"))

if __name__== '__main__':
    main()