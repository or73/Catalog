from flask import Blueprint, render_template, render_template_string

from modules import app_Category, app_Item

catalog_routes = Blueprint('catalog_routes', __name__, template_folder='templates')
"""
 * * * * * * * * * * * * * * * * * * * * *
 ---------------- CATALOG ----------------
 * * * * * * * * * * * * * * * * * * * * *
"""

# Show all categories - PUBLIC
@catalog_routes.route('/')
@catalog_routes.route('/catalog/')
def show_catalog():
    print('-------------- Initial route --------------')
    # Load all categories
    print('Loading all categories...')
    categories_query = app_Category.get_all_categories_name('asc')
    # getAllCategoriesName('asc')  # db_session.query(Category).order_by(asc(Category.name))
    # Load all latest items
    print('Loading all 10 latest items')
    items_query = list(app_Item.get_all_item_create('desc', 10))
    # items_query = list(getAllItemCreate('desc', 10))
    # list(db_session.query(Item).order_by(desc(Item.created)).limit(10))

    for item in items_query:
        print('item: ', item)
        # Create categories property into item, to store all categories name
        item.categories = ''
        # Make a query in item_category table, by item._id
        item_category_query = app_Category.get_all_category_items(item.get_id())
        # getAllCategoryItems(item._id)  # db_session.query(item_category).filter_by(_item_id=item._id).all()
        # Loop in item_categories query, to catch item _id
        for category in item_category_query:
            print('category: ', category)
            # Make a query in Category by _id, to catch the name
            category_query = app_Category.get_category(category[0])
            # getCategory(category[0])  # db_session.query(Category).filter_by(_id=category[0]).one()
            print('category_query: ', category_query)
            # Update item.categories string
            if category_query:
                item_str = ''
                item_str += '<a class="item_category"'
                item_str += 'href="{{ url_for(\'category_routes.show_category\', category_id=%s) }}">' \
                            % category_query.get_id()
                item_str += '- %s</a>' % category_query.name

                item.categories += render_template_string(item_str)
    return render_template('show_catalog_public.html',
                           categories=categories_query,
                           items=items_query)


# Show all categories - PRIVATE
@catalog_routes.route('/catalog/private/')
def show_catalog_private():
    print('-------------- Initial route --------------')
    # Load all categories
    print('Loading all categories...')
    categories_query = app_Category.get_all_categories_name('asc')
    # db_session.query(Category).order_by(asc(Category.name))
    # Load all latest items
    print('Loading all 10 latest items')
    items_query = app_Item.get_all_item_create('desc', 10)
    # list(db_session.query(Item).order_by(desc(Item.created)).limit(10))

    for item in items_query:
        # Create categories property into item, to store all categories name
        item.categories = ''
        # Make a query in item_category table, by item._id
        item_category_query = app_Category.get_all_category_items(item.get_id())
        # Loop in item_categories query, to catch item _id
        for category in item_category_query:
            # Make a query in Category by _id, to catch the name
            category_query = app_Category.get_category(category[0])
            # Update item.categories string
            if category_query:
                item_str = ''
                item_str += '<a class="item_category"'
                item_str += 'href="{{ url_for(\'category_routes.show_category\', category_id=%s) }}">' \
                            % category_query.get_id()
                item_str += '- %s</a>' % category_query.name

                item.categories += render_template_string(item_str)
    return render_template('show_catalog.html',
                           categories=categories_query,
                           items=items_query)
