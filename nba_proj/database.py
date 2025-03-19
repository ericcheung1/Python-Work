import sqlite3

conn = sqlite3.connect('nba_stats.db')
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
               player_id INTEGER PRIMARY KEY,
               player TEXT
    )
""")
conn.commit()

