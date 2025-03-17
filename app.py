import streamlit as st
import json
import os

# Set page config
st.set_page_config(
    page_title="Personal Books Library Manager",
    page_icon="📚",
    layout="wide"
)

# Initialize Session State For Library Data
if 'library' not in st.session_state:
    st.session_state.library = []

# Initialize Form State
if 'form_data' not in st.session_state:
    st.session_state.form_data = {
        'title': '',
        'author': '',
        'year': '',
        'genre': '',
        'read': False
    }

data_file = 'library.txt'

def load_library():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return []

def save_library(library):
    with open(data_file, 'w') as file:
        json.dump(library, file)

# This Line Loads Library Dataa
st.session_state.library = load_library()


st.title("📚 Personal Books Library Manager")

# Sidebar for adding books
with st.sidebar:
    st.header("Add New Book")
    with st.form("add_book_form"):
        title = st.text_input("Title", value=st.session_state.form_data['title'])
        author = st.text_input("Author", value=st.session_state.form_data['author'])
        year = st.text_input("Year", value=st.session_state.form_data['year'])
        genre = st.text_input("Genre", value=st.session_state.form_data['genre'])
        read = st.checkbox("Have you read this book?", value=st.session_state.form_data['read'])
        
        if st.form_submit_button("Add Book"):
            if title and author and year and genre:
                new_book = {
                    'title': title,
                    'author': author,
                    'year': year,
                    'genre': genre,
                    'read': read
                }
                st.session_state.library.append(new_book)
                save_library(st.session_state.library)
                # Reset form data
                st.session_state.form_data = {
                    'title': '',
                    'author': '',
                    'year': '',
                    'genre': '',
                    'read': False
                }
                st.rerun()
            else:
                st.error("❌ Please fill in all required fields!")

# Main content area
tab1, tab2, tab3 = st.tabs(["Library", "Search", "Statistics"])

# Library Tab
with tab1:
    st.header("Your Library")
    if st.session_state.library:
        for book in st.session_state.library:
            with st.expander(f"{book['title']} by {book['author']}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Year:** {book['year']}")
                    st.write(f"**Genre:** {book['genre']}")
                    st.write(f"**Status:** {'Read' if book['read'] else 'Unread'}")
                with col2:
                    if st.button("Remove", key=f"remove_{book['title']}"):
                        st.session_state.library = [b for b in st.session_state.library if b != book]
                        save_library(st.session_state.library)
                        st.rerun()
    else:
        st.info("Your Library Is Empty. Please Add Some Books!")

# Search Tab
with tab2:
    st.header("Search Library")
    search_by = st.selectbox("Search by:", ["Title", "Author"])
    search_term = st.text_input(f"Enter the {search_by}:")
    
    if search_term:
        results = [book for book in st.session_state.library 
                  if search_term.lower() in book[search_by].lower()]
        
        if results:
            for book in results:
                with st.expander(f"{book['title']} by {book['author']}"):
                    st.write(f"**Year:** {book['year']}")
                    st.write(f"**Genre:** {book['genre']}")
                    st.write(f"**Status:** {'Read' if book['read'] else 'Unread'}")
        else:
            st.info(f"No books found matching '{search_term}' in the {search_by} field.")

# Statistics Tab
with tab3:
    st.header("Library Statistics")
    total_books = len(st.session_state.library)
    read_books = len([book for book in st.session_state.library if book['read']])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Books", total_books)
    with col2:
        st.metric("Books Read", read_books)
    with col3:
        st.metric("Reading Progress", f"{percentage_read:.1f}%")

# Footer
st.markdown("---")  

st.markdown("© 2024 All Rights Reserved - Created by Rahim Ali")

