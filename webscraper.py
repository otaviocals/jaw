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
import lxml
import sys
import gc



######################
# Webscrapping Stage #
######################

def Webscraper(url, folder, print_output = None, visual_output = None):

    rows = []
    row = []
    append_to_csv = False
    current_os = platform

    if current_os.startswith("linux"):
        slash = "/"
    elif current_os.startswith("win32") or current_os.startswith("cygwin"):
        slash = "\\"
    elif current_os.startswith("darwin"):
        slash = "/"
    else:
        slash = "/"

#Getting Raw Data

    with closing(PhantomJS()) as browser:

        browser.implicitly_wait(10)
        table_class = ""
        tries = 0

#Getting Table HTML
        
        got_table = False
        while tries <= 5:
            browser.get(url)
    
            page_source = browser.find_elements_by_class_name("a85")
            if len(page_source) > 0:
                table_class = "a85"
                got_table = True
                break
            else:
                page_source = browser.find_elements_by_class_name("a84")
                if len(page_source) > 0:
                    table_class = "a84"
                    got_table = True
                    break
            tries += 1
        
#Getting Dates HTML
        
        dates_list = browser.find_elements_by_class_name("a19")
        if len(dates_list) > 0:
            dates_class = "a19"
            dates = browser.find_element_by_class_name("a19").text
        else:
            dates_list = browser.find_elements_by_class_name("a18")
            if len(dates_list) > 0:
                dates_class = "a18"
                dates = browser.find_element_by_class_name("a18").text

#Getting Title HTML

        title = browser.find_element_by_class_name("mnuTitulo").text.replace(" ", "_")
        title += "_"
        sub_title_list = browser.find_elements_by_class_name("a25l")
        if len(sub_title_list) > 0:
            sub_title_class = "a25l"
            sub_title = browser.find_element_by_class_name("a25l").text.replace(" ", "_").upper()
        else:
            sub_title_list = browser.find_elements_by_class_name("a24l")
            if len(sub_title_list) > 0:
                sub_title_class = "a24l"
                sub_title = browser.find_element_by_class_name("a24l").text.replace(" ", "_").upper()
        title += sub_title
        title = normalize("NFKD",title).encode("ASCII","ignore").decode("ASCII")

        print(title)
        if not print_output == None:
            print_output.write((title+"\n").encode("utf-8").decode("utf-8"))
        if not visual_output == None:
            visual_output.append(title+"\n")

        page_source = browser.page_source

######################
#  Processing Stage  #
######################


#Getting Table Dates

    if dates_class == "a19":
        date_string_cut = dates.find(" a ")
        start_date = dates[:date_string_cut]
        end_date = dates[date_string_cut+3:]
    elif dates_class == "a18":
        start_date = dates
        end_date = start_date

#Getting Table Data
    
    table_start = page_source.find("class=\""+table_class+"\"")-93
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
            #row = [normalize("NFKD",ele.text).encode("ASCII","ignore").decode("ASCII") for elem in tds]
            #row.insert(0,"Data")
            row = ["Data","Posicao","Instituicao","% a.m.","% a.a."]
            rows.append(row)
            append_to_csv = True
            print("No file detected. Creating table...")
            if not print_output == None:
                print_output.write("No file detected. Creating table...\n")
            if not visual_output == None:
                visual_output.append("No file detected. Creating table...\n")
        
#Loading previous file if it exists
        
    else:
        with open(folder+slash+title+".csv","r",encoding="UTF-8",newline="") as f:
            csv_file_read = reader(f)
            for read_row in csv_file_read:
                rows.append(read_row)
            
#Checking Digests
            
            same_table = (current_hash == rows[len(rows)-1][2])
            
            if(not same_table):
                rows.pop()
                append_to_csv = True
                print("Changes Detected! Appending new data...")
                if not print_output == None:
                    print_output.write("Changes Detected! Appending new data...\n")
                if not visual_output == None:
                    visual_output.append("Changes Detected! Appending new data...\n")
            else:
                append_to_csv = False
                print("No changes detected.")
                if not print_output == None:
                    print_output.write("No changes detected.\n")
                if not visual_output == None:
                    visual_output.append("No changes detected.\n")

#Parsing XML to CSV
            
    if(append_to_csv == True):
        for tr in soup_table.find_all("tr")[3:]:
            tds = tr.find_all("td")
            row = [elem.text for elem in tds]
            row.insert(0,end_date)
            rows.append(row)
        rows.append(["","Current Version:",current_hash])
        #print(rows[4:])

#Writing current table to file

        with open(folder+slash+title+".csv","w",encoding="utf-8",newline="") as g:
            csv_file = writer(g)
            csv_file.writerows(rows)

    gc.collect()

######################
#        Main        #
######################

if __name__ == "__main__":
    from sys import argv
    url = input("Enter url to scrap from:\n")
    folder = input("Enter folder to download to:\n")
    Webscraper(url,folder)
