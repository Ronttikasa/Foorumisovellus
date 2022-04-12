CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    category_name TEXT NOT NULL
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    header TEXT NOT NULL,
    category_id INTEGER REFERENCES categories
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    user_id INTEGER REFERENCES users,
    thread INTEGER REFERENCES threads,
    first_in_thread BOOLEAN NOT NULL,
    time TIMESTAMP
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    group_name TEXT NOT NULL
);

CREATE TABLE users_in_groups (
    user_id INTEGER REFERENCES users,
    group_id INTEGER REFERENCES groups
);

CREATE TABLE category_access (
    category_id INTEGER REFERENCES categories,
    group_id INTEGER REFERENCES groups
);
