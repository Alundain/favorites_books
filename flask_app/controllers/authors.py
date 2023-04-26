from flask import render_template, redirect, request
from flask_app import app
from flask_app.models.author import Author
from flask_app.models.book import Book


@app.route('/')
def index():
    return redirect('/authors')

@app.route('/authors')
def author():
    authors = Author.get_all()
    return render_template("authors.html", all_authors = authors)

@app.route('/create/author', methods=['POST'])
def create_author():
    data = {
        "name": request.form['name']
    }
    author_id = Author.save(data)
    return redirect('/authors')

@app.route('/author/<int:id>')
def show_author(id):
    data = {
        "id": id
    }
    #datos del autor
    name_author=Author.get_by_id(data)
    # libros que NO escribió el autor
    no_favoritos_books=Book.unfavorited_books(data)
    # libros que SI escribió el autor TODO

    return render_template('show_author.html', name_author=Author.get_by_id(data), no_favoritos_books=Book.unfavorited_books(data))

@app.route('/favortites/book',methods=['POST'])
def favortites_book():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    Author.add_favorites(data)
    return redirect(f"/author/{request.form['author_id']}")