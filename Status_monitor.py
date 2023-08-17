import time
import urllib
from urllib.request import urlopen, Request
import click
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import pandas as pd


@click.group()
def cli():
    pass

@cli.command()
#command to check live status of URLs from input by user in an Excel sheet
def stat_check(): 
    while True:
        #make a list containing entries from the Excel sheet input by the user
        file = input("Enter file name: ")
        df = pd.read_excel(file)
        URLS = list(df['URLs'])                
        print("\nTesting URLs.", time.ctime())

        for url in URLS:
            validate = URLValidator()
            try:
                validate(url)
                status=" "
                #send a request to see whether URL is active or not
                try:
                    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
                    r = Request(url, headers=headers)
                    req = urllib.request.urlopen(r)
                    status = "Active"

                except urllib.request.URLError:
                    status = "Unavailable"

                print(status + ': ' + url)
            except ValidationError:
                print("Invalid URL: " + url)
        print("\nPress 'Ctrl + C' to abort")
        time.sleep(10)
        
            
    
@cli.command()
#command to edit list of URLs in Excel sheet
def change_url(): 
    while True:
        file = input("Enter file name: ")
        df = pd.read_excel(file)

        #code to ask if the user wants to make any changes to the Excel sheet

        change=input("Do you want to add/remove a URL ? YES/NO: ")
        if change.lower() == 'yes':
            add = input("Do you want to add a URL ? YES/NO: ")
            if add.lower()=='yes':
                new=input("Enter URL: ")
                data=[{'URLs': str(new)}]
                df = df.append(data, ignore_index=True)
                df.to_excel(file, index = False)
                break
            elif add.lower()=='no':
                remove = input("Do you want to remove a URL ? YES/NO: ")
                if remove.lower()=='yes':
                    old=input("Enter URL: ")
                    df.drop(df[df['URLs']==str(old)].index, inplace=True)
                    df.to_excel(file, index = False)
                    break
                elif remove.lower=='no':
                    pass
                    break
                else:
                    print("Enter only 'Yes' or 'No'")
                
            else:
                print("Enter only 'Yes' or 'No'")
        elif change.lower()=='no':
            pass
            break
        else:
            print("Enter only 'Yes' or 'No'")
