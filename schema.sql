CREATE TABLE films (
    id SERIAL NOT NULL PRIMARY KEY,
    name TEXT,
    release_year INTEGER,
    description TEXT,
    member_id integer
    CONSTRAINT fk_member
        FOREIGN KEY(member_id)
            REFERENCES members(id)
            ON DELETE SET NULL
);

CREATE TABLE members (
    id SERIAL NOT NULL PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    name TEXT,
    email TEXT,
    role TEXT NOT NULL
);

CREATE TABLE reviews (
    id SERIAL NOT NULL PRIMARY KEY,
    film_id INTEGER NOT NULL,
    username TEXT,
    stars INTEGER,
    text TEXT,
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_film
        FOREIGN KEY(film_id)
            REFERENCES films(id)
            ON DELETE CASCADE
);

CREATE TABLE genres (
    id SERIAL NOT NULL PRIMARY KEY,
    genre TEXT NOT NULL
);

CREATE TABLE films_genres (
    id SERIAL NOT NULL PRIMARY KEY,
    film_id INTEGER NOT NULL REFERENCES films(id) ON DELETE CASCADE,
    genre_id INTEGER NOT NULL REFERENCES genres(id) ON DELETE CASCADE
);