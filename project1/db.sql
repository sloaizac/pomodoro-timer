CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(200) NOT NULL,
    UNIQUE(username)
);

CREATE TABLE books(
    id SERIAL PRIMARY KEY,
    isbn VARCHAR(20) NOT NULL,
    title VARCHAR(50) NOT NULL,
    author VARCHAR(50) NOT NULL,
    year SMALLINT NOT NULL
);

CREATE TABLE reviews(
    book_id INT REFERENCES books(id),
    user_id INT REFERENCES users(id),
    rating SMALLINT NOT NULL,
    opinion VARCHAR(500),
    PRIMARY KEY(book_id, user_id)
);