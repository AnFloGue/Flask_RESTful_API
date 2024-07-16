from flask import Flask, jsonify, request, render_template
import json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import redis


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

app = Flask(__name__)
limiter = Limiter(app=app, key_func=get_remote_address)


def load_books():
    try:
        with open('books.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_books(books):
    with open('books.json', 'w') as file:
        json.dump(books, file, indent=4)


books = load_books()


@app.route('/api/books', methods=['GET'])
@limiter.limit("10/minute")  # Apply rate limiting
def get_books():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    start_index = (page - 1) * limit
    end_index = start_index + limit
    paginated_books = books[start_index:end_index]
    return jsonify(paginated_books)


@app.route('/')
def home():
    return render_template('BookManager.html')
# Apply rate limiting to other endpoints as needed
@app.route('/api/books', methods=['POST'])
@limiter.limit("5/minute")  # Example: Different rate limit for POST requests
def add_book():
    # Implementation remains the same
    ...


@app.route('/api/books/<int:id>', methods=['PUT'])
@limiter.limit("5/minute")  # Example: Apply rate limiting
def update_book(id):
    # Implementation remains the same
    ...


@app.route('/api/books/<int:id>', methods=['DELETE'])
@limiter.limit("5/minute")  # Example: Apply rate limiting
def delete_book(id):
    # Implementation remains the same
    ...


@app.route('/api/books', methods=['GET'])
def handle_books():
    # Log a message when a GET request is received
    app.logger.info('GET request received for /api/books')
    # Handle the request logic
    # ...


if __name__ == "__main__":
    app.run(debug=True)
