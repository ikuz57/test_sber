CREATE SCHEMA IF NOT EXISTS content;
GRANT ALL ON SCHEMA content TO app;

CREATE TABLE IF NOT EXISTS content.departments (
    id INT PRIMARY KEY,
    name TEXT NOT NULL,
    code BIGINT NOT NULL,
    type_dep TEXT NOT NULL,
    address TEXT NOT NULL,
    coordinates TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS content.schedule (
    id SERIAL PRIMARY KEY,
    department_id INT,
    day INT NOT NULL,
    start_work INT DEFAULT 0,
    finish_work INT DEFAULT(24*60),
    start_break INT DEFAULT 0,
    finish_break INT DEFAULT(24*60),
    modified DATE,
    FOREIGN KEY (department_id) REFERENCES content.departments (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS content.workingtime (
    id SERIAL PRIMARY KEY,
    department_id INT,
    date timestamp,
    time_work INT,
    FOREIGN KEY (department_id) REFERENCES content.departments (id) ON DELETE CASCADE
);