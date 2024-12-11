from mongita import MongitaClientDisk
from bson.objectid import ObjectId

client = MongitaClientDisk()
db = client.MovieDirectorDB

directors = db.directors
movies = db.movies

def add_director(name):
    if directors.find_one({"name": name}):
        raise ValueError("Director already exists")
    return directors.insert_one({"name": name})

def get_all_directors():
    return list(directors.find())

def update_director(director_id, new_name):
    result = directors.update_one({"_id": ObjectId(director_id)}, {"$set": {"name": new_name}})
    if result.matched_count == 0:
        raise ValueError("Director not found")
    return result

def delete_director(director_id):
    directors.delete_one({"_id": ObjectId(director_id)})
    movies.delete_many({"director_id": ObjectId(director_id)})


def add_movie(title, director_id):
    if not directors.find_one({"_id": ObjectId(director_id)}):
        raise ValueError("Director not found")
    return movies.insert_one({"title": title, "director_id": ObjectId(director_id)})

def get_all_movies():
    return list(movies.find())

def update_movie(movie_id, new_title, new_director_id):
    if not directors.find_one({"_id": ObjectId(new_director_id)}):
        raise ValueError("Director not found")
    result = movies.update_one(
        {"_id": ObjectId(movie_id)},
        {"$set": {"title": new_title, "director_id": ObjectId(new_director_id)}}
    )
    if result.matched_count == 0:
        raise ValueError("Movie not found")
    return result

def delete_movie(movie_id):
    movies.delete_one({"_id": ObjectId(movie_id)})
