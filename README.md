# NetStream DBMS (Streaming Platform Management)

A comprehensive Database Management System project built using Python, Streamlit, and MySQL. This project demonstrates advanced database concepts including ER modeling, 3NF normalization, constraints, and complex SQL joins.

## 🚀 How to Run

### 1. Prerequisites
- Install **MySQL Server** (XAMPP/WAMP or Standalone).
- Ensure Python 3.8+ is installed.

### 2. Setup Database
- Open MySQL Workbench or any SQL client.
- Create a database: `CREATE DATABASE streaming_db;`
- (Note: The app will attempt to create the tables automatically on the first run).

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
cd src
streamlit run app.py
```

---

## 📂 Project Structure
- `schema/ddl.sql`: Full table definitions with constraints (PK, FK, CHECK, UNIQUE).
- `schema/dummy_data.sql`: Initial records for demonstration.
- `src/database.py`: MySQL connection handler.
- `src/queries.py`: Repository of 15+ SQL queries used in the app.
- `src/app.py`: Streamlit frontend with 7 specialized modules.

---

## 🛠️ Database Concepts Demonstrated

### 1. Normalization (3NF)
The database is split into 8 tables to eliminate redundancy and improve data integrity:
- `Users`, `Subscriptions`, `User_Subscriptions`
- `Content`, `Genres`, `Content_Genre`
- `Watch_History`, `Ratings`

### 2. Constraints
- **Primary Keys**: Every table has a unique ID.
- **Foreign Keys**: Enforced referential integrity (e.g., `user_id` in `Ratings` links to `Users`).
- **Check Constraints**: `rating` is between 1-5, `price` is >= 0.
- **Unique**: Usernames and Emails are unique.

### 3. Key SQL Queries (Total 15+)
1. `SELECT * FROM Users`: Fetch all user records.
2. `INSERT INTO Users`: Create new user accounts.
3. `UPDATE User_Subscriptions`: Change status of plans.
4. `DELETE FROM Users`: Remove user and their data (CASCADE).
5. `SELECT COUNT(*)`: Aggregate count for dashboard.
6. `AVG(rating) + GROUP BY`: Calculate mean rating for each movie.
7. `JOIN (Content + Genres)`: Fetch content with its linked categories.
8. `JOIN (Watch_History + Users + Content)`: See who watched what.
9. `BAR CHART Aggregation`: Count views per genre.
10. `LIKE '%keyword%'`: Partial search for movies/directors.
11. `ON DUPLICATE KEY UPDATE`: Upsert ratings.
12. `ORDER BY ... DESC`: Find most recently watched movies.
13. `LIMIT`: Show top 5 rated content.
14. `HAVING COUNT(*) > 0`: Filter content with at least one rating.
15. `INNER JOIN`: Link subscriptions to user profiles.

---

## 📺 Application Modules
1. **Dashboard**: Metrics for Users, Content, and Popular Genres.
2. **User Management**: Add, View, and Delete users.
3. **Subscriptions**: Assign plans and track status.
4. **Content Management**: Upload and search movies/series.
5. **Genre Management**: Categorize content.
6. **Watch History**: Detailed logs of user activity.
7. **Ratings**: User feedback and average scores.
