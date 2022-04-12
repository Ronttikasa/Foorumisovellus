CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    thread INTEGER REFERENCES threads,
    time TIMESTAMP
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    header TEXT,
    category_id INTEGER REFERENCES categories,
    first_msg_id INTEGER REFERENCES messages
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    category_name TEXT
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    group_name TEXT
);

CREATE TABLE users_in_groups (
    user_id INTEGER REFERENCES users,
    group_id INTEGER REFERENCES groups
);

CREATE TABLE category_access (
    category_id INTEGER REFERENCES categories,
    group_id INTEGER REFERENCES groups
);
