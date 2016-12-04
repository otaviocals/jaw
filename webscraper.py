#                                                                                                       #
#   Just Another Webscraper (J.A.W.)                                                                    #
#                                    v0.1                                                               #
#                                                                                                       #
#       written by Otavio Cals                                                                          # 
#                                                                                                       #
#   Description: A webscrapper for downloading tables and exporting them to .csv files autonomously.    #
#                                                                                                       #
#########################################################################################################


#Required external modules: Selenium, BeautifoulSoup4, Hashlib

from csv import writer, reader
from unicodedata import normalize
from contextlib import closing
from selenium.webdriver import PhantomJS
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from pathlib import Path
from hashlib import sha512
from os.path import isdir
from os import makedirs,getcwd
from sys import platform


rows = []
current_os = platform

if current_os.startswith("linux"):
    slash = "/"
elif current_os.startswith("win32") or current_os.startswith("cygwin"):
    slash = "\\"
elif current_os.startswith("darwin"):
    slash = "/"
else:
    slash = "/"


######################
# Webscrapping Stage #
######################

def Webscraper(url, folder):

#Getting Raw Data

    with closing(PhantomJS()) as browser:
        browser.get(url)
        browser.implicitly_wait(10)
    
        page_source = browser.find_element_by_class_name("a78")
    
        dates = browser.find_element_by_class_name("a19").text

        title = browser.find_element_by_class_name("mnuTitulo").text.replace(" ", "_")
        title += "_"
        title += browser.find_element_by_class_name("a25l").text.replace(" ", "_").upper()

        print(title)

        page_source = browser.page_source

######################
#  Processing Stage  #
######################

#Getting Title of Table

    title = normalize("NFKD",title).encode("ASCII","ignore").decode("ASCII")

#Getting Table Dates
    
    date_string_cut = dates.find(" a ")
    start_date = dates[:date_string_cut]
    end_date = dates[date_string_cut+3:]

#Getting Table Data

    table_start = page_source.find("class=\"a85\"")-93
    start_cut_source = page_source[table_start:]

    table_end = start_cut_source.find("</td></tr></tbody></table>")+26
    html_table = start_cut_source[:table_end]

#Getting Table Digest

    current_hash = sha512(html_table.encode("UTF-8")).hexdigest()

#Parsing HTML to XML

    soup_table = BeautifulSoup(html_table, "lxml")

######################
#    Writing Stage   #
######################

#Check Folder Existence

    if(not isdir(folder)):
        makedirs(folder)
    
#Creating Document if there is no previous file

    if(not Path(folder+slash+title+".csv").is_file()):
        for tr in [soup_table.find_all("tr")[2]]:
            tds = tr.find_all("td")
            row = [elem.text for elem in tds]
            row.insert(0,"Data")
            rows.append(row)
            append_to_csv = True
        
#Loading previous file if it exists
        
    else:
        with open(folder+slash+title+".csv","r",encoding="UTF-8") as f:
            csv_file_read = reader(f)
            for read_row in csv_file_read:
                rows.append(read_row)
            
#Checking Digests
            
            same_table = (current_hash == rows[len(rows)-1][2])
            if(not same_table):
                rows.pop()
                append_to_csv = True
                print("Changes Detected! Appending new data...")
            else:
                append_to_csv = False
                print("No changes detected.")

#Parsing XML to CSV
            
    if(append_to_csv):
        for tr in soup_table.find_all("tr")[3:]:
            tds = tr.find_all("td")
            row = [elem.text for elem in tds]
            row.insert(0,end_date)
            rows.append(row)
        rows.append(["","Current Version:",current_hash])

#Writing current table to file

    with open(folder+slash+title+".csv","w",encoding="UTF-8") as f:
        csv_file = writer(f)
        csv_file.writerows(rows)


######################
#        Main        #
######################

if __name__ == "__main__":
    from sys import argv
    url = input("Enter url to scrap from:\n")
    folder = input("Enter folder to download to:\n")
    Webscraper(url,folder)
