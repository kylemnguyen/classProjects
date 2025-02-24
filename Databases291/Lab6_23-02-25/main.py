import sqlite3
import hashlib

# ---------- Set up database

def setup_db():
    """ 
    Creates the movies and users tables.
    """
    global connection, cursor

    # Connect to SQLite database
    connection = sqlite3.connect("movies.db")
    cursor = connection.cursor()

    # Drop tables if they exist (removes all data)
    cursor.execute("DROP TABLE IF EXISTS movies;")
    cursor.execute("DROP TABLE IF EXISTS users;")

    # Create the 'movies' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        title TEXT,
        id INTEGER PRIMARY KEY,
        year INTEGER,
        budget INTEGER
    );
    """)

    # Create the 'users' table for login testing
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    );
    """)

    # Insert some test users 
    cursor.execute("INSERT INTO users VALUES ('admin', 'securepassword');")
    cursor.execute("INSERT INTO users VALUES ('user1', 'password123');")

    connection.commit()


# ---------- Functions to be implemented


def insert_movies(): 
    """ Inserts values into the movies table. """
    global connection, cursor

    movie_values = [
        ("Spiderman 2", 1, 2002, 200),
        ("The Dark Knight", 2, 2010, 160),
        ("Zootopia", 3, 2018, 208)
    ]

    # TODO: Implement SQL query to insert movie_values into movies
    # KYLEMNGUYEN'S CODE
    ####################### - KYLEMNGUYEN CODE
    
    cursor.executemany(
        "INSERT INTO movies VALUES (?, ?, ?, ?)",
        movie_values,
    )
    
    
    #######################
    
    connection.commit()

def insert_movie_rollback(): 
    """ Inserts a movie but rolls back to undo the change. """

    global connection, cursor
    cursor.execute("INSERT INTO movies VALUES('Test Movie', 4, 2023, 50);") 

    # TODO: Implement rollback to undo this insert before the commit
    ####################### - KYLEMNGUYEN CODE
    
    connection.rollback()
    
    #######################
    connection.commit()

    

def login_secure(username, password):
    """
    Secure login function that prevents SQL injection.
    The current implementation is wrong, you must change this to stop the attack.
    Returns: Boolean value 
    """
    global cursor

    # TODO: Modify the query below to prevent SQL injection.

    # WARNING: This is vulnerable to SQL injection
    ####################### - KYLEMNGUYEN CODE
    
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}';"
    print("[DEBUG] Executing query:", query)  # To show SQL Injection
    cursor.execute(
        'SELECT * FROM users WHERE username = :uname AND password = :pw;',
        { 'uname': username, 'pw': password },
    )
    ####################### - KYLEMNGUYEN CODE

    result = cursor.fetchone()

    return result is not None

def subtract_numbers(a,b): 
    """ Returns the difference of numbers a and b (a - b). """
    # TODO: Implement the return statement to be used in year_budget_difference
    ####################### - KYLEMNGUYEN CODE
    return a - b
    
def year_budget_difference():
    """ Returns movies where (year - budget) > 1849. """
    global cursor, connection
    connection.create_function('subtract', 2, subtract_numbers)
    
    #TODO: Write a SQL query using the user-defined function 'subtract' to filter results.
    ####################### - KYLEMNGUYEN CODE
    
    cursor.execute("""
        SELECT * FROM movies WHERE
        subtract(movies.year, movies.budget) > 1849;               
    """)
    ####################### - KYLEMNGUYEN CODE
    
    
    return cursor.fetchone() 

# OPTIONAL TASKS

def hash_password(password):
    """ Returns the hashed password using SHA-256. """

    # TODO: Implement password hashing using SHA-256 and return the hashed value.
    ####################### - KYLEMNGUYEN CODE
    alg = hashlib.sha256()
    alg.update(password.encode('utf-8'))
    return alg.hexdigest()

    
    
    



def insert_user_hashed_password():
    hashed_pw = hash_password("securepassword123")
    try: 
        # TODO: Fix the bug in this query, use the exception error as a hint.
        # Query goal: Insert a new user 'user2' with password as hashed_pw into the users table
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?);", ("user2", hashed_pw))
    except sqlite3.Error as e: 
        print(e)
    connection.commit()


# ---------- Run main 


if __name__ == "__main__":
    setup_db()
    insert_movies()

    # Demonstrate insert_movies()
    print("\n--- Testing insert_movies ---")

    query = "SELECT * FROM movies"
    cursor.execute(query)
    result = cursor.fetchall() 
    print("Database:",result) 

    if result: 
        print("[✓] insert_movies() passed! Great job!")
    else: 
        raise Exception("[✖] insert_movies() failed. Try again!")


    # Demonstrate rollback
    print("\n--- Testing insert_movie_rollback ---")
    insert_movie_rollback() 
    query = "SELECT * FROM movies WHERE id = 4"
    cursor.execute(query)
    result = cursor.fetchone() 

    if result: 
        raise Exception("[✖] insert_movie_rollback() failed. Try again!")
    else: 
        print("[✓] insert_movie_rollback() passed! Great job!")

    query = "SELECT * FROM movies"
    cursor.execute(query)
    result = cursor.fetchall() 
    print("Database:",result) 

    # Demonstrate SQL Injection
    print("\n--- Testing login_secure ---")
    user_input_username = "admin"
    user_input_password = "' OR '1'='1"  # Classic SQL Injection payload


    print("Trying to log in...")
    if login_secure(user_input_username, user_input_password):
        raise Exception("[✖] login_secure() failed. Try again!")
    else:
        print("[✓] login_secure() passed! Great job!")

    query = "SELECT * FROM users"
    cursor.execute(query)
    result = cursor.fetchall() 
    print("User Database:",result) 


    # Demonstrate User function 
    print("\n--- Testing year_budget_difference ---")
    result = year_budget_difference() 

    if result == None: 
        raise Exception("[✖] year_budget_difference failed. Did you implement subtract_numbers?")
            
    elif result[1] == 2: 
        print("[✓] year_budget_difference() passed! Great job!")

    else:
        raise Exception("[✖] year_budget_difference failed. Try again!")
    
    print("Result from query:", result)
    
    # Demonstrate hashing. Uncomment if you want to test the functions. 
    print("\n--- OPTIONAL: Testing hash_password ---")
    insert_user_hashed_password() 
    query = "SELECT password FROM users WHERE username = 'user2' "
    cursor.execute(query)
    result = cursor.fetchone()
    print("Hashed password:", result[0])
        
    # Close connection
    connection.close()
