CREATE DATABASE diesel_offer;

USE diesel_offer;

CREATE TABLE bills(
    id INT AUTO_INCREMENT PRIMARY KEY,
    mobile_number VARCHAR(20),
    vehicle_number VARCHAR(20),
    bill_number VARCHAR(20),
    fuel_liters FLOAT,
    bill_date DATE
);

CREATE TABLE users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50)
);

CREATE TABLE redeemed_offers(
    id INT AUTO_INCREMENT PRIMARY KEY,
    mobile_number VARCHAR(20),
    total_fuel FLOAT,
    reward_name VARCHAR(100),
    redeemed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);