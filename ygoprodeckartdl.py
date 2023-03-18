#created by Empyrrhus

import json #allow user to pass api request parameters
import sys #read command line arguments
import requests #api request
import urllib.request #download images
import os #create directories
from time import sleep #limit api request rate
from tqdm import tqdm #downloading progress bar

#YGOPRODECK rate limit is 20 requests per second, will be IP banned for 1 hour if violated
requests_per_second = 15

#get cards and sets data from YGOPRODECK using api call
input_param = {"format": "tcg", "sort": "id"}
if "-param" in sys.argv:
    print("Enter custom parameters:")
    while True:
        input_raw = input()
        try:
            input_param = json.loads(input_raw)
            break
        except:
            pass
        print("Please enter a valid JSON object, ex. {\"format\": \"tcg\", \"archetype\": \"Blue-Eyes\"}")
response = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php', params = input_param)
response_sets = requests.get('https://db.ygoprodeck.com/api/v7/cardsets.php')
set_dict = dict()

#functions
#sort card set name and year into dictionary
def sort_sets():
    for set in response_sets.json():
        if "set_name" in set and "tcg_date" in set:
            set_dict.update({set["set_name"]:set["tcg_date"][:4]})
    return

#create a text file for every image, containing related keywords
def keyword_file(image_type, card, card_image):
    with open(image_type + "/" + str(card_image["id"]) + ".txt", 'w', encoding="utf-8") as f:
        if "id" in card:
            f.write(str(card["id"]) + ", ")
        if "name" in card:
            f.write(str(card["name"]) + ", ")
        if "type" in card:
            f.write(str(card["type"]) + ", ")
        if "frameType" in card:
            f.write(str(card["frameType"]) + ", ")
        if "atk" in card:
            f.write(str(card["atk"]) + "ATK, ")
        if "def" in card:
            f.write(str(card["def"]) + "DEF, ")
        if "level" in card:
            if card["frameType"] == "xyz":
                f.write("Rank " + str(card["level"]) + ", ")
            else:
                f.write("Level " + str(card["level"]) + ", ")
        if "race" in card:
            f.write(str(card["race"]) + ", ")
        if "attribute" in card:
            f.write(str(card["attribute"]) + ", ")
        if "archetype" in card:
            f.write(str(card["archetype"]) + ", ")
        if "scale" in card:
            f.write(str(card["scale"]) + ", ")
        if "linkval" in card:
            f.write("Link " + str(card["linkval"]) + ", ")
        if "linkmarkers" in card:
            f.write(str(card["linkmarkers"]).replace('[', '').replace(']', '').replace('\'', '') + ", ")
        if "card_sets" in card:
            for set in card["card_sets"]:
                if "set_name" in set:
                    f.write(str(set["set_name"]) + ", ")
                if "set_code" in set:
                    f.write(str(set["set_code"]) + ", ")
                if "set_rarity" in set:
                    f.write(str(set["set_rarity"]) + ", ")
                if "set_rarity_code" in set and set["set_rarity_code"] != "":
                    f.write(str(set["set_rarity_code"]).replace('(', '').replace(')', '') + ", ")
                if str(set["set_name"]) in set_dict: #add year of set release as a keyword
                    f.write(str(set_dict[str(set["set_name"])]) + ", ")
        if "banlist_info" in card and "ban_tcg" in card["banlist_info"]:
            f.write(str(card["banlist_info"]["ban_tcg"]) + ", ")
        if "formats" in card:
            f.write(str(card["formats"]) + ", ")
        if "treated_as" in card:
            f.write("Treated as " + str(card["treated_as"]) + ", ")
        if "desc" in card:
            f.write(str(card["desc"]).replace(',', '').replace('\n', ' ').replace('\r',''))
        f.close()
    return

#check for server response
if response.status_code == 200:
    #user chooses which image sets to download
    if "-full" not in sys.argv and "-small" not in sys.argv and "-cropped" not in sys.argv:
        print("No images downloaded. Try adding \"-full\", \"-small\", or \"-cropped\" arguments to download those respective image sets.")
    else:
        #create set lookup for keyword date tag
        if "-keyword" in sys.argv:
            sort_sets()
        
        #create output folders if it does not already exist
        if "-full" in sys.argv and not os.path.exists("image_url"):
            os.mkdir("image_url")
        if "-small" in sys.argv and not os.path.exists("image_url_small"):
            os.mkdir("image_url_small")
        if "-cropped" in sys.argv and not os.path.exists("image_url_cropped"):
            os.mkdir("image_url_cropped")

        #download every received card to appropriate folder
        with open("failed_downloads.txt", 'w', encoding="utf-8") as g:
            fail_counter = 0
            for card in tqdm(response.json()["data"]):
                for card_image in card["card_images"]:
                    try:
                        if "-full" in sys.argv:
                            sleep(1 / requests_per_second)
                            urllib.request.urlretrieve(str(card_image["image_url"]), "image_url/" + str(card_image["id"]) + ".jpg")
                            if "-keyword" in sys.argv:
                                keyword_file("image_url", card, card_image)
                        if "-small" in sys.argv:
                            sleep(1 / requests_per_second)
                            urllib.request.urlretrieve(str(card_image["image_url_small"]), "image_url_small/" + str(card_image["id"]) + ".jpg")
                            if "-keyword" in sys.argv:
                                keyword_file("image_url_small", card, card_image)
                        if "-cropped" in sys.argv:
                            sleep(1 / requests_per_second)
                            urllib.request.urlretrieve(str(card_image["image_url_cropped"]), "image_url_cropped/" + str(card_image["id"]) + ".jpg")
                            if "-keyword" in sys.argv:
                                keyword_file("image_url_cropped", card, card_image)
                    except:
                         g.write(str(card["name"]) + " - " + str(card_image["id"]) + "\n")
                         fail_counter += 1
        g.close()
        print("\nDone. Failed downloads: " + str(fail_counter) + ".")
        if fail_counter > 0:
            print("\nSee failed_downloads.txt for details.")
else:
    print("\nError: " + str(response.status_code))
    if response.status_code == 400:
        print("Bad Request")
    elif response.status_code == 401:
        print("Unauthorized")
    elif response.status_code == 403:
        print("Forbidden")
    elif response.status_code == 404:
        print("Not Found")
    elif response.status_code == 429:
        print("Too Many Requests")
    elif response.status_code == 500:
        print("Internal Server Error")
    elif response.status_code == 501:
        print("Not Implemented")
    elif response.status_code == 502:
        print("Bad Gateway")
    elif response.status_code == 503:
        print("Service Unavailable")
    elif response.status_code == 504:
        print("Gateway Timed Out")