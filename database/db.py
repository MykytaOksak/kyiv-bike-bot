import psycopg2


class Database:
    def __init__(self, url):
        self.url = url
        self.conn = None
        self.cursor = None

    def connect(self):
        print('database url: ', self.url)
        self.conn = psycopg2.connect(self.url, sslmode='require')
        self.cursor = self.conn.cursor()
        if self.conn:
            print('database is connected')
    
    def create_table(self, table_name):
        query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            link TEXT,
            image TEXT,
            tags TEXT,
            description TEXT,
            rating TEXT
        );
        '''
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query)
    
    def add(self, table_name, values):
        query = f'''
        INSERT INTO {table_name} (link, image, tags, description, rating)
        VALUES (%s, %s, %s, %s, %s);
        '''
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query, values)
    
    def add_id(self, table_name, values):
        query = f'''
        INSERT INTO {table_name} (id, link, image, tags, description, rating)
        VALUES (%s, %s, %s, %s, %s, %s);
        '''
        with self.conn:
            with self.conn.cursor() as cur:            
                cur.execute(query, values)
    
    def read_all(self, table_name):
        query = f'SELECT * FROM {table_name};'
        with self.conn:
            with self.conn.cursor() as cur:            
                cur.execute(query)
                rows = cur.fetchall()
                return rows
    
    def read_one(self, table_name, id):
        query = f'SELECT link, image, tags, description, rating FROM {table_name} WHERE id=%s;'
        values = (id,)
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query, values)
                row = cur.fetchone()
                return row
    
    def remove_one(self, table_name, id):
        query = f'DELETE FROM {table_name} WHERE id=%s;'
        values = (id,)
        with self.conn:
            with self.conn.cursor() as cur:            
                cur.execute(query, values)
    
    def update_rating(self, table_name, id, rating):
        query = f'SELECT rating FROM {table_name} WHERE id=%s;'
        values = (id,)
        with self.conn:
            with self.conn.cursor() as cur:            
                cur.execute(query, values)
                current_rating = cur.fetchone()[0]
        
        uid = rating.split(':')[1]
        
        if current_rating == 'not rated':
            query = f'UPDATE {table_name} SET rating=%s WHERE id=%s;'
            values = (rating, id)
            
            with self.conn:
                with self.conn.cursor() as cur:                
                    cur.execute(query, values)
        else:
            if uid in current_rating:
                # replace user's old rating with a new one
                new_rating_list = current_rating.split(';')
                
                for i, rating_and_used in enumerate(new_rating_list):
                    if f':{uid}' in rating_and_used:
                        new_rating_list[i] = rating
                        break
                
                new_rating_str = ';'.join(new_rating_list)
                query = f'UPDATE {table_name} SET rating=%s WHERE id=%s;'
                values = (new_rating_str, id)
                
                with self.conn:
                    with self.conn.cursor() as cur:
                        cur.execute(query, values)
            else:
                query = f'UPDATE {table_name} SET rating=%s WHERE id=%s;'
                values = (current_rating + ';' + rating, id)
                
                with self.conn:
                    with self.conn.cursor() as cur:                    
                        cur.execute(query, values)            
    
    def close(self):
        self.cursor.close()
        self.conn.close()
   