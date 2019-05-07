from flask import Blueprint, render_template

from database.database_setup import item_category
from modules import app_Category, app_Item
from config import db_session

category_routes = Blueprint('category_routes', __name__, template_folder='templates')
"""
 * * * * * * * * * * * * * * * * * * * * *
 --------------- CATEGORY ----------------
 * * * * * * * * * * * * * * * * * * * * *
"""

# Show a Category
@category_routes.route('/catalog/<int:category_id>/')
@category_routes.route('/catalog/<int:category_id>/category/')
def show_category(category_id):
    print('--------------- show_category')
    print('category_id: ', category_id)

    # Validate if category_id exists
    category = app_Category.get_category(category_id)
    # db_session.query(Category).filter_by(_id=category_id).one()

    if category:
        # Load all category items
        items_query = db_session.query(item_category).filter_by(_category_id=category_id)
        items = []
        for item in items_query:
            items.append(app_Item.get_item_info(item[1]))
            # items.append(db_session.query(Item).filter_by(_id=item[1]).one())
        return render_template('show_category_public.html',
                               category=category.name,
                               items=items)
    else:  # Category does not exist
        print('Category does not exist')
        return
