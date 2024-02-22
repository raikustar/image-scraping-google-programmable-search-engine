import os
import requests as rq
from bs4 import BeautifulSoup as bs
import urllib.request 
import urllib.error
from datetime import date as d
import pandas as pd


# Methods

def fileName(fileTitle, path, index):
    date = d.today()    
    file_name_full = f"{path}/{fileTitle}-{index}-{date}.jpg"
    return file_name_full

def saveUrlToFile(url):
    text_file = "search_history.txt"
    if not os.path.isfile(text_file):
        with open(text_file, "x") as file:
            file.close()

# if url exists don't write new line, elif add new link to list    
    with open(text_file, "a") as wf:
        with open(text_file, "r") as rf:
            ln = rf.readlines()
            n_list = []
            for i in ln:
                n_list.append(i)
            n_url = str(url) + "\n"

            if not n_url in n_list:
                wf.write(n_url)

def filterImageUrl(url):
    link = str(url)
    nl = link[2:-2]
    return nl



# app-esque functions
        
def googleImagesThumbnailWebScraping():
    dataInput = "lion"#input("What are you searching for? ")
    num = 25 #int(input("How many pictures? "))

    google_url = "https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q="
    searching = google_url + dataInput

    response = rq.get(searching)
    soup = bs(response.content, "html.parser")
    results = soup.find_all("img")

    print(results)
    count, links = 1, []

    for result in results:
        try:
            link = result["src"]
            links.append(link)
            count += 1
            if count > num:
                break

        except KeyError:
            continue

    links.pop(0)
    print(links)

    testpath = "imagedata/test/"
    if not os.path.exists(testpath):
        os.mkdir(testpath)

    name = "negative"

    for img in links:
        index = links.index(img)
        string = f"{testpath}{name}{index}.jpg"
        urllib.request.urlretrieve(img, string)
        print(f"Loading {index+1} out of {len(links)}")

def scraping():
    # Google - Custom Google Search JSON API 
    api_key = "Custom_Search_JSON_API_KEY"

    # Google - Programmable search engine url key
    search_key = "your_google_generated_key=cx_string"

    search_input = input("What are you search for? ")
    num_searches = int(input("How many images?(100 maximum due to FREE api)? "))
    img_size = "huge"
    path = "test/"
    search_url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_key}&q={search_input}&searchType=image&imgSize{img_size}"
    
    s = rq.get(url=search_url)
    json_data = s.json()

    try:   
        saved_links = pd.read_csv("search_history.txt", sep=";")
        worked_links = saved_links.values.tolist()
        links = []

        if len(json_data) != 0:
            index = 1
            while index < num_searches:
                if index < len(json_data["items"]):
                    try:
                        image_link = json_data["items"][index]["link"]
                        if image_link in [link[0] for link in worked_links]:
                            num_searches += 1
                        else:
                            print(f"{image_link} is not in worked_links, adding to search_list.txt")
                            saveUrlToFile(url=image_link)
                            links.append(image_link)
                                
                        index += 1
                    except KeyError:
                        continue

                else:
                    break
                        
                    
        elif "error" in json_data:
            print("Error:",json_data["error"]["status"] + " => " + json_data["error"]["details"][0]["reason"]) 
        else:
            print("Unknown error....")     

        
        if not os.path.exists(path=path):
            os.mkdir(path=path)

        if len(links) >= 1:
            for idx, link in enumerate(links):
                urllib.request.urlretrieve(url=link, filename=fileName(fileTitle=search_input, path=path, index=idx))
                print(f"Downloading picture {idx+1}")

    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")


def main():
    scraping()


if __name__ == "__main__":
    main()

