import os
import sqlite3
import sys

db_name = "categories.db"

if db_name not in os.listdir("."):
    raise AssertionError

def getParent(categoryId):
    """
    Selects the category as root and returns it.

    :param categoryId: CategoryID used to select given category as root.
    :return: the row of the selected category as root.
    """
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    category_row = None
    query = """SELECT * FROM categories WHERE CategoryID = {};""".format(
        categoryId)
    cur.execute(query)
    category_row = cur.fetchone()

    conn.commit()
    conn.close()

    return category_row

def getChild(category_id):
    """
    Gets all children of a given category id provided as arg.

    :param category_id: CategoryID used for filtering purposes.
    :return:
    """
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    categories = None
    query = """
    SELECT * FROM categories 
    WHERE CategoryParentID = {};""".format(str(category_id))
    cur.execute(query)

    categories = cur.fetchall()

    conn.commit()
    conn.close()

    return categories

def render_cats(html_file, category_row):
    """
    Renders the category tree branch at the given ID from root to leaf in
    an unordered list.

    :param html_file: html file created with CategoryID number
    :param category: single Category row from getChild()
    :return:
    """
    list_header = "<ul>"
    html_file.write(list_header)

    name = category_row[1]
    list_item = "<li>{}</li>".format(name)
    html_file.write(list_item)

    id = category_row[0]
    child_rows = getChild(id)
    if len(child_rows) > 0:
        for son_row in child_rows:
            render_cats(html_file, son_row)

    list_footer = "</ul>"
    html_file.write(list_footer)


def start():
    """
    Starts the render html operation by taking the CategoryID provided by user.

    :return:
    """
    id = sys.argv[1]
    category = getParent(id)

    if category is None:
        print("\nInvalid ID: {}".format(id))
        raise AssertionError

    else:
        html_file_name = "{}.html".format(id)
        file = open(html_file_name, "w")

        html = """<!DOCTYPE html>"""
        html += """<html lang="en">"""
        html += """<head>"""
        html += """<meta charset="utf-8">"""
        html += """<title> The Ebay Category Hierarchy</title>"""
        html += """</head>"""
        html += """<body>"""
        html += """<h1>Category Tree for {}</h1>""".format(category[1])

        file.write(html)
        render_cats(file, category)

        html = """</body></html>"""
        file.write(html)
        file.close()

        print(html_file_name)


def render_all():
    """
    Renders html files for the whole hierarchy. Careful!

    :return:
    """
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    query = """SELECT * FROM categories;"""
    cur.execute(query)
    results = cur.fetchall()

    for row in results:
        id = row[0]
        category = getParent(id)

        html_file_name = "{}.html".format(id)
        file = open(html_file_name, "w")

        html = """<!DOCTYPE html>"""
        html += """<html lang="en">"""
        html += """<head>"""
        html += """<meta charset="utf-8">"""
        html += """<title> The Ebay Category Hierarchy</title>"""
        html += """</head>"""
        html += """<body>"""
        html += """<h1>Category Tree for {}</h1>""".format(category[1])

        file.write(html)
        render_cats(file, category)

        html = """</body></html>"""
        file.write(html)
        file.close()

        print(html_file_name)


if __name__ == '__main__':
    try:
        start()
    except Exception:
        print("Error rendering html!")