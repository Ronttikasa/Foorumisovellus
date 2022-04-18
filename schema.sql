DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS threads CASCADE;
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS groups CASCADE;
DROP TABLE IF EXISTS users_in_groups CASCADE;
DROP TABLE IF EXISTS category_access CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    visible BOOLEAN NOT NULL
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    category_name TEXT NOT NULL,
    visible BOOLEAN NOT NULL
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    topic TEXT NOT NULL,
    category_id INTEGER REFERENCES categories,
    visible BOOLEAN NOT NULL
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    user_id INTEGER REFERENCES users,
    thread_id INTEGER REFERENCES threads,
    first_in_thread BOOLEAN NOT NULL,
    time TIMESTAMP,
    visible BOOLEAN NOT NULL
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    group_name TEXT NOT NULL,
    visible BOOLEAN NOT NULL
);

CREATE TABLE users_in_groups (
    user_id INTEGER REFERENCES users,
    group_id INTEGER REFERENCES groups,
    visible BOOLEAN NOT NULL
);

CREATE TABLE category_access (
    category_id INTEGER REFERENCES categories,
    group_id INTEGER REFERENCES groups,
    visible BOOLEAN NOT NULL
);

INSERT INTO categories (category_name, visible) VALUES ('Testialue', TRUE);