from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        #lista de autores que ha marcado como favoritos
        self.favoritos_de_autores = []
    
    @classmethod
    def get_all(cls):
        query = "SELECT * from books;"
        books = []
        results = connectToMySQL('favorites_books').query_db(query)
        for row in results:
            books.append(cls(row))
        return books
    
    @classmethod
    def save (cls,data):
        query = "INSERT INTO books (title, num_of_pages) VALUES (%(title)s, %(num_of_pages)s);"
        return connectToMySQL('favorites_books').query_db(query,data)
    
    @classmethod
    def get_by_one(cls, data):
        query = "SELECT * FROM books LEFT JOIN favorites ON books.id = favorites.book_id LEFT JOIN authors ON authors.id = favorites.author_id WHERE books.id = %(id)s;"
        results = connectToMySQL('favorites_books').query_db(query,data)
        book = cls(results[0])
        for row in results:
            if row['authors.id'] == None:
                break
            data = {
                "id": row['authors.id'],
                "name": row['name'],
                "created_at" : row['created_at'],
                "created_at" : row['created_at']
            }
            book.favoritos_de_autores.append(author.Author[data])
            return book
    
    @classmethod
    def unfavorited_books(cls,data):
        query = "SELECT * FROM books WHERE books.id NOT IN(SELECT book_id FROM favorites WHERE author_id = %(id)s);"
        results = connectToMySQL('favorites_books').query_db(query,data)
        books = []
        for row in results:
            books.append(cls(row))
        print(books)
        return books