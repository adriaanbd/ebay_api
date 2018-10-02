import os
import sqlite3
from api_call import get_categories, load_data, urn

# Set your db name:
db_name = "categories.db"


def db_setup():
    """
    Deletes database file if exists in working directory, otherwise it
    creates one by connecting to it, creates our initial table, commits and
    closes connection.
    """
    if db_name in os.listdir("."):
        os.remove(db_name)

    db_conn = sqlite3.connect(db_name)  # Open connection return Conn object
    cur = db_conn.cursor()  # Create Cursor instance for db CRUD operations

    query = """CREATE TABLE categories
        (CategoryID integer primary key,
        CategoryName text,
        CategoryLevel integer,
        BestOfferEnabled integer,
        CategoryParentID integer);
        """

    cur.execute(query)
    db_conn.commit()
    db_conn.close()


def db_conn():
    """
    Connects to our database and returns a connection and cursor.

    :return: Connection object, Cursor instance as tuple
    """
    db_conn = sqlite3.connect(db_name)
    cur = db_conn.cursor()

    return db_conn, cur


def build_db(call):
    """
    Loads XML CategoryArray from API response and iterates through its
    results to find id, name, level and best offer enabled for each
    category, and inserts it into our Categories table.

    :param call: tuple of headers and xml specs for request
    :return:
    """
    db, c = db_conn()

    for items in load_data(call):
        id = int(items.find("{{{}}}CategoryID".format(urn)).text)
        name = items.find("{{{}}}CategoryName".format(urn)).text
        level = int(items.find("{{{}}}CategoryLevel".format(urn)).text)
        boe = 0

        try:
            if items.find("{{{}}}BestOfferEnabled".format(urn)).text == "true":
                boe = 1

        except Exception:
            pass

        parent_id = int(items.find("{{{}}}CategoryParentID".format(urn)).text)
        if parent_id == id:
            parent_id = -1

        category_fields = [id, name, level, boe, parent_id]

        insert_items = """INSERT INTO categories VALUES (?, ?, ?, ?, ?);"""

        c.execute(insert_items, category_fields)

        db.commit()  # COMMIT

    db.close()  # CLOSE


def execute_query(query):
    """
    Executes a SQL query and returns its results in a list with
    cursor.fetchall

    :param query: SQL query
    :return: list of results of SQL query
    """
    db, c = db_conn()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


def tree_view():
    """
    Creates view of adjacency model for categories hierarchy.

    :return:
    """
    db, cur = db_conn()

    view = """CREATE VIEW category_tree AS
    SELECT root.CategoryName as level_1,
            down1.CategoryName as level_2,
            down2.CategoryName as level_3,
            down3.CategoryName as level_4,
            down4.CategoryName as level_5,
            down5.CategoryName as level_6
        FROM categories AS root
    LEFT JOIN categories AS down1
        ON down1.CategoryParentID = root.CategoryID
    LEFT JOIN categories AS down2
        ON down2.CategoryParentID = down1.CategoryID
    LEFT JOIN categories AS down3
        ON down3.CategoryParentID = down2.CategoryID
    LEFT JOIN categories AS down4
        ON down4.CategoryParentID = down3.CategoryID
    LEFT JOIN categories AS down5
        ON down5.CategoryParentID = down4.CategoryID
    WHERE root.CategoryParentID = -1
    ORDER BY level_1, level_2, level_3, level_4, level_5, level_6;"""

    cur.execute(view)
    db.commit()
    db.close()

    
if __name__ == '__main__':
    try:
        db_setup()
        build_db(get_categories())
        tree_view()
    except Exception:
        print("Error setting up the database!")



