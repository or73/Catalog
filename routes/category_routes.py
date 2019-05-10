from flask import Blueprint, render_template

from database.database_setup import item_category
from modules import app_Category, app_Item, app_User, app_User_Session
from config import auth, db_session, g

category_routes = Blueprint('category_routes', __name__, template_folder='templates')
"""
 * * * * * * * * * * * * * * * * * * * * * * * * *
 --------------- CATEGORY - PUBLIC ---------------
 * * * * * * * * * * * * * * * * * * * * * * * * * 
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


"""
 * * * * * * * * * * * * * * * * * * * * * * * * *
 --------------- CATEGORY - PRIVATE --------------
 * * * * * * * * * * * * * * * * * * * * * * * * * 
"""
# Create CRUD Operations
# Protected with @auth.login_required


@category_routes.route('/catalog/private/<int:category_id>/')
@category_routes.route('/catalog/private/<int:category_id>/category/')
@auth.login_required
def show_category_private(category_id):
    # TODO: show private web page with categories
    return category_id


@category_routes.route('/catalog/private/<int:category_id>/create/')
@category_routes.route('/catalog/private/<int:category_id>/category/create')
@auth.login_required
def create_category(category_id):
    # TODO: button to create a category, the button appears in show_category_private web page
    return category_id


@category_routes.route('/catalog/private/<int:category_id>/delete/')
@category_routes.route('/catalog/private/<int:category_id>/category/delete')
@auth.login_required
def delete_category(category_id):
    # TODO: button to delete a category, the button appears in the show_category_private web page
    #           and in the category web page
    return category_id


@category_routes.route('/catalog/private/<int:category_id>/update/')
@category_routes.route('/catalog/private/<int:category_id>/category/update')
@auth.login_required
def update_category(category_id):
    # TODO: button to update a category, the button appears in the show_category_private web page
    #           and in the category web page
    return category_id


@auth.verify_password
def verify_password(username, password):
    user_session = app_User_Session.get_user_info_name(username)
    user = app_User.get_user_info_name(username)
    if not user or not user_session or not user.verify_password(password):
        return False
    g.user = user
    return True

