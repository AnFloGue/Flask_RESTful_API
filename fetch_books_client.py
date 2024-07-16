import requests

# http://127.0.0.1:5001/api/books?page=2&limit=10
def fetch_books(base_url, page=1, limit=10):
    response = requests.get(f"{base_url}/api/books", params={"page": page, "limit": limit})
    if response.status_code == 200:
        return response.json()
    else:
        return None


def main():
    base_url = "http://127.0.0.1:5001"
    page = 1
    limit = 10
    all_books = []
    
    while True:
        books = fetch_books(base_url, page, limit)
        if not books:
            break
        all_books.extend(books)
        if len(books) < limit:
            break
        page += 1
    
    print(f"Fetched {len(all_books)} books in total.")


if __name__ == "__main__":
    main()
