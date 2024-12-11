import json

class Book:
    def __init__(self, book_id, title, author, genre, description):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.description = description

    def __str__(self):
        return f"ID: {self.book_id}, Title: {self.title}, Author: {self.author}, Genre: {self.genre}, Description: {self.description}"

class BookNode:
    def __init__(self, book):
        self.book = book
        self.next = None

class BookManager:
    def __init__(self):
        self.books = {}
        self.head = None
        self.stack = []
        self.queue = []

    def add_book(self):
        book_id = input("Enter the Book ID: ")
        title = input("Enter the Book Title: ")
        author = input("Enter the Author: ")
        genre = input("Enter the Genre: ")
        description = input("Enter a brief description of the book: ")
        book = Book(book_id, title, author, genre, description)


        self.books[book_id] = book


        new_node = BookNode(book)
        if self.head is None:
            self.head = new_node
        else:
            current_node = self.head
            while current_node.next:
                current_node = current_node.next
            current_node.next = new_node


        self.stack.append(('add', book))
        print("Book added successfully!\n")


    def search_book(self):
        search_title = input("Enter the Book Title to search for: ")
        found_books = []
        for book in self.books.values():
            if search_title.lower() in book.title.lower():
                found_books.append(book)
        if found_books:
            for book in found_books:
                print(book)
        else:
            print("No books found with that title.\n")

    def display_books(self):
        current_node = self.head
        if not current_node:
            print("No books available.\n")
        while current_node:
            print(current_node.book)
            current_node = current_node.next

    def delete_book(self):
        book_id = input("Enter the Book ID to delete: ")
        if book_id in self.books:
            book_to_delete = self.books.pop(book_id)

            current_node = self.head
            prev_node = None
            while current_node:
                if current_node.book.book_id == book_id:
                    if prev_node:
                        prev_node.next = current_node.next
                    else:
                        self.head = current_node.next
                    break
                prev_node = current_node
                current_node = current_node.next

            self.stack.append(('delete', book_to_delete))
            print(f"Book with ID {book_id} deleted successfully!\n")
        else:
            print("Book not found.\n")

    def undo(self):
        if self.stack:
            last_action, book = self.stack.pop()
            if last_action == 'add':
                del self.books[book.book_id]
                print(f"Undone add operation: {book.title} removed.\n")
            elif last_action == 'delete':
                self.books[book.book_id] = book
                print(f"Undone delete operation: {book.title} restored.\n")
        else:
            print("No actions to undo.\n")

    def save_books(self):
        filename = "books.json"
        with open(filename, "w") as file:
            json.dump([book.__dict__ for book in self.books.values()], file)
        print("Books saved to file successfully!\n")

    def load_books(self):
        filename = "books.json"
        try:
            with open(filename, "r") as file:
                books_data = json.load(file)
                for book_data in books_data:
                    book = Book(**book_data)
                    self.books[book.book_id] = book

                    new_node = BookNode(book)
                    if not self.head:
                        self.head = new_node
                    else:
                        current_node = self.head
                        while current_node.next:
                            current_node = current_node.next
                        current_node.next = new_node
            print("Books loaded from file successfully!\n")
        except FileNotFoundError:
            print("No saved books found.\n")

    def make_enquiry(self):
        book_id = input("Enter the Book ID to enquire about: ")
        enquiry = input("Enter your question about the book: ")
        self.queue.append((book_id, enquiry))
        print(f"Enquiry added: {enquiry}\n")

    def process_enquiries(self):
        if self.queue:
            book_id, enquiry = self.queue.pop(0)
            print(f"Processing enquiry for book ID {book_id}: {enquiry}\n")
        else:
            print("No enquiries to process.\n")

def main():
    manager = BookManager()

    while True:
        print("Book Collection Manager")
        print("1. Add a new Book")
        print("2. Search for a Book")
        print("3. Display all Books")
        print("4. Delete a Book")
        print("5. Undo Last Action")
        print("6. Save Books to file")
        print("7. Load Books from file")
        print("8. Make an Enquiry about a Book")
        print("9. Process Enquiries")
        print("10. Exit")

        choice = input("Enter your choice (1-10): ")

        if choice == '1':
            manager.add_book()
        elif choice == '2':
            manager.search_book()
        elif choice == '3':
            manager.display_books()
        elif choice == '4':
            manager.delete_book()
        elif choice == '5':
            manager.undo()
        elif choice == '6':
            manager.save_books()
        elif choice == '7':
            manager.load_books()
        elif choice == '8':
            manager.make_enquiry()
        elif choice == '9':
            manager.process_enquiries()
        elif choice == '10':
            print("Thank you for using the Book Collection Manager!")
            break
        else:
            print("Invalid choice! Please select between 1 and 10.")

if __name__ == "__main__":
    main()

