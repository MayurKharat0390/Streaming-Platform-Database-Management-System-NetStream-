-- Dummy Data for Streaming Platform
USE streaming_db;

-- Insert Genres
INSERT INTO Genres (genre_name) VALUES 
('Sci-Fi'), ('Action'), ('Drama'), ('Comedy'), ('Horror'), ('Documentary');

-- Insert Subscription Plans
INSERT INTO Subscriptions (plan_name, price, duration_months) VALUES 
('Basic', 9.99, 1),
('Standard', 15.99, 1),
('Premium', 19.99, 1),
('Annual Basic', 99.99, 12);

-- Insert Users
INSERT INTO Users (username, email, password) VALUES 
('john_doe', 'john@example.com', 'hashed_pw_1'),
('jane_smith', 'jane@example.com', 'hashed_pw_2'),
('bob_builder', 'bob@example.com', 'hashed_pw_3'),
('alice_wonder', 'alice@example.com', 'hashed_pw_4');

-- Insert Content (Faculty Safe / Educational / Sci-Fi)
INSERT INTO Content (title, content_type, release_year, duration_min, director, description) VALUES 
('Cosmos: A Spacetime Odyssey', 'Series', 2014, 45, 'Brannon Braga', 'An exploration of how we discovered the laws of nature and found our coordinates in space and time.'),
('Apollo 11', 'Movie', 2019, 93, 'Todd Douglas Miller', 'A look at the Apollo 11 mission to land on the moon led by commander Neil Armstrong.'),
('The Imitation Game', 'Movie', 2014, 114, 'Morten Tyldum', 'Based on the real life story of legendary cryptanalyst Alan Turing during World War II.'),
('Blue Planet II', 'Series', 2017, 60, 'James Honeyborne', 'Sir David Attenborough returns to the ocean to explore the latest discoveries in marine life.'),
('Hidden Figures', 'Movie', 2016, 127, 'Theodore Melfi', 'The story of a team of female African-American mathematicians who served a vital role in NASA.');

-- Link Content to Genres
INSERT INTO Content_Genre (content_id, genre_id) VALUES 
(1, 6), (1, 1), -- Cosmos: Documentary, Sci-Fi
(2, 6), (2, 3), -- Apollo 11: Documentary, Drama
(3, 3), (3, 2), -- Imitation Game: Drama, Action
(4, 6),         -- Blue Planet: Documentary
(5, 3), (5, 6); -- Hidden Figures: Drama, Documentary

-- Assign Subscriptions
INSERT INTO User_Subscriptions (user_id, plan_id, start_date, end_date, status) VALUES 
(1, 3, '2024-01-01', '2024-02-01', 'Active'),
(2, 2, '2024-01-05', '2024-02-05', 'Active'),
(3, 1, '2023-12-01', '2024-01-01', 'Expired');

-- Watch History
INSERT INTO Watch_History (user_id, content_id) VALUES 
(1, 1), (1, 3), (2, 1), (2, 2), (3, 4), (4, 5), (1, 5);

-- Ratings
INSERT INTO Ratings (user_id, content_id, rating, review) VALUES 
(1, 1, 5, 'Masterpiece!'),
(2, 1, 4, 'Great visuals.'),
(1, 3, 5, 'The best superhero movie.'),
(2, 2, 5, 'Love the 80s vibe.'),
(3, 4, 3, 'Funny but awkward.');
