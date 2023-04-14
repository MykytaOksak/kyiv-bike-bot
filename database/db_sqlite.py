import os
import psycopg2 as ps

class Database:
    def __init__(self, db_name):
        self.con = ps.connect(os.getenv('DATABASE_URL'))
        self.cur = self.con.cursor()
        if self.con:
            print('database is connected')
        self.create_table()

    def create_table(self):
        self.cur.execute('CREATE TABLE IF NOT EXISTS routes(id INTEGER PRIMARY KEY, link TEXT, image TEXT, tags TEXT, description TEXT, rating TEXT)')
        self.con.commit()

    def add(self, values):
        self.cur.execute('INSERT INTO routes(link, image, tags, description, rating) VALUES (?, ?, ?, ?, ?)', values)
        self.con.commit()

    def add_id(self, values):
        self.cur.execute('INSERT INTO routes(id, link, image, tags, description, rating) VALUES (?, ?, ?, ?, ?, ?)', values)
        self.con.commit()

    def read_all(self):
        return self.cur.execute('SELECT * FROM routes').fetchall()

    def read_one(self, id):
        return self.cur.execute('SELECT link, image, tags, description, rating FROM routes WHERE id == ?', (id,)).fetchone()

    def remove_one(self, id):
        self.cur.execute('DELETE FROM routes WHERE id == ?', (id,))
        self.con.commit()

    def update_rating(self, id, rating):
        current_rating = self.cur.execute('SELECT rating FROM routes WHERE id == ?', (id,)).fetchone()[0]
        uid = rating.split(':')[1]
        if current_rating == 'not rated':
            self.cur.execute('UPDATE routes SET rating = ? WHERE id == ?', (rating, id))
            self.con.commit()    
        else:
            if uid in current_rating:
                # replace the old rating with the new rating
                new_rating_list = current_rating.split(';')
                for i, rating_and_used in enumerate(new_rating_list):
                    if f':{uid}' in rating_and_used:
                        new_rating_list[i] = rating
                        break
                new_rating_str = ';'.join(new_rating_list)
                self.cur.execute(f"UPDATE routes SET rating = ? WHERE id = ?", (new_rating_str, id))
                self.con.commit()
            else:
                self.cur.execute('UPDATE routes SET rating = ? WHERE id == ?', (current_rating + ';' + rating, id))
                self.con.commit()      

    def close(self):
        self.cur.close()
        self.con.close()

main_db = Database('approved_routes.db')
propolsals_db = Database('proposed_routes.db')
bin_db = Database('removed_routes.db')