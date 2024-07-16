from flask import Flask, jsonify, request, render_template
import json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(app=app, key_func=get_remote_address)


def load_books():
    try:
        with open('books.json') as file:
            return json.load(file)
    except Exception:
        return []


def save_books(books):
    with open('books.json', 'w') as file:
        json.dump(books, file, indent=4)


books = load_books()


@app.route('/api/books', methods=['GET'])
@limiter.limit("10/minute")
def get_books():
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 10))
    start = offset
    end = start + limit
    total_books = len(books)
    if start > total_books or start < 0:
        return jsonify({'error': 'Invalid offset'}), 400
    if limit < 1:
        return jsonify({'error': 'Invalid limit'}), 400
    return jsonify(books[start:min(end, total_books)])


@app.route('/api/books', methods=['POST'])
@limiter.limit("5/minute")
def add_book():
    data = request.get_json(force=True)
    if 'title' in data and 'author' in data:
        new_id = max([book['id'] for book in books], default=0) + 1
        books.append({'id': new_id, **data})
        save_books(books)
        return jsonify({'id': new_id, **data}), 201
    return jsonify({'error': 'Missing title or author'}), 400


@app.route('/api/books/<int:id>', methods=['PUT', 'DELETE'])
@limiter.limit("5/minute")
def modify_book(id):
    book = next((b for b in books if b['id'] == id), None)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    if request.method == 'PUT':
        book.update(request.get_json(force=True))
        save_books(books)
        return jsonify(book), 200
    elif request.method == 'DELETE':
        books.remove(book)
        save_books(books)
        return jsonify({'message': 'Book deleted successfully'}), 200


@app.route('/book-manager')
def book_manager():
    return render_template('BookManager.html')


if __name__ == "__main__":
    app.run(debug=True)
