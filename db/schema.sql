DROP TABLE IF EXISTS post;
CREATE TABLE post (
	post_id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone_number VARCHAR(15) NOT NULL,
    num_spots INTEGER,
	origin TEXT NOT NULL,
	destination TEXT NOT NULL,
	publish_date_time DATETIME NOT NULL,
	carpool_date_time DATETIME NOT NULL,
	pick_up TEXT,
	drop_off TEXT,
	price DECIMAL(4, 2)
);