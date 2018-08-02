tables = [          """

                         CREATE TABLE IF NOT EXISTS mydiary_users(
                         id serial PRIMARY KEY, 
                         name VARCHAR (100), 
                         username VARCHAR (100) UNIQUE NOT NULL ,
                         email VARCHAR (100) UNIQUE NOT NULL ,
                         phone_number VARCHAR (10) UNIQUE ,
                         bio VARCHAR (1000), 
                         gender VARCHAR (10),
                         password VARCHAR (1000))
                         
                      """,
                      """

                         CREATE TABLE IF NOT EXISTS mydiary_entry(
                         id serial PRIMARY KEY,
                         user_id INTEGER NOT NULL ,
                         FOREIGN KEY(user_id) REFERENCES mydiary_users(id) ON DELETE CASCADE,
                         title VARCHAR (100) NOT NULL,
                         body VARCHAR NOT NULL,
                         creation_date VARCHAR (12),
                         update_date VARCHAR (12)
                         )
                            
                         """
        ]
