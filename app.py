import streamlit as st
import requests

# Open Library API
API_URL = "https://openlibrary.org/search.json?title={}"

st.set_page_config(page_title="📚 Book Finder", layout="wide")

st.title("📚 Book Finder Application")

query = st.text_input("Enter Book Title")

if st.button("🔍 Search"):
    if not query:
        st.warning("Please enter a book title to search.")
    else:
        url = API_URL.format(query)
        try:
            response = requests.get(url)
            data = response.json()

            if "docs" not in data or len(data["docs"]) == 0:
                st.info("No books found for your search.")
            else:
                for book in data["docs"][:20]:
                    title = book.get("title", "N/A")
                    author = ", ".join(book.get("author_name", ["Unknown"]))
                    year = book.get("first_publish_year", "N/A")

                    st.markdown(f"### {title}")
                    st.write(f"**Author(s):** {author}")
                    st.write(f"**First Published:** {year}")

                    # Book cover (if available)
                    cover_id = book.get("cover_i", None)
                    if cover_id:
                        cover_url = f"http://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                        st.image(cover_url, width=150)
                    st.divider()

        except Exception as e:
            st.error(f"Failed to fetch data: {e}")
