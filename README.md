# About
This program uses Python 3.5.2 and its Request library to access Ebay's GetCategories API,  download the entire eBay 
category tree, and stores it in a SQLite database. The SQLite database is 
then queried to render category trees in HTML that reflect the structure of 
the tree.

## Getting started
Download all files and store them in the same directory. The files are:
1. `db_setup.py`
2. `api_call.py`
3. `render_html.py`
4. `get_categories.sh`

### Get the data and set-up your database
From your prompt run `./get_categories.sh --rebuild`. This will run 
`db_setup.py` to create your local `categories.db` database on SQLite in your 
working directory, with a `categories` table and a `category_tree` view of 
the hierarchical structure using an adjacency model. If the `categories.db` 
file already exists in your working directory, the program will delete it 
and create a new one.

### Render html file with CategoryID
From your prompt run `./get_categories.sh --render [CategoryID]` and the 
program will search all childs of the `CategoryID` in reference and create its 
tree 
structure using unordered lists in html. For example, `./get_categories.sh 
--render 1` will generate html file with tree structure for that 
`CategoryID`. If the `categories.db` does not exist in  the working directory 
or the `CategoryID` isn't valid, the program will exit with an error.
