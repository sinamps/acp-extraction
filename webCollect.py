import sys
import os
sys.path.append('/s/bach/g/under/videep/.local/bin')
#import html2text
import requests
from bs4 import BeautifulSoup
def getText(url, fileName):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    content = r.text
    content = os.linesep.join([s for s in content.splitlines() if s])
    #findLists(content)
    print(type(soup)) 
    unordredLists = soup.find_all('ul')
    findLists(soup.find_all('ul'), str(fileName) +'UnOrdered')
    findLists(soup.find_all('ol'), str(fileName) +'Ordered')
    findLists(soup.find_all('p'),str(fileName) +'pragraphs')
   
    with open(str(fileName) + 'structure.txt', 'w') as structurefile:                   #Write the entire structure to a file 
        structurefile.write(soup.prettify())                            
    with open(str(fileName) +'paras.txt', 'w') as pfile:                                #Extract paragraphs from body
        for para in soup.find_all("p"):
           pfile.write("%s\n\n" % para.get_text()) 
    with open(str(fileName) +'links.txt', 'w') as lfile:
        for link in soup.find_all('a'):                                             #Extract all links from body
            lfile.write("{text} - {link} \n".format(link = link.get('href') , text = link.get_text()))

def findLists(listOfLists, nameOfFile):
    i=0
    with open(str(nameOfFile) + '.txt', 'a') as lfile:
        for eachList in listOfLists:
            lfile.write('___Heading___')
            lfile.write(str(eachList.find_previous().get_text()) + '\n' )
            lfile.write(str(eachList.get_text()) + '\n')

            i=i+1
        

def main():
    url = sys.argv[1]
    fileName = str(sys.argv[2]) 
    links = []
    paragraphs = []
    #url = 'https://www.luc.edu/its/aboutits/itspoliciesguidelines/access_control_policy.shtml'
    getText(url, fileName)
    


main()
