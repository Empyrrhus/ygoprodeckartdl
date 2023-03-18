# ygoprodeckartdl

A simple python script to selectively download Yu-Gi-Oh! card images from ygoprodeck.com.

# Installation
Requirements: Python 3

Clone the repository and run the script from command line:
```
>pip install -r requirements.txt
```

# Instructions
You can run the script from the command line with:
```
>python ygoprodeckartdl.py [arguments]
``` 

Command line arguments:
```
-full						Downloads the full card art into the \image_url folder.
-small					Downloads the thumbnail card art into the \image_url_small folder.
-cropped				Downloads the cropped card art into the \image_url_cropped folder.
-param					Enables a selective filter of cards to download. If not used, will default to downloading all available TCG cards.
-keyword				Creates a text file containing related keywords for every downloaded image.
```
At least one of the "-full", "-small", or "-cropped" arguments must be used, otherwise there will be no cards to download.

If "-param" is used, you must enter your filter in JSON format when prompted by the script.
For example, to download all TCG cards in the Blue-Eyes archetype, you would enter this filter:
```
{"format": "tcg", "archetype": "Blue-Eyes"}
```
Only cards that satisfy all parameters in the filter will be downloaded. For a list of parameters, see the official <a href="https://ygoprodeck.com/api-guide/">YGOPRODeck api guide</a>.

If the script fails to download any images (for example, the missing cropped art of <a href="https://ygoprodeck.com/card/sanctity-of-dragon-8825">Sanctity of Dragon</a>, that card will be listed in "failed_downloads.txt".