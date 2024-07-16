document.addEventListener("DOMContentLoaded", function() {
    fetchBooks(0, 10); // Initial fetch for the first 10 books
});

let offset = 0;
const limit = 10;

function fetchBooks(offset, limit) {
    fetch(`http://127.0.0.1:5000/api/books?offset=${offset}&limit=${limit}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const booksList = document.getElementById('booksList');
            if (offset === 0) booksList.innerHTML = ''; // Clear the list if offset is 0
            data.forEach(book => {
                const listItem = document.createElement('li');
                listItem.textContent = `${book.id}. ${book.title} - ${book.author}`;
                booksList.appendChild(listItem);
            });
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}

document.getElementById('loadMore').addEventListener('click', function() {
    offset += limit; // Increase the offset to load the next set of books
    fetchBooks(offset, limit);
});