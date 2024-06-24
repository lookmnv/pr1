CREATE TABLE Authors (
    Id SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL
);

CREATE TABLE Publishers (
    Id SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL
);

CREATE TABLE Books (
    Id SERIAL PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    AuthorId INT REFERENCES Authors(Id),
    PublisherId INT REFERENCES Publishers(Id),
    Price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE Orders (
    Id SERIAL PRIMARY KEY,
    BookId INT REFERENCES Books(Id),
    Quantity INT NOT NULL,
    OrderDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO Authors (Name) VALUES ('Author 1'), ('Author 2');
INSERT INTO Publishers (Name) VALUES ('Publisher 1'), ('Publisher 2');
INSERT INTO Books (Title, AuthorId, PublisherId, Price) VALUES
('Book 1', 1, 1, 19.99),
('Book 2', 2, 2, 29.99);
INSERT INTO Orders (BookId, Quantity) VALUES (1, 2), (2, 1);


CREATE USER books_user WITH PASSWORD 'password123';
GRANT CONNECT, TEMPORARY ON DATABASE books_db TO books_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO books_user;