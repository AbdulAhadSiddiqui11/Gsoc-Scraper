import requests, openpyxl 
import bs4
from collections import defaultdict

organisation_frequency = defaultdict(int)

for Gyear in range(2016,2021):
    # Replace "YEAR" by the year you 
    # want to get data from. Eg. "2018" 
    url = 'https://summerofcode.withgoogle.com/archive/'+str(Gyear)+'/organizations/'

    # Creating a response object 
    # from the given url 
    res = requests.get(url) 

    # We'll be using the Archive page 
    # of GSoC's website as our source. 
    # Checking the url's status 
    res.raise_for_status() 

    # Specify the language you 
    # want to search for 
    language = 'python'

    # BS4 object to store the 
    # html text We use res.text 
    # to get the html code in text format 
    soup = bs4.BeautifulSoup(res.text, 'html.parser') 

    # Selecting the specific tag 
    # with class name 
    orgElem = soup.select('h4[class ="organization-card__name font-black-54"]') 


    # Similarly finding the links 
    # for each org's gsoc page 
    orgLink = soup.find_all("a", class_="organization-card__link") 
    languageCheck = ['no'] * len(orgElem) 
    orgURL = ['none'] * len(orgElem) 

    item = 0
    # Loop to go through each organisation 
    for link in orgLink: 

        # Gets the anchor tag's hyperlink 
        presentLink = link.get('href') 

        url2 = 'https://summerofcode.withgoogle.com' + presentLink 
        print(item) 
        print(url2) 
        orgURL[item] = url2 
        res2 = requests.get(url2) 
        res2.raise_for_status() 

        soup2 = bs4.BeautifulSoup(res2.text, 'html.parser') 
        tech = soup2.find_all("li", 
                        class_="organization__tag organization__tag--technology") 

        # Finding if the org uses 
        # the specified language 
        for name in tech: 

            if language in name.getText(): 
                languageCheck[item] = 'yes'

        item = item + 1
    wb = openpyxl.Workbook() 
    sheet = wb['Sheet'] 

    for i in range(0, len(orgElem)): 
        sheet.cell(row = i + 1, column = 1).value = orgElem[i].getText() 
        sheet.cell(row = i + 1, column = 2).value = languageCheck[i] 
        sheet.cell(row = i + 1, column = 3).value = orgURL[i]
        # if lang. is the specified one.
        # Increment the freq. of that org by one
        if languageCheck[i] == 'yes':
            organisation_frequency[orgElem[i].getText()] += 1

    wb.save('gsocOrgsList'+str(Gyear)+'.xlsx') 

# creating an text file
# with freq.of orgs 
# during specified period which uses the given lang.
file = open("gsocFreq.txt", "w")
i = 0
for org,freq in organisation_frequency.items():
    file.write(str(org) + '\t :' + str(freq) +'\n')
file.close()

