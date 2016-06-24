import sqlite3 as sql

mock_data = (
	('waterloo', 'markham'),
	('waterloo', 'mississauga')
)

with sql.connect('../post.db') as con:
	cur = con.cursor()
	with open('schema.sql') as schema:
		for x in schema.read().split(';'):
			cur.execute(x)
		cur.executemany('INSERT INTO post (origin, destination) VALUES (?, ?)', mock_data)