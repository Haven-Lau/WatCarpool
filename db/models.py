import sqlite3 as sql

mock_data = (
    ('6778678975', 3, 'Waterloo', 'London', '2016-06-12 06:02:31', '2016-06-12 06:02:31', 'Burger King', 'Heather\'s Pussy', 15.00),
    ('8979809870', 16, 'Waterloo', 'Markham', '2016-07-11 06:00:00', '2016-06-11 06:34:33', 'Ez', 'Ernie\'s House', 00.01),
    ('3216089687', 4000, 'Cali', 'Waterloo', '2016-06-04 03:02:21', '2016-06-13 06:02:31', 'Wemesh', 'Yason', 69.00),

)

with sql.connect('../post.db') as con:
    cur = con.cursor()
    with open('schema.sql') as schema:
        for x in schema.read().split(';'):
            cur.execute(x)
        cur.executemany('INSERT INTO post (phone_number, num_spots, origin, destination, publish_date_time, carpool_date_time, pick_up, drop_off, price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', mock_data)