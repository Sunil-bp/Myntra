import sqlite3

def check_db():
    conn = sqlite3.connect('_mynra.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    tables = [item for t in tables for item in t]

    if len(tables) != 3:
        if "PRODUCT" not in tables:
            print("Crating product tables")
            conn.execute('''CREATE TABLE PRODUCT
                     (ID INT PRIMARY KEY     NOT NULL,
                     PRODUCT_NAME           TEXT    ,
                     PRODUCT_ID             INT     NOT NULL,
                     PRODUCT_MRP             INT    ,
                     PRODUCT_URL            CHAR(200)    ,
                     SIZE                   CHAR(50)    ,
                     IMAGE_URL              CHAR(200)  ,
                     articleType            CHAR(50)    ,
                     subCategory            CHAR(50)    ,
                     masterCategory         CHAR(50)    ,
                     gender                 CHAR(50)    ,
                     brand                  CHAR(50)    
                     );''')

            print("Created product table")
        print(tables)
        if "SIZE" not in tables:
            print("Crating size tables")
            conn.execute('''CREATE TABLE SIZE
                                 (SIZE_ID    INT PRIMARY KEY     NOT NULL,
                                 PRODUCT_ID             INT    NOT NULL,
                                 SIZE                   CHAR(50)     NOT NULL,
                                  FOREIGN KEY(PRODUCT_ID) REFERENCES PRODUCT(PRODUCT_ID)
                                 );''')

            print("Created size table")

        if "PRICE" not in tables:
            print("Crating PRICE tables")
            conn.execute('''CREATE TABLE PRICE
                                 (PRICE_ID    INT PRIMARY KEY     NOT NULL,
                                 PRODUCT_ID             INT    NOT NULL,
                                 SIZE_ID                  INT     NOT NULL,
                                 PRICE                 INT   NOT NULL,
                                 Date timestamp,
                                  FOREIGN KEY(PRODUCT_ID) REFERENCES PRODUCT(PRODUCT_ID)
                                  FOREIGN KEY(SIZE_ID) REFERENCES SIZE(SIZE_ID)
                                 );''')

            print("Created PRICE table")

    cursor.close()
    conn.close()