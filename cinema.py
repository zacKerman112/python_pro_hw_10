import sqlite3
from datetime import datetime

conn = sqlite3.connect("cinema.db")
conn.execute("PRAGMA foreign_keys = ON;")
conn.create_function("movie_age", 1, lambda year: datetime.now().year - year)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS movies(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    release_year INTEGER,
                    genre TEXT
                    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS actors(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    birth_year INTEGER
                    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS movie_cast (
                    movie_id INTEGER,
                    actor_id INTEGER,
                    PRIMARY KEY (movie_id, actor_id),
                    FOREIGN KEY (movie_id) REFERENCES movies (id),
                    FOREIGN KEY (actor_id) REFERENCES actors (id)
                )""")


def add_movie():
    """a function for adding movies"""
    title = input("Enter movie title: ")
    year = int(input("Enter release year: "))
    genre = input("Enter genre: ")
    cursor.execute("INSERT INTO movies (title, release_year, genre) VALUES (?, ?, ?)",
                   (title, year, genre))
    conn.commit()
    print(f"Movie '{title}' has been added.")


def add_actor():
    """a function for adding actors"""
    name = input("Enter actor name: ")
    year = int(input("Enter birth year: "))
    cursor.execute("INSERT INTO actors (name, birth_year) VALUES (?, ?)",
                   (name, year))
    conn.commit()
    print(f"Actor '{name}' has been added.")


def get_movies_with_actors():
    """function for showing movies with actors"""
    query = """
    SELECT movies.title, actors.name
    FROM movies
    JOIN movie_cast ON movies.id = movie_cast.movie_id
    JOIN actors ON movie_cast.actor_id = actors.id
    """
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(f'Movie: {row[0]} | Actor: {row[1]}')


def get_unique_genres():
    """a function for getting unique genres"""
    query = """SELECT DISTINCT genre FROM movies"""
    cursor.execute(query)
    genres = [row[0] for row in cursor.fetchall()]
    for g in genres:
        print(f"Genre: {g}")


def count_genre_amount():
    """function for counting genres"""
    query = """SELECT genre, COUNT(id) FROM movies GROUP BY genre"""
    cursor.execute(query)
    for genre, count in cursor.fetchall():
        print(f"Genre: {genre} | Amount: {count}")


def get_avg_year_by_genre():
    """getting average year by genre"""
    genre_name = input("Enter genre: ")
    query = """SELECT AVG(actors.birth_year)
    FROM actors
    JOIN movie_cast ON actors.id = movie_cast.actor_id
    JOIN movies ON movie_cast.movie_id = movies.id
    WHERE movies.genre = ?
    """
    cursor.execute(query, (genre_name,))
    result = cursor.fetchone()[0]
    print(f"Average birth year: {round(result, 1) if result else 0.0}")


def movie_name_matches():
    """checking is name matches the searched name"""
    name = input("Enter movie name to search: ")
    query = "SELECT title FROM movies WHERE title LIKE ?"
    cursor.execute(query, (f"%{name}%",))
    results = cursor.fetchall()
    if not results:
        print("Not found.")
    else:
        for row in results:
            print(f"Found: {row[0]}")


def get_data_paged():
    """getting paged data"""
    page = int(input("Enter page number: "))
    per_page = int(input("Items per page: "))
    skip = (page - 1) * per_page
    cursor.execute("SELECT * FROM movies LIMIT ? OFFSET ?", (per_page, skip))
    for row in cursor.fetchall():
        print(row)


def get_all_the_names_and_ages():
    """getting ages of movies by names of names"""
    cursor.execute("SELECT title, movie_age(release_year) FROM movies")
    for title, age in cursor.fetchall():
        print(f"Movie: {title} | Age: {age}")

    cursor.execute("SELECT name FROM actors UNION SELECT title FROM movies ORDER BY name")
    print("\n--- Union List ---")
    for row in cursor.fetchall():
        print(row[0])


def console_interface():
    """a min console interface"""
    while True:
        print("\n" + "=" * 15 + " MENU " + "=" * 15)
        print("1: Add movie\n2: Add actor\n3: Show movies with actors\n4: Show unique genres")
        print("5: Show genre counts\n6: Avg birth year by genre\n7: Search movie")
        print("8: Show movies (paged)\n9: Show names/ages & Union\n0: EXIT")

        answer = input("ENTER: ")

        if answer == "1":
            add_movie()
        elif answer == "2":
            add_actor()
        elif answer == "3":
            get_movies_with_actors()
        elif answer == "4":
            get_unique_genres()
        elif answer == "5":
            count_genre_amount()
        elif answer == "6":
            get_avg_year_by_genre()
        elif answer == "7":
            movie_name_matches()
        elif answer == "8":
            get_data_paged()
        elif answer == "9":
            get_all_the_names_and_ages()
        elif answer == "0":
            break
        else:
            print("WRONG OPTION")


if __name__ == "__main__":
    console_interface()
    conn.close()