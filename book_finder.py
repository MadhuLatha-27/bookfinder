import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
import io

# Open Library API URL
API_URL = "https://openlibrary.org/search.json?title={}"

class BookFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Book Finder")
        self.root.geometry("800x600")
        self.root.config(bg="#f5f5f5")

        # Heading
        heading = tk.Label(root, text="Book Finder Application", 
                           font=("Arial", 20, "bold"), bg="#f5f5f5")
        heading.pack(pady=10)

        # Search Frame
        search_frame = tk.Frame(root, bg="#f5f5f5")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Enter Book Title:", font=("Arial", 12), bg="#f5f5f5").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 12), width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        search_btn = tk.Button(search_frame, text="🔍 Search", font=("Arial", 12), 
                               bg="#4CAF50", fg="white", command=self.search_books)
        search_btn.pack(side=tk.LEFT, padx=5)

        # Results Frame
        self.results_frame = tk.Frame(root, bg="#f5f5f5")
        self.results_frame.pack(pady=10, fill="both", expand=True)

        # Scrollable Treeview
        self.tree = ttk.Treeview(self.results_frame, columns=("Title", "Author", "Year"), show="headings")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Year", text="First Published")
        self.tree.pack(fill="both", expand=True)

        # Bind double click to view cover
        self.tree.bind("<Double-1>", self.show_cover)

        # Store book data
        self.books_data = []

    def search_books(self):
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Input Error", "Please enter a book title to search.")
            return

        url = API_URL.format(query)
        try:
            response = requests.get(url)
            data = response.json()

            self.tree.delete(*self.tree.get_children())
            self.books_data = []

            if "docs" not in data or len(data["docs"]) == 0:
                messagebox.showinfo("No Results", "No books found for your search.")
                return

            for book in data["docs"][:20]:  # show top 20 results
                title = book.get("title", "N/A")
                author = ", ".join(book.get("author_name", ["Unknown"]))
                year = book.get("first_publish_year", "N/A")
                cover_id = book.get("cover_i", None)

                self.tree.insert("", tk.END, values=(title, author, year))
                self.books_data.append({"title": title, "author": author, "year": year, "cover_id": cover_id})

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data: {e}")

    def show_cover(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return
        index = self.tree.index(selected_item)
        book = self.books_data[index]

        if book["cover_id"]:
            cover_url = f"http://covers.openlibrary.org/b/id/{book['cover_id']}-L.jpg"
            response = requests.get(cover_url)
            img_data = response.content
            img = Image.open(io.BytesIO(img_data))
            img = img.resize((250, 350))
            img = ImageTk.PhotoImage(img)

            cover_window = tk.Toplevel(self.root)
            cover_window.title(book["title"])
            cover_label = tk.Label(cover_window, image=img)
            cover_label.image = img
            cover_label.pack(pady=10)

            tk.Label(cover_window, text=book["title"], font=("Arial", 14, "bold")).pack()
            tk.Label(cover_window, text=f"Author: {book['author']}").pack()
            tk.Label(cover_window, text=f"First Published: {book['year']}").pack()
        else:
            messagebox.showinfo("No Cover", "No cover image available for this book.")


if __name__ == "__main__":
    root = tk.Tk()
    app = BookFinderApp(root)
    root.mainloop()
