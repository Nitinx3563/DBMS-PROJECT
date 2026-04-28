-- Triggers, Views, and Indexes for Used Car Price Prediction & Marketplace

-- 1. Trigger: When a transaction is inserted, automatically update listing status to "sold"
CREATE TRIGGER IF NOT EXISTS UpdateListingStatusOnTransaction
AFTER INSERT ON Transactions
BEGIN
    UPDATE Listings
    SET status = 'sold'
    WHERE listing_id = NEW.listing_id;
END;

-- 2. View: AvailableCars showing available listings with car details
CREATE VIEW IF NOT EXISTS AvailableCars AS
SELECT 
    L.listing_id,
    L.price,
    L.predicted_price,
    L.condition,
    L.date_posted,
    C.brand,
    C.model,
    C.year,
    C.fuel_type,
    C.mileage,
    CS.engine,
    CS.transmission,
    CS.color,
    CS.seats,
    U.name AS seller_name,
    U.location
FROM Listings L
JOIN Cars C ON L.car_id = C.car_id
JOIN CarSpecifications CS ON C.car_id = CS.car_id
JOIN Users U ON C.user_id = U.user_id
WHERE L.status = 'available';

-- 3. Indexes for performance on price, brand, and location
CREATE INDEX IF NOT EXISTS idx_listing_price ON Listings(price);
CREATE INDEX IF NOT EXISTS idx_car_brand ON Cars(brand);
CREATE INDEX IF NOT EXISTS idx_user_location ON Users(location);

-- 4. Example Price Prediction Logic (Calculated as Average Price)
-- Usage from backend:
-- SELECT AVG(price) FROM Listings JOIN Cars USING(car_id) WHERE brand=? AND model=? AND year=?
