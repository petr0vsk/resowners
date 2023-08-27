set search_path to owners;
-- Таблица серверов
CREATE TABLE if not exists servers (
    server_id SERIAL PRIMARY KEY,
    server_name VARCHAR(255) NOT NULL UNIQUE
);

-- Таблица сетевых дисков
CREATE TABLE if not exists network_drives (
    drive_id SERIAL PRIMARY KEY,
    server_id INT REFERENCES servers(server_id),
    drive_path VARCHAR(255) NOT NULL
);

-- Таблица пользователей (владельцев и заместителей)
CREATE TABLE if not exists users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL UNIQUE
);

-- Таблица директорий без прямых ссылок на владельцев
CREATE TABLE if not exists directories (
    dir_id SERIAL PRIMARY KEY,
    drive_id INT REFERENCES network_drives(drive_id),
    path VARCHAR(255) NOT NULL,
    note TEXT
);

-- Связующая таблица для отношений между директориями и их владельцами
CREATE TABLE if not exists directory_owners (
    dir_id INT REFERENCES directories(dir_id),
    user_id INT REFERENCES users(user_id),
    PRIMARY KEY (dir_id, user_id)
);

-- Связующая таблица для отношений между директориями и их заместителями
CREATE TABLE if not exists directory_second_owners (
    dir_id INT REFERENCES directories(dir_id),
    user_id INT REFERENCES users(user_id),
    PRIMARY KEY (dir_id, user_id)
);





