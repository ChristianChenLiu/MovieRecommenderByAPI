import requests_with_caching #this is course specific, need to create a personal key instead and perform queries through it
import json

def get_movies_from_tastedive(name):
    tastedive_params = {"q":name,"type": "movies","limit": 5}
    response = requests_with_caching.get("https://tastedive.com/api/similar", params = tastedive_params)
    return json.loads(response.text)

def extract_movie_titles(tastedive_dict):
    res = list()
    for movie in tastedive_dict['Similar']['Results']:
        res.append(movie['Name'])
    return res

def get_related_titles(movie_titles_list):
    if not movie_titles_list: return movie_titles_list
    related_titles = set()
    for title in movie_titles_list:
        related_list = extract_movie_titles(get_movies_from_tastedive(title))
        for movie_title in related_list:
            related_titles.add(movie_title)
    return list(related_titles)

def get_movie_data(movie_title):
    return json.loads(requests_with_caching.get('http://www.omdbapi.com/', params = {"t": movie_title, "r": 'json'}).text)

def get_movie_rating(OMDB_dict):
    for rating in OMDB_dict['Ratings']:
        if rating['Source'] == 'Rotten Tomatoes':
            return int(rating['Value'][:-1])
    return 0

def get_sorted_recommendations(movie_titles_list):
    related_movies_titles_list = get_related_titles(movie_titles_list)
    
    return sorted(related_movies_titles_list, key = lambda title: (get_movie_rating(get_movie_data(title)), title), reverse=True)