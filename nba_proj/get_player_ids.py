import sqlite3

def get_player_ids(name, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT player from players WHERE player = ?', (name,))
    result = cursor.fetchone()

    try:
        if result:
            player_id = result[0]
        else:
            cursor.execute('SELECT MAX(player_id) FROM players')
            max_id = cursor.fetchone()[0]
            player_id = 1 if max_id is None else max_id+1

            cursor.execute('INSERT INTO players (player_id, player) VALUES (?, ?)', (player_id, name))
            conn.commit()
            return player_id
    
    except sqlite3.Error as e:
        print(f'Database Error: {e}')
        return None
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()