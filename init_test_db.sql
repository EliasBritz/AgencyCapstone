DROP TABLE IF EXISTS movie_actors CASCADE;
DROP TABLE IF EXISTS actors CASCADE;
DROP TABLE IF EXISTS movies CASCADE;

CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_date TIMESTAMP NOT NULL
);

CREATE TABLE actors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INTEGER NOT NULL,
    gender VARCHAR(50) NOT NULL
);

CREATE TABLE movie_actors (
    movie_id INTEGER,
    actor_id INTEGER,
    PRIMARY KEY (movie_id, actor_id),
    FOREIGN KEY (movie_id) REFERENCES movies (id) ON DELETE CASCADE,
    FOREIGN KEY (actor_id) REFERENCES actors (id) ON DELETE CASCADE
);

INSERT INTO movies (title, release_date) VALUES
('Movie 1', '2022-01-01 00:00:00'),
('Movie 2', '2022-02-02 00:00:00');

INSERT INTO actors (name, age, gender) VALUES
('Actor 1', 30, 'Male'),
('Actor 2', 25, 'Female'),
('Actor 3', 40, 'Male');

INSERT INTO movie_actors (movie_id, actor_id) VALUES
(1, 1),
(1, 2),
(2, 3);