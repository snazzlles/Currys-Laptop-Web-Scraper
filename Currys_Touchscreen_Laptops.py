#Web Scraping - Own's Attempt at Several Websites
#21/07/20
#Scraping information on TOUCHSCREEN LAPTOPS from all currys pages

#-------------------------------------------------------------------------------
#importing beautiful soup and url open
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


#-------------------------------------------------------------------------------
#opening the csv file to prepare to write
filename = "Touchscreen_Laptops2.csv"

#filename = "Currys_Laptops.csv"
f = open(filename, "w")     #common place to use "f" as a variable name for the file that's open to write to

headers = "Product Name, Screen Size, CPU, OS, RAM, Memory, Price \n"

f.write(headers)

#-------------------------------------------------------------------------------
def CurrysScrape(my_url):
    #my_url = 'https://www.currys.co.uk/gbuk/computing/laptops/laptops/315_3226_30328_xx_ba00013339-bv00312517/1_50/relevance-desc/xx-criteria.html'

    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, "html.parser")


    containers = page_soup.findAll("article", {"class":"product result-prd stamped"})
    print(len(containers))

    def Container_Loop(containers):     #function to gather information and print / write it
        for container in containers:
            title_container = container.findAll("header",{"class":"productTitle"})
            product_name_raw = title_container[0].text.strip().replace("\n"," ")
            product_name = product_name_raw.replace(","," |")

            if '10"' in product_name or '11"' in product_name or '11.6"' in product_name or '12"' in product_name:
                screen = '10" - 12"'
            elif '13"' in product_name or '13.3"' in product_name:
                screen = '13" - 13.3"'
            elif '14"' in product_name:
                screen = '14"'
            else:
                screen = '15"+'

            info_container = container.findAll("ul",{"class":"productDescription"})
            product_info = info_container[0].text.replace("\n",",")
            #print(product_info)

            for i in range(5):
                if "Intel" in product_info.split(",")[i] or "Ryzen" in product_info.split(",")[i] or "Processor" in product_info.split(",")[i]:
                    cpu = product_info.split(",")[i]

                elif "Windows" in product_info.split(",")[i] or "Chrome" in product_info.split(",")[i]:
                    os = product_info.split(",")[i]

                elif "RAM" in product_info.split(",")[i] or "Memory" in product_info.split(",")[i]:
                    memory = product_info.split(",")[i]
                    ram = memory.split("/")[0]
                    storage = memory.split("/")[1]

            price_container = container.findAll("div",{"class":"productPrices"})
            product_price_raw = price_container[0].div.div.strong.text.strip()
            product_price = product_price_raw.replace(",","")

            f.write(product_name + "," + screen + "," + cpu + "," + os + "," + ram + "," + storage + "," + product_price + "\n")
            #print(product_name , "," ,cpu, ",", os ,"," ,ram, ",",memory, ",", product_price,"\n")

    #end of function Container_Loop

    Container_Loop(containers)      #calling function to gather information and print / write it
    #---------------------------------------------------------------------------

    containers = page_soup.findAll("article", {"class":"product result-prd"})
    print(len(containers))

    Container_Loop(containers)      #calling function to gather information and print / write it

    #---------------------------------------------------------------------------

    if my_url != "https://www.currys.co.uk/gbuk/computing/laptops/laptops/315_3226_30328_xx_ba00013339-bv00312517/3_50/relevance-desc/xx-criteria.html":
        next_page_raw = page_soup.findAll("a", {"title":"next"})
        next_page = next_page_raw[0].get('href')
        return next_page

    f.close()
#end of function CurrysScrape


my_url = 'https://www.currys.co.uk/gbuk/computing/laptops/laptops/315_3226_30328_xx_ba00013339-bv00312517/1_50/relevance-desc/xx-criteria.html'
next_page = CurrysScrape(my_url)

for i in range (2):
    my_url = next_page
    next_page = CurrysScrape(my_url)

