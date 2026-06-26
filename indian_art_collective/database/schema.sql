-- ============================================================
-- Indian Art Collective - Database Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS indian_art_collective;
USE indian_art_collective;

-- ============================================================
-- CORE TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS ARTISANS (
    Artisan_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    DOB DATE,
    Years_of_Experience INT DEFAULT 0,
    Skill_Level ENUM('Beginner', 'Intermediate', 'Advanced', 'Master') DEFAULT 'Beginner',
    Address TEXT,
    State VARCHAR(50),
    Phone VARCHAR(15),
    Gender ENUM('Male', 'Female', 'Other'),
    Password VARCHAR(255) NOT NULL NOT NULL
);

CREATE TABLE IF NOT EXISTS CRAFT (
    Craft_ID INT AUTO_INCREMENT PRIMARY KEY,
    Craft_Name VARCHAR(100) NOT NULL,
    Category VARCHAR(100),
    Region VARCHAR(100),
    Description TEXT
);

CREATE TABLE IF NOT EXISTS PRODUCT (
    Product_ID INT AUTO_INCREMENT PRIMARY KEY,
    Product_Name VARCHAR(150) NOT NULL,
    Price DECIMAL(10,2) NOT NULL,
    Stock_Quantity INT DEFAULT 0,
    Description TEXT,
    Artisan_ID INT,
    Craft_ID INT,
    Image_URL VARCHAR(255),
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Artisan_ID) REFERENCES ARTISANS(Artisan_ID) ON DELETE SET NULL,
    FOREIGN KEY (Craft_ID) REFERENCES CRAFT(Craft_ID) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS BUYER (
    Buyer_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Phone VARCHAR(15),
    Address TEXT,
    Password VARCHAR(255) NOT NULL NOT NULL
);

CREATE TABLE IF NOT EXISTS ORDERS (
    Order_ID INT AUTO_INCREMENT PRIMARY KEY,
    Order_Date DATE NOT NULL,
    Quantity INT NOT NULL,
    Total_Amount DECIMAL(10,2) NOT NULL,
    Buyer_ID INT,
    Product_ID INT,
    FOREIGN KEY (Buyer_ID) REFERENCES BUYER(Buyer_ID) ON DELETE SET NULL,
    FOREIGN KEY (Product_ID) REFERENCES PRODUCT(Product_ID) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS GOVERNMENT_SCHEMES (
    Scheme_ID INT AUTO_INCREMENT PRIMARY KEY,
    Scheme_Name VARCHAR(150) NOT NULL,
    Launch_Year INT,
    Benefits TEXT,
    Eligibility TEXT
);

CREATE TABLE IF NOT EXISTS EXHIBITION (
    Exhibition_ID INT AUTO_INCREMENT PRIMARY KEY,
    Exhibition_Name VARCHAR(150) NOT NULL,
    Location VARCHAR(200),
    Start_Date DATE,
    End_Date DATE
);

-- ============================================================
-- RELATIONSHIP TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS SPECIALIZES (
    Artisan_ID INT,
    Craft_ID INT,
    PRIMARY KEY (Artisan_ID, Craft_ID),
    FOREIGN KEY (Artisan_ID) REFERENCES ARTISANS(Artisan_ID) ON DELETE CASCADE,
    FOREIGN KEY (Craft_ID) REFERENCES CRAFT(Craft_ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ENROLLED_IN (
    Artisan_ID INT,
    Scheme_ID INT,
    PRIMARY KEY (Artisan_ID, Scheme_ID),
    FOREIGN KEY (Artisan_ID) REFERENCES ARTISANS(Artisan_ID) ON DELETE CASCADE,
    FOREIGN KEY (Scheme_ID) REFERENCES GOVERNMENT_SCHEMES(Scheme_ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS PARTICIPATES (
    Artisan_ID INT,
    Exhibition_ID INT,
    PRIMARY KEY (Artisan_ID, Exhibition_ID),
    FOREIGN KEY (Artisan_ID) REFERENCES ARTISANS(Artisan_ID) ON DELETE CASCADE,
    FOREIGN KEY (Exhibition_ID) REFERENCES EXHIBITION(Exhibition_ID) ON DELETE CASCADE
);

-- Admin table (not in schema but needed for auth)
CREATE TABLE IF NOT EXISTS ADMIN (
    Admin_ID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Email VARCHAR(100)
);

-- ============================================================
-- SAMPLE DATA
-- ============================================================

-- Crafts
INSERT INTO CRAFT (Craft_Name, Category, Region, Description) VALUES
('Madhubani Painting', 'Visual Art', 'Bihar', 'Traditional folk art from the Mithila region of Bihar, characterized by geometric patterns and nature motifs.'),
('Warli Art', 'Visual Art', 'Maharashtra', 'Ancient tribal art form using geometric shapes to depict daily life and nature.'),
('Blue Pottery', 'Ceramic', 'Rajasthan', 'Traditional Jaipur craft using quartz stone paste and blue cobalt oxide dye.'),
('Pashmina Weaving', 'Textile', 'Kashmir', 'Fine handwoven fabric made from Cashmere goat wool, known for warmth and softness.'),
('Dhokra Metal Casting', 'Metal Work', 'Chhattisgarh', 'Non-ferrous metal casting using the lost wax technique, one of the oldest methods.'),
('Kalamkari', 'Textile', 'Andhra Pradesh', 'Hand-painted or block-printed cotton textile using natural dyes and traditional motifs.'),
('Bidriware', 'Metal Work', 'Karnataka', 'Metalwork craft involving zinc and copper alloy inlaid with silver or gold.'),
('Bamboo Craft', 'Handicraft', 'Assam', 'Traditional craft of weaving and shaping bamboo into functional and decorative items.');

-- Artisans (passwords are werkzeug hashes of 'password123')
INSERT INTO ARTISANS (Name, Email, DOB, Years_of_Experience, Skill_Level, Address, State, Phone, Gender, Password) VALUES
('Sunita Devi', 'sunita@artisan.com', '1978-03-15', 25, 'Master', 'Village Ranti, Madhubani', 'Bihar', '9876543210', 'Female', 'scrypt:32768:8:1$HvICUAJD61kHJRoS$e36d561ccd58a04184f1770d0470a3bea5209fe553d02931efb9c7b48d2512b763b07810088dff0c8041638a5eebe0288c0522560999b004affcdc1ec6f04810'),
('Ramesh Warli', 'ramesh@artisan.com', '1985-07-22', 15, 'Advanced', 'Dahanu, Palghar', 'Maharashtra', '9765432109', 'Male', 'scrypt:32768:8:1$HvICUAJD61kHJRoS$e36d561ccd58a04184f1770d0470a3bea5209fe553d02931efb9c7b48d2512b763b07810088dff0c8041638a5eebe0288c0522560999b004affcdc1ec6f04810'),
('Fatima Khanam', 'fatima@artisan.com', '1990-11-08', 10, 'Advanced', 'Jaipur Old City', 'Rajasthan', '9654321098', 'Female', 'scrypt:32768:8:1$HvICUAJD61kHJRoS$e36d561ccd58a04184f1770d0470a3bea5209fe553d02931efb9c7b48d2512b763b07810088dff0c8041638a5eebe0288c0522560999b004affcdc1ec6f04810'),
('Abdul Rashid', 'abdul@artisan.com', '1972-05-30', 30, 'Master', 'Srinagar, Dal Lake Area', 'Jammu & Kashmir', '9543210987', 'Male', 'scrypt:32768:8:1$HvICUAJD61kHJRoS$e36d561ccd58a04184f1770d0470a3bea5209fe553d02931efb9c7b48d2512b763b07810088dff0c8041638a5eebe0288c0522560999b004affcdc1ec6f04810'),
('Priya Kumari', 'priya@artisan.com', '1995-02-14', 5, 'Intermediate', 'Patna, Bihar', 'Bihar', '9432109876', 'Female', 'scrypt:32768:8:1$HvICUAJD61kHJRoS$e36d561ccd58a04184f1770d0470a3bea5209fe553d02931efb9c7b48d2512b763b07810088dff0c8041638a5eebe0288c0522560999b004affcdc1ec6f04810');

-- Buyers (passwords are werkzeug hashes of 'password123')
INSERT INTO BUYER (Name, Email, Phone, Address, Password) VALUES
('Arjun Sharma', 'arjun@buyer.com', '9111234567', '12 MG Road, Bangalore', 'scrypt:32768:8:1$HvICUAJD61kHJRoS$e36d561ccd58a04184f1770d0470a3bea5209fe553d02931efb9c7b48d2512b763b07810088dff0c8041638a5eebe0288c0522560999b004affcdc1ec6f04810'),
('Meera Patel', 'meera@buyer.com', '9222345678', '45 Marine Drive, Mumbai', 'scrypt:32768:8:1$HvICUAJD61kHJRoS$e36d561ccd58a04184f1770d0470a3bea5209fe553d02931efb9c7b48d2512b763b07810088dff0c8041638a5eebe0288c0522560999b004affcdc1ec6f04810'),
('Rahul Gupta', 'rahul@buyer.com', '9333456789', '78 Connaught Place, Delhi', 'scrypt:32768:8:1$HvICUAJD61kHJRoS$e36d561ccd58a04184f1770d0470a3bea5209fe553d02931efb9c7b48d2512b763b07810088dff0c8041638a5eebe0288c0522560999b004affcdc1ec6f04810');

-- Admin
INSERT INTO ADMIN (Username, Password, Email) VALUES
('admin', 'scrypt:32768:8:1$HvICUAJD61kHJRoS$e36d561ccd58a04184f1770d0470a3bea5209fe553d02931efb9c7b48d2512b763b07810088dff0c8041638a5eebe0288c0522560999b004affcdc1ec6f04810', 'admin@indianartcollective.com');

-- Products
INSERT INTO PRODUCT (Product_Name, Price, Stock_Quantity, Description, Artisan_ID, Craft_ID, Image_URL) VALUES
('Madhubani Fish Painting', 1500.00, 10, 'Hand-painted Madhubani art on handmade paper featuring auspicious fish motifs symbolizing prosperity.', 1, 1, '/static/uploads/default_product.jpg'),
('Madhubani Wedding Scene', 2500.00, 5, 'Intricate Madhubani painting depicting a traditional wedding ceremony with vibrant colors.', 1, 1, '/static/uploads/default_product.jpg'),
('Warli Village Life Canvas', 1800.00, 8, 'Large canvas Warli art showing village life, harvest festivals and community gatherings.', 2, 2, '/static/uploads/default_product.jpg'),
('Blue Pottery Vase', 950.00, 15, 'Hand-crafted blue pottery vase from Jaipur with traditional floral patterns.', 3, 3, '/static/uploads/default_product.jpg'),
('Blue Pottery Dinner Set', 4500.00, 3, 'Complete 12-piece dinner set in authentic Jaipur blue pottery style.', 3, 3, '/static/uploads/default_product.jpg'),
('Pure Pashmina Shawl', 8500.00, 6, 'Authentic hand-woven Pashmina shawl from Kashmir with traditional sozni embroidery.', 4, 4, '/static/uploads/default_product.jpg'),
('Pashmina Stole', 3500.00, 12, 'Lightweight Pashmina stole with delicate border patterns, ideal for all seasons.', 4, 4, '/static/uploads/default_product.jpg'),
('Dhokra Ganesha Idol', 1200.00, 20, 'Hand-crafted Ganesha idol using traditional lost wax Dhokra technique.', 2, 5, '/static/uploads/default_product.jpg');

-- Government Schemes
INSERT INTO GOVERNMENT_SCHEMES (Scheme_Name, Launch_Year, Benefits, Eligibility) VALUES
('Pradhan Mantri Kaushal Vikas Yojana', 2015, 'Free skill training, certification, monetary reward up to ₹8000', 'Indian citizens aged 15-45 years'),
('Ambedkar Hastshilp Vikas Yojana', 1992, 'Financial assistance up to ₹5 lakhs, market linkage support, training', 'SC/ST artisans below poverty line'),
('National Handicrafts Development Programme', 2010, 'Design development, marketing support, export promotion', 'Registered handicraft artisans'),
('Rajiv Gandhi Shilpi Swasthya Bima Yojana', 2007, 'Health insurance coverage up to ₹15000 per year', 'Artisans aged 18-60 years with Craft Identity Card'),
('Mudra Yojana for Artisans', 2015, 'Collateral-free loans up to ₹10 lakhs at subsidized interest', 'Artisans with business plan, no existing loans');

-- Exhibitions
INSERT INTO EXHIBITION (Exhibition_Name, Location, Start_Date, End_Date) VALUES
('Dilli Haat Handicraft Mela 2025', 'Dilli Haat, INA, New Delhi', '2025-11-15', '2025-11-30'),
('Surajkund Crafts Mela', 'Surajkund, Faridabad, Haryana', '2025-02-01', '2025-02-16'),
('India International Trade Fair', 'Pragati Maidan, New Delhi', '2025-11-14', '2025-11-27'),
('Crafts of India Exhibition', 'Nehru Centre, Mumbai', '2025-12-10', '2025-12-20'),
('National Crafts Festival', 'Shilpgram, Udaipur, Rajasthan', '2025-12-21', '2026-01-01');

-- Orders
INSERT INTO ORDERS (Order_Date, Quantity, Total_Amount, Buyer_ID, Product_ID) VALUES
('2025-01-10', 2, 3000.00, 1, 1),
('2025-01-15', 1, 1800.00, 2, 3),
('2025-01-20', 1, 950.00, 3, 4),
('2025-02-01', 1, 8500.00, 1, 6),
('2025-02-10', 2, 7000.00, 2, 7),
('2025-02-15', 1, 1200.00, 3, 8),
('2025-03-01', 1, 2500.00, 1, 2),
('2025-03-10', 1, 4500.00, 2, 5);

-- Specializes
INSERT INTO SPECIALIZES (Artisan_ID, Craft_ID) VALUES
(1, 1), (2, 2), (2, 5), (3, 3), (4, 4), (5, 1), (5, 6);

-- Enrolled In
INSERT INTO ENROLLED_IN (Artisan_ID, Scheme_ID) VALUES
(1, 1), (1, 3), (2, 1), (3, 2), (3, 4), (4, 4), (5, 1), (5, 5);

-- Participates
INSERT INTO PARTICIPATES (Artisan_ID, Exhibition_ID) VALUES
(1, 1), (1, 3), (2, 2), (3, 1), (3, 5), (4, 3), (4, 4), (5, 2);
