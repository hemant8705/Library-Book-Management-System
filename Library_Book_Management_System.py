# --- Book node for the singly linked list ---
class Book:
    def __init__(self, book_id, title, author, status="Available"):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.status = status
        self.next = None

# --- Singly linked list for books management ---
class LinkedList:
    def __init__(self):
        self.head = None

    def insertBook(self, book_id, title, author):
        new_book = Book(book_id, title, author)
        new_book.next = self.head
        self.head = new_book
        print(f"Book '{title}' added.")

    def deleteBook(self, book_id):
        current = self.head
        prev = None
        while current:
            if current.book_id == book_id:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                print(f"Book '{current.title}' deleted.")
                return current  # Return deleted book for undo
            prev = current
            current = current.next
        print("Book not found.")
        return None

    def searchBook(self, book_id):
        current = self.head
        while current:
            if current.book_id == book_id:
                return current
            current = current.next
        return None

    def displayBooks(self):
        books = []
        current = self.head
        while current:
            books.append((current.book_id, current.title, current.author, current.status))
            current = current.next
        return books

# --- Stack class for undo functionality ---
class Stack:
    def __init__(self):
        self.stack = []

    def push(self, data):
        self.stack.append(data)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        return None

    def is_empty(self):
        return len(self.stack) == 0

    def viewTransactions(self):
        return self.stack[::-1]

# --- Library System integrating list and stack ---
class LibrarySystem:
    def __init__(self):
        self.book_list = LinkedList()
        self.trans_stack = Stack()

    def insertBook(self, book_id, title, author):
        self.book_list.insertBook(book_id, title, author)

    def deleteBook(self, book_id):
        book = self.book_list.deleteBook(book_id)
        if book:
            self.trans_stack.push(("delete", book.book_id, book.title, book.author, book.status))

    def searchBook(self, book_id):
        book = self.book_list.searchBook(book_id)
        if book:
            return (book.book_id, book.title, book.author, book.status)
        return None

    def displayBooks(self):
        return self.book_list.displayBooks()

    def issueBook(self, book_id):
        book = self.book_list.searchBook(book_id)
        if book and book.status == "Available":
            book.status = "Issued"
            self.trans_stack.push(("issue", book_id))
            print(f"Book '{book.title}' issued.")
        else:
            print("Book not available for issue.")

    def returnBook(self, book_id):
        book = self.book_list.searchBook(book_id)
        if book and book.status == "Issued":
            book.status = "Available"
            self.trans_stack.push(("return", book_id))
            print(f"Book '{book.title}' returned.")
        else:
            print("Book not currently issued.")

    def undoTransaction(self):
        last_action = self.trans_stack.pop()
        if not last_action:
            print("No transactions to undo.")
            return

        action = last_action[0]
        if action == "issue":
            book_id = last_action[1]
            book = self.book_list.searchBook(book_id)
            if book:
                book.status = "Available"
                print(f"Undo: Book '{book.title}' status set to Available.")
        elif action == "return":
            book_id = last_action[1]
            book = self.book_list.searchBook(book_id)
            if book:
                book.status = "Issued"
                print(f"Undo: Book '{book.title}' status set to Issued.")
        elif action == "delete":
            _, book_id, title, author, status = last_action
            self.book_list.insertBook(book_id, title, author)
            inserted_book = self.book_list.searchBook(book_id)
            if inserted_book:
                inserted_book.status = status
            print(f"Undo: Book '{title}' restored.")

    def viewTransactions(self):
        return self.trans_stack.viewTransactions()

# --- Sample usage ---
if __name__ == "__main__":
    ls = LibrarySystem()
    ls.insertBook(1, "DSA Fundamentals", "Alice")
    ls.insertBook(2, "Python Basics", "Bob")
    ls.insertBook(3, "Algorithms", "Carol")
    print("Initial books:", ls.displayBooks())

    ls.issueBook(2)
    ls.returnBook(2)
    ls.deleteBook(3)
    print("Books after operations:", ls.displayBooks())

    ls.undoTransaction()  # Undo delete
    ls.undoTransaction()  # Undo return
    print("Books after undo:", ls.displayBooks())
    print("Transactions:", ls.viewTransactions())
