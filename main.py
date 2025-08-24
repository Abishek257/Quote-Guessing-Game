from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from random import choice

app = Flask(__name__)

BASE_URL = "https://quotes.toscrape.com"
ALL_QUOTES = []


def scrape_quotes():
    """Scrape quotes once and cache them."""
    if ALL_QUOTES:  # already scraped
        return

    url = "/page/1"
    while url:
        response = requests.get(f"{BASE_URL}{url}")
        soup = BeautifulSoup(response.text, "lxml")

        quotes = soup.find_all(class_="quote")
        for info in quotes:
            ALL_QUOTES.append({
                "text": info.find(class_="text").get_text(),
                "author": info.find(class_="author").get_text(),
                "bio-link": info.find("a")["href"]
            })

        next_page = soup.find(class_="next")
        url = next_page.find("a")["href"] if next_page else None


@app.route("/")
def index():
    scrape_quotes()
    return render_template("index.html")


@app.route("/get_quote")
def get_quote():
    """Return a random quote to start the game."""
    quote = choice(ALL_QUOTES)
    return jsonify({
        "text": quote["text"],
        "author": quote["author"],
        "bio_link": quote["bio-link"],
        "guesses": 4
    })


@app.route("/get_hint", methods=["POST"])
def get_hint():
    """Return hint depending on guesses left."""
    data = request.json
    quote = data["quote"]
    guesses_left = data["guesses"]

    if guesses_left == 3:
        response = requests.get(f"{BASE_URL}{quote['bio_link']}")
        soup = BeautifulSoup(response.text, "lxml")
        birth_date = soup.find(class_="author-born-date").get_text()
        birth_place = soup.find(class_="author-born-location").get_text()
        return jsonify({"hint": f"Born on {birth_date} {birth_place}."})

    elif guesses_left == 2:
        return jsonify({"hint": f"First name starts with '{quote['author'][0]}'."})

    elif guesses_left == 1:
        parts = quote["author"].split()
        if len(parts) > 1:
            return jsonify({"hint": f"Last name starts with '{parts[-1][0]}'."})
        else:
            return jsonify({"hint": f"Name starts with '{quote['author'][0]}'."})

    return jsonify({"hint": None})


if __name__ == "__main__":
    app.run(debug=True)
