from flask import Flask, request, render_template, redirect, url_for
from database import add_director, get_all_directors, delete_director, update_director
from database import add_movie, get_all_movies, delete_movie, update_movie

app = Flask(__name__)

@app.route('/')
def index():
    all_directors = get_all_directors()
    all_movies = get_all_movies()
    return render_template('index.html', directors=all_directors, movies=all_movies)

@app.route('/add_director', methods=['GET', 'POST'])
def add_director_route():
    if request.method == 'POST':
        name = request.form['name']
        try:
            add_director(name)
        except ValueError as e:
            return str(e), 400
        return redirect(url_for('index'))
    return render_template('add_director.html')

@app.route('/update_director/<id>', methods=['GET', 'POST'])
def update_director_route(id):
    if request.method == 'POST':
        new_name = request.form['name']
        try:
            update_director(id, new_name)
        except ValueError as e:
            return str(e), 400
        return redirect(url_for('index'))
    director = next(d for d in get_all_directors() if str(d["_id"]) == id)
    return render_template('update_director.html', director=director)

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie_route():
    if request.method == 'POST':
        title = request.form['title']
        director_id = request.form['director_id']
        try:
            add_movie(title, director_id)
        except ValueError as e:
            return str(e), 400
        return redirect(url_for('index'))
    all_directors = get_all_directors()
    return render_template('add_movie.html', directors=all_directors)

@app.route('/update_movie/<id>', methods=['GET', 'POST'])
def update_movie_route(id):
    if request.method == 'POST':
        new_title = request.form['title']
        new_director_id = request.form['director_id']
        try:
            update_movie(id, new_title, new_director_id)
        except ValueError as e:
            return str(e), 400
        return redirect(url_for('index'))
    movie = next(m for m in get_all_movies() if str(m["_id"]) == id)
    all_directors = get_all_directors()
    return render_template('update_movie.html', movie=movie, directors=all_directors)

@app.route('/delete_director/<id>')
def delete_director_route(id):
    delete_director(id)
    return redirect(url_for('index'))

@app.route('/delete_movie/<id>')
def delete_movie_route(id):
    delete_movie(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
