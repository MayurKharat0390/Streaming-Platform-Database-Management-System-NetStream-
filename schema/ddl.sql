-- Streaming Platform DBMS Schema (3NF)
-- Database: streaming_db

CREATE DATABASE IF NOT EXISTS streaming_db;
USE streaming_db;

-- 1. Genres Table
CREATE TABLE IF NOT EXISTS Genres (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    genre_name VARCHAR(50) NOT NULL UNIQUE
);

-- 2. Subscriptions Table (Plans)
CREATE TABLE IF NOT EXISTS Subscriptions (
    plan_id INT AUTO_INCREMENT PRIMARY KEY,
    plan_name VARCHAR(50) NOT NULL UNIQUE,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    duration_months INT NOT NULL CHECK (duration_months > 0)
);

-- 3. Users Table
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. User_Subscriptions (Junction Table for Users and Plans)
CREATE TABLE IF NOT EXISTS User_Subscriptions (
    sub_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    plan_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status ENUM('Active', 'Expired', 'Cancelled') DEFAULT 'Active',
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (plan_id) REFERENCES Subscriptions(plan_id) ON DELETE CASCADE,
    CONSTRAINT chk_dates CHECK (end_date >= start_date)
);

-- 5. Content Table (Movies and Series)
CREATE TABLE IF NOT EXISTS Content (
    content_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content_type ENUM('Movie', 'Series') NOT NULL,
    release_year INT CHECK (release_year >= 1888),
    duration_min INT CHECK (duration_min > 0),
    director VARCHAR(100),
    description TEXT
);

-- 6. Content_Genre (Junction Table for Content and Genres)
CREATE TABLE IF NOT EXISTS Content_Genre (
    content_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (content_id, genre_id),
    FOREIGN KEY (content_id) REFERENCES Content(content_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES Genres(genre_id) ON DELETE CASCADE
);

-- 7. Watch_History Table
CREATE TABLE IF NOT EXISTS Watch_History (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    content_id INT NOT NULL,
    watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (content_id) REFERENCES Content(content_id) ON DELETE CASCADE
);

-- 8. Ratings Table
CREATE TABLE IF NOT EXISTS Ratings (
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    content_id INT NOT NULL,
    rating TINYINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review TEXT,
    rated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, content_id), -- One rating per user per content
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (content_id) REFERENCES Content(content_id) ON DELETE CASCADE
);
