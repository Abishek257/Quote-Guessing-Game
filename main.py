# Import neccessary libraries
import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice

all_quotes = []

base_url = "https://quotes.toscrape.com/"       # static
url = "/page/1"                                 # dynamic

# Extract all quote details from the website and append to the list
while url:
    response = requests.get(f"{base_url}{url}")
    print(f"{base_url}{url}")
    soup = BeautifulSoup(response.text,"lxml")
    
    quotes = soup.find_all(class_ = "quote")
    
    for info in quotes:
        all_quotes.append({
            "text"    : info.find(class_="text").get_text(),
            "author"  : info.find(class_="author").get_text(),
            "bio-link": info.find("a")["href"]
        })
    
    # Update the 'url' to change the page of the website
    next_page = soup.find(class_="next")
    
    if next_page:
        url = next_page.find("a")["href"]
    else:
        url = None
    
    sleep(2)

# Randomly choose one quote from all the extracted quotes       
quote = choice(all_quotes)
remain_guess = 4
print(quote["text"])

# Compare the guessed author name with the actual author name and print the result
guess = ''
while guess.lower() != quote["author"].lower() and remain_guess > 0:
    guess = input(f"Who said this quote? Guess remaining{remain_guess}")
    
    if guess == quote["author"]:
        print("Success")
        break
    remain_guess = remain_guess - 1
    
    if remain_guess == 3:
        response = requests.get(f"{base_url}{quote['bio-link']}")
        soup = BeautifulSoup(response.text,"lxml")
        Birth_date = soup.find(class_="author-born-date").get_text()
        Birth_place = soup.find(class_="author-born-location").get_text()
        
        print(f"Hint: Author birth date and location{Birth_date}{Birth_place}")
    
    elif remain_guess == 2:
        first_name = quote["author"][0]
        print(f"Hint: Author First name starts with{first_name}")
        
    elif remain_guess == 1:
        last_name = quote["author"].split(" ")[1][0]
        print(f"Hint: Author's last name starts with{last_name}")
    
    else:
        print(f"Failure! Answer is {quote['author']}")