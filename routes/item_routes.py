from flask import Blueprint, render_template

from modules import app_Item, app_User, app_User_Session
from config import auth, g

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

"""
 * * * * * * * * * * * * * * * * * * * * * * *
 --------------- ITEM - PRIVATE --------------
 * * * * * * * * * * * * * * * * * * * * * * * 
"""
# Create CRUD Operations
# Protected with @auth.login_required


@item_routes.route('/catalog/private/category/<int:item_id>/')
@item_routes.route('/catalog/private/category/<int:item_id>/item/')
@auth.login_required
def show_item_private(item_id):
    # TODO: show private web page with items
    return item_id


@item_routes.route('/catalog/private/category/<int:item_id>/create/')
@item_routes.route('/catalog/private/category/<int:item_id>/item/create')
@auth.login_required
def create_item(item_id):
    # TODO: button to create an item, the button appears in show_item_private web page
    return item_id


@item_routes.route('/catalog/private/category/<int:item_id>/delete/')
@item_routes.route('/catalog/private/category/<int:item_id>/item/delete')
@auth.login_required
def delete_item(item_id):
    # TODO: button to delete an item, the button appears in the show_item_private web page
    #           and in the item web page
    return item_id


@item_routes.route('/catalog/private/category/<int:item_id>/update/')
@item_routes.route('/catalog/private/category/<int:item_id>/item/update')
@auth.login_required
def update_category(item_id):
    # TODO: button to update a category, the button appears in the show_category_private web page
    #           and in the category web page
    return item_id


@auth.verify_password
def verify_password(username, password):
    user_session = app_User_Session.get_user_info_name(username)
    user = app_User.get_user_info_name(username)
    if not user or not user_session or not user.verify_password(password):
        return False
    g.user = user
    return True
