from flask import Blueprint, render_template

from modules import app_Item

item_routes = Blueprint('item_routes', __name__, template_folder='templates')
"""
 * * * * * * * * * * * * * * * * * * *
 --------------- ITEM ---------------
 * * * * * * * * * * * * * * * * * * *
"""
# @app.route('/catalog/category/<int:item_id>/')
# @app.route('/catalog/category/<int:item_id>/item/')
# Show an Item of a Category
@item_routes.route('/catalog/category/<int:item_id>/')
@item_routes.route('/catalog/category/<int:item_id>/item/')
def show_item(item_id):
    print('--------------- show_item')
    item = app_Item.get_item_info(item_id)   # getItemInfo(item_id)
    return render_template('show_item_public.html',
                           item=item)
