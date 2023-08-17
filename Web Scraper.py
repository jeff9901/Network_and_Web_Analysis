#import required libraries
import re
import requests
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd

#loop to take user input and validate it
while True:
    original_url = input("Enter the website url(in 'http://www.example.domain/' format):  ")

    try:
        r = requests.get(original_url)
        status = int(r.status_code)
        if status not in range(200, 300):
            print ("Site unavailable or does not exist. Please enter URL again.\n")
        else:
            break
    except (requests.exceptions.InvalidSchema, requests.exceptions.InvalidURL, requests.exceptions.ConnectionError, requests.exceptions.MissingSchema):
        print("Error. Try again.\n")
        continue
    
unscraped = deque([original_url])

scraped = list()

emails = list()

new_emails=list()

#take out the base url from input and create Excel file from name of website to be accessed
split = urlsplit(original_url)
loc = ("{0.netloc}".format(split)).split('.')[1]
file = loc + ".xlsx"
base_url = "{0.scheme}://{0.netloc}".format(split)

if '/' in split.path:
    path = original_url[:original_url.rfind('/')+1]
else:
    path = original_url

#send request to parent website and get its html script        
main_response = requests.get(base_url)

soup = BeautifulSoup(main_response.text, 'html.parser')

#find links in parent website and add to a list 
for anchor in soup.find_all("a"):
    if "href" in anchor.attrs:
        link = anchor.attrs["href"]
    else:
        link = ''
    if link.startswith('/'):
        link = base_url + link
    elif not link.startswith('http'):
        link = path + link
    if not link in unscraped and not link in scraped:
        unscraped.append(link)

#loop to scrape through each element in above-mentioned list
while len(unscraped):
    url = unscraped.popleft()
    scraped.append(url)
    print("Scraping "+ url)

    try:
        response = requests.get(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL, requests.exceptions.ConnectionError):
        continue

    #list containing all entities having regex email format
    lst = list(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]{2,4}", response.text, re.I))

    #loop to fish out emails from above list
    for x in lst:
        if x.endswith(".png"):
            continue
        elif x.endswith(".jpg"):
            continue
        else:
            new_emails.append(x)
            
    #loop to add the emails to the Excel file       
    for i in new_emails:
        if i in emails:
            continue
        else:
            emails.append(i)
            data=[{'Emails': i}] 
            df=pd.DataFrame(emails, columns=["Email"])
            df.to_excel(file, index = False)
     
    
print("Done")