


from bs4 import BeautifulSoup
import requests
import re
import random
import json  # Import the json module

# List of user-agent strings
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
]

# Define the headers to be used in the request
HEADERS = {
    "User-Agent": random.choice(USER_AGENTS),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}

def extract_movie_info(movie_item):
    """
    Extracts the movie title and year from a single movie list item.

    Args:
        movie_item: A BeautifulSoup object representing a single movie list item (<li>).

    Returns:
        A dictionary containing the movie title and year, or None if an error occurs.
    """
    try:
        # Extract the movie title
        title_element = movie_item.select_one("a.ipc-title-link-wrapper h3.ipc-title__text")
        if title_element:
            text_content = title_element.text.strip()
            match = re.search(r"\d+\.\s+(.+)", text_content)
            if match:
                title = match.group(1)
            else:
                title = text_content
        else:
            title = None

        # Extract the movie year
        year_element = movie_item.select_one("span.sc-e8bccfea-7.hvVhYi.cli-title-metadata-item")
        year = year_element.text.strip() if year_element else None

        return {"title": title, "year": year}

    except Exception as e:
        print(f"An error occurred while extracting movie info: {e}")
        return None

def extract_top_movies(url, num_movies=25):
    """
    Extracts the top N movie details from the IMDb Top 250 chart.

    Args:
        url: The URL of the IMDb Top 250 chart.
        num_movies: The number of movies to extract.

    Returns:
        A list of dictionaries, where each dictionary contains the title and year of a movie.
    """
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Target the list of movies
        movie_list = soup.select_one("ul.ipc-metadata-list.ipc-metadata-list--dividers-between.sc-e22973a9-0.khSCXM.compact-list-view.ipc-metadata-list--base")
        if not movie_list:
            print("Could not find the movie list.")
            return []

        # Target the list items
        movie_items = movie_list.select("li.ipc-metadata-list-summary-item")

        movie_details = []
        for movie_item in movie_items[:num_movies]:  # Iterate through the first num_movies
            movie_info = extract_movie_info(movie_item)
            if movie_info:
                movie_details.append(movie_info)

        return movie_details

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def save_to_json(data, filename="movie_data.json"):
    """
    Saves the movie data to a JSON file.

    Args:
        data: A list of dictionaries, where each dictionary contains the title and year of a movie.
        filename: The name of the JSON file to create.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=4, ensure_ascii=False)  # Use json.dump() to write JSON data

        print(f"Data saved to {filename}")

    except Exception as e:
        print(f"An error occurred while saving to JSON: {e}")

# Example usage
url = "https://www.imdb.com/chart/top/"
top_movies = extract_top_movies(url, num_movies=25)

if top_movies:
    save_to_json(top_movies)