
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


# ---------------- DATABASE ----------------

def createDatabase():
    conn = sqlite3.connect("movieTracker.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Movies (
            movieID INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            genre TEXT NOT NULL,
            yearReleased INTEGER NOT NULL,
            rating INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ---------------- RETRIEVE DATA ----------------

def loadData():
    for item in movieTree.get_children():
        movieTree.delete(item)

    conn = sqlite3.connect("movieTracker.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM Movies
        ORDER BY title ASC
    """)

    records = cursor.fetchall()

    for record in records:
        movieTree.insert("", tk.END, values=record)

    conn.close()


# ---------------- ADD MOVIE OR TV SHOW ----------------

def addMovie():

    title = titleEntry.get().strip()
    showType = typeCombo.get()
    genre = genreEntry.get().strip()
    year = yearEntry.get().strip()
    rating = ratingCombo.get()

    # Validation

    if title == "" or genre == "" or year == "" or rating == "":
        messagebox.showerror(
            "Error",
            "Please complete all fields."
        )
        return

    if showType == "":
        messagebox.showerror(
            "Error",
            "Please select Movie or TV Show."
        )
        return

    if not year.isdigit():
        messagebox.showerror(
            "Error",
            "Please enter a valid year."
        )
        return

    year = int(year)

    currentYear = datetime.now().year

    if year < 1888 or year > currentYear:
        messagebox.showerror(
            "Error",
            "Please enter a valid release year."
        )
        return

    rating = int(rating)

    if rating < 1 or rating > 5:
        messagebox.showerror(
            "Error",
            "Rating must be between 1 and 5."
        )
        return

    # Insert record into database

    conn = sqlite3.connect("movieTracker.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Movies
        (title, type, genre, yearReleased, rating)
        VALUES (?, ?, ?, ?, ?)
    """, (title, showType, genre, year, rating))

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        "Movie or TV show added successfully."
    )

    # Clear input fields

    titleEntry.delete(0, tk.END)
    typeCombo.set("")
    genreEntry.delete(0, tk.END)
    yearEntry.delete(0, tk.END)
    ratingCombo.set("")

    loadData()


# ---------------- SORT DATA ----------------

def sortData():

    for item in movieTree.get_children():
        movieTree.delete(item)

    conn = sqlite3.connect("movieTracker.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM Movies
        ORDER BY title ASC
    """)

    records = cursor.fetchall()

    for record in records:
        movieTree.insert("", tk.END, values=record)

    conn.close()


# ---------------- SEARCH BY GENRE ----------------

def searchGenre():

    searchValue = genreSearchEntry.get().strip()

    if searchValue == "":
        messagebox.showerror(
            "Error",
            "Please enter a genre to search."
        )
        return

    for item in movieTree.get_children():
        movieTree.delete(item)

    conn = sqlite3.connect("movieTracker.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM Movies
        WHERE genre LIKE ?
        ORDER BY title ASC
    """, ('%' + searchValue + '%',))

    records = cursor.fetchall()

    for record in records:
        movieTree.insert("", tk.END, values=record)

    conn.close()

    if len(records) == 0:
        messagebox.showinfo(
            "Search",
            "No movies or TV shows found."
        )


# ---------------- VIEW ALL RECORDS ----------------

def viewAll():

    genreSearchEntry.delete(0, tk.END)

    loadData()


# ---------------- GUI ----------------

createDatabase()

root = tk.Tk()

root.title("Movie & TV Show Tracker")
root.geometry("1000x650")

# Colours

backgroundColour = "#FCE4EC"
buttonColour = "#F8BBD0"
textColour = "#4A3040"

root.configure(bg=backgroundColour)


# ---------------- TITLE ----------------

heading = tk.Label(
    root,
    text="Movie & TV Show Tracker",
    font=("Arial", 22, "bold"),
    bg=backgroundColour,
    fg=textColour
)

heading.pack(pady=15)


# ---------------- INPUT FRAME ----------------

inputFrame = tk.Frame(
    root,
    bg=backgroundColour
)

inputFrame.pack(pady=10)


# Title

tk.Label(
    inputFrame,
    text="Title:",
    bg=backgroundColour,
    fg=textColour
).grid(row=0, column=0, padx=10, pady=5)

titleEntry = tk.Entry(
    inputFrame,
    width=25
)

titleEntry.grid(row=0, column=1, padx=10, pady=5)


# Type

tk.Label(
    inputFrame,
    text="Type:",
    bg=backgroundColour,
    fg=textColour
).grid(row=0, column=2, padx=10, pady=5)

typeCombo = ttk.Combobox(
    inputFrame,
    values=["Movie", "TV Show"],
    state="readonly",
    width=22
)

typeCombo.grid(row=0, column=3, padx=10, pady=5)


# Genre

tk.Label(
    inputFrame,
    text="Genre:",
    bg=backgroundColour,
    fg=textColour
).grid(row=1, column=0, padx=10, pady=5)

genreEntry = tk.Entry(
    inputFrame,
    width=25
)

genreEntry.grid(row=1, column=1, padx=10, pady=5)


# Year Released

tk.Label(
    inputFrame,
    text="Year Released:",
    bg=backgroundColour,
    fg=textColour
).grid(row=1, column=2, padx=10, pady=5)

yearEntry = tk.Entry(
    inputFrame,
    width=25
)

yearEntry.grid(row=1, column=3, padx=10, pady=5)


# Rating

tk.Label(
    inputFrame,
    text="Rating (1-5):",
    bg=backgroundColour,
    fg=textColour
).grid(row=2, column=0, padx=10, pady=5)

ratingCombo = ttk.Combobox(
    inputFrame,
    values=["1", "2", "3", "4", "5"],
    state="readonly",
    width=22
)

ratingCombo.grid(row=2, column=1, padx=10, pady=5)


# ---------------- BUTTONS ----------------

buttonFrame = tk.Frame(
    root,
    bg=backgroundColour
)

buttonFrame.pack(pady=15)


def createButton(text, command):

    return tk.Button(
        buttonFrame,
        text=text,
        command=command,
        bg=buttonColour,
        fg=textColour,
        activebackground="#F48FB1",
        font=("Arial", 10, "bold"),
        width=16,
        relief="flat"
    )


createButton(
    "Add Movie / TV Show",
    addMovie
).grid(row=0, column=0, padx=5, pady=5)

createButton(
    "Sort A-Z",
    sortData
).grid(row=0, column=1, padx=5, pady=5)

createButton(
    "View All",
    viewAll
).grid(row=0, column=2, padx=5, pady=5)


# ---------------- SEARCH FRAME ----------------

searchFrame = tk.Frame(
    root,
    bg=backgroundColour
)

searchFrame.pack(pady=10)

tk.Label(
    searchFrame,
    text="Search by Genre:",
    bg=backgroundColour,
    fg=textColour
).grid(row=0, column=0, padx=5)

genreSearchEntry = tk.Entry(
    searchFrame,
    width=25
)

genreSearchEntry.grid(
    row=0,
    column=1,
    padx=5
)

tk.Button(
    searchFrame,
    text="Search",
    command=searchGenre,
    bg=buttonColour,
    fg=textColour,
    relief="flat"
).grid(row=0, column=2, padx=5)


# ---------------- DISPLAY TABLE ----------------

tableFrame = tk.Frame(
    root,
    bg=backgroundColour
)

tableFrame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=15
)

columns = (
    "ID",
    "Title",
    "Type",
    "Genre",
    "Year Released",
    "Rating"
)

movieTree = ttk.Treeview(
    tableFrame,
    columns=columns,
    show="headings"
)

for column in columns:

    movieTree.heading(
        column,
        text=column
    )

    movieTree.column(
        column,
        anchor="center",
        width=140
    )

movieTree.pack(
    fill="both",
    expand=True
)


# ---------------- START PROGRAM ----------------

loadData()

root.mainloop()
