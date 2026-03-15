from database import execute_query

# --- DASHBOARD QUERIES ---

def get_total_users():
    query = "SELECT COUNT(*) as count FROM Users"
    result = execute_query(query, fetch=True)
    return result[0]['count'] if result else 0

def get_total_content():
    query = "SELECT COUNT(*) as count FROM Content"
    result = execute_query(query, fetch=True)
    return result[0]['count'] if result else 0

def get_top_rated_content():
    """Example of JOIN, AVG, GROUP BY, ORDER BY"""
    query = """
    SELECT c.title, AVG(r.rating) as avg_rating, COUNT(r.rating_id) as total_ratings
    FROM Content c
    LEFT JOIN Ratings r ON c.content_id = r.content_id
    GROUP BY c.content_id
    HAVING total_ratings > 0
    ORDER BY avg_rating DESC
    LIMIT 5
    """
    return execute_query(query, fetch=True)

def get_popular_genres():
    """Example of Multiple JOINs and Aggregation"""
    query = """
    SELECT g.genre_name, COUNT(wh.history_id) as views
    FROM Genres g
    JOIN Content_Genre cg ON g.genre_id = cg.genre_id
    JOIN Watch_History wh ON cg.content_id = wh.content_id
    GROUP BY g.genre_id
    ORDER BY views DESC
    """
    return execute_query(query, fetch=True)

# --- USER MANAGEMENT ---

def add_user(username, email, password):
    query = "INSERT INTO Users (username, email, password) VALUES (%s, %s, %s)"
    return execute_query(query, (username, email, password))

def get_all_users():
    return execute_query("SELECT user_id, username, email, created_at FROM Users", fetch=True)

def delete_user(user_id):
    return execute_query("DELETE FROM Users WHERE user_id = %s", (user_id,))

# --- CONTENT MANAGEMENT ---

def add_content(title, content_type, release_year, duration, director, description):
    query = """
    INSERT INTO Content (title, content_type, release_year, duration_min, director, description)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    return execute_query(query, (title, content_type, release_year, duration, director, description))

def get_all_content():
    query = """
    SELECT c.*, GROUP_CONCAT(g.genre_name SEPARATOR ', ') as genres
    FROM Content c
    LEFT JOIN Content_Genre cg ON c.content_id = cg.content_id
    LEFT JOIN Genres g ON cg.genre_id = g.genre_id
    GROUP BY c.content_id
    """
    return execute_query(query, fetch=True)

def search_content(keyword):
    query = "SELECT * FROM Content WHERE title LIKE %s OR director LIKE %s"
    return execute_query(query, (f"%{keyword}%", f"%{keyword}%"), fetch=True)

# --- GENRE MANAGEMENT ---

def add_genre(name):
    return execute_query("INSERT INTO Genres (genre_name) VALUES (%s)", (name,))

def get_genres():
    return execute_query("SELECT * FROM Genres", fetch=True)

def link_content_genre(content_id, genre_id):
    query = "INSERT IGNORE INTO Content_Genre (content_id, genre_id) VALUES (%s, %s)"
    return execute_query(query, (content_id, genre_id))

# --- SUBSCRIPTION MANAGEMENT ---

def add_plan(name, price, duration):
    query = "INSERT INTO Subscriptions (plan_name, price, duration_months) VALUES (%s, %s, %s)"
    return execute_query(query, (name, price, duration))

def get_all_plans():
    return execute_query("SELECT * FROM Subscriptions", fetch=True)

def assign_subscription(user_id, plan_id, start_date, end_date):
    query = """
    INSERT INTO User_Subscriptions (user_id, plan_id, start_date, end_date, status)
    VALUES (%s, %s, %s, %s, 'Active')
    """
    return execute_query(query, (user_id, plan_id, start_date, end_date))

def get_user_subscriptions():
    query = """
    SELECT us.sub_id, u.username, s.plan_name, us.start_date, us.end_date, us.status
    FROM User_Subscriptions us
    JOIN Users u ON us.user_id = u.user_id
    JOIN Subscriptions s ON us.plan_id = s.plan_id
    """
    return execute_query(query, fetch=True)

# --- WATCH HISTORY & RATINGS ---

def add_watch_history(user_id, content_id):
    query = "INSERT INTO Watch_History (user_id, content_id) VALUES (%s, %s)"
    return execute_query(query, (user_id, content_id))

def get_watch_history():
    query = """
    SELECT wh.history_id, u.username, c.title, wh.watched_at
    FROM Watch_History wh
    JOIN Users u ON wh.user_id = u.user_id
    JOIN Content c ON wh.content_id = c.content_id
    ORDER BY wh.watched_at DESC
    """
    return execute_query(query, fetch=True)

def add_rating(user_id, content_id, rating, review):
    query = """
    INSERT INTO Ratings (user_id, content_id, rating, review)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE rating = VALUES(rating), review = VALUES(review)
    """
    return execute_query(query, (user_id, content_id, rating, review))

def get_ratings_with_details():
    query = """
    SELECT r.rating_id, u.username, c.title, r.rating, r.review, r.rated_at
    FROM Ratings r
    JOIN Users u ON r.user_id = u.user_id
    JOIN Content c ON r.content_id = c.content_id
    """
    return execute_query(query, fetch=True)
