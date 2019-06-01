"""
File Path: application/modules/catalog/views.py
Description: Catalog routes/paths for App - Define Catalog routes/paths
Copyright (c) 2019. This Application has been developed by OR73.
"""
import json
import os
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for, send_from_directory
from flask_login import current_user, login_required, login_user, logout_user
from jinja2 import Template
from markupsafe import Markup

from ..catalog import CatalogMethod

catalog_bp = Blueprint('catalog_bp', __name__)


@catalog_bp.route('/')
@catalog_bp.route('/catalog')
def index():

    # categories = Category.query(name).distinct().order_by(desc(name))
    # items = Item.query().all()
    # return render_template('index.html', categories=categories, items=items, item_categories=item_categories)
    print('1. catalog_bp.route(/) - current_user: ', current_user)

    # Load all categories from DB
    categories = CatalogMethod.category_method_get_all_categories_order_by_name('asc')
    print('|--- categories: ', categories)
    # Load all items from DB
    items = CatalogMethod.item_method_get_all_items_order_by_name('asc')
    print('|--- items: ', items)
    # Load all categories in which the same item exist
    item_categories = {}
    if len(items) > 0 and items:
        print('len(items): ', len(items))
        print('len(categories): ', len(categories))
        for item in items:
            print('item: ', item)
            item_categories[item.get_name()] = CatalogMethod.get_all_categories_name_of_item_id(item.get_id())
            print('item_categories: ', item_categories)
            # CatalogMethod.get_all_categories_id_of_item_id(item.get_id())

    return render_template('index.html',
                           title='Catalog Application',
                           subtitle='Python3 + Flask + SQLALchemy',
                           categories=categories,
                           item_categories=item_categories)


@catalog_bp.route('/endpoint_json')
@login_required
def endpoint_json():
    """ Run and display various analytics reports in JSON format"""
    print('--------------------- Catalog-views - endpoint_json')
    category_dictionary = {}
    all_categories = CatalogMethod.category_method_get_all_categories_order_by_name('asc')

    categories_list = []
    """ Categories list - to return """
    for category in all_categories:
        items_list = CatalogMethod.get_all_items_of_category_id(category.get_id())
        """ Get a list of Items linked with a specified Category_id """

        items_json_list = []
        """ Items list linked with a Category """
        for item in items_list:
            item_json = {
                'id': item.get_id(),
                'name': item.get_name(),
                'description': item.get_description(),
                'price': item.get_price(),
                'category_id': category.get_id()
            }
            items_json_list.append(item_json)

        category_json = {
            'id': category.get_id(),
            'name': category.get_name(),
            'description': category.get_description(),
            'owner': category.get_owner(),
            'items': items_json_list
        }
        """ Create Category JSON object """

        categories_list.append(category_json)
        """ Append Category JSON object to categories_list """
    """ Loop to append each category details and contained items """

    category_dictionary['Category'] = categories_list
    """ Append categories_list to category_dictionary """

    """ Get all items in a list of dictionaries """
    return render_template('catalog/endpoint_json.html',
                           title='EndPoint - JSON',
                           categories=json.dumps(category_dictionary, indent=2))


@catalog_bp.route('/endpoint_web')
@login_required
def endpoint_web():
    """ Run and display various analytics reports in HTML format """
    categories = CatalogMethod.category_method_get_all_categories_order_by_name('asc')
    """ All categories is ascendant order """

    items = CatalogMethod.item_method_get_all_items_order_by_name('asc')
    """ All items in ascendant order """

    # { category_name: [items_name ], ... }
    catalog_links_name_by_category = CatalogMethod.get_all_catalog_links_grouped_by_category()
    """ All catalog_links with category_name & item_name, grouped by category """
    # { item_name: [categories_name ], ... }
    catalog_links_name_by_item = CatalogMethod.get_all_catalog_links_grouped_by_item()
    """ All catalog_links with category_name & item_name, grouped by item """

    # { user_id: [(login_time, logout_time), ...], ... }
    login_logout_sessions = CatalogMethod.auth_method_get_all_in_dictionary()
    """ All login_logout_sessions start/end """

    print('login_logout_sessions: ', login_logout_sessions)

    # user_name - login_time - logout_time - duration
    # login_logout_sessions_name = CatalogMethod.get_all_login_logout_sessions_names()
    """ All login_logout_sessions start/end with date-format & time duration """
    return render_template('catalog/endpoint_web.html',
                           title='EndPoint - WEB',
                           categories=categories,
                           items=items,
                           catalog_links_categories=catalog_links_name_by_category,
                           catalog_links_items=catalog_links_name_by_item,
                           login_logout_sessions=login_logout_sessions)


@catalog_bp.route('/favicon')
@catalog_bp.route('/favicon.ico')
def favicon():
    ico_dir = os.path.join(os.path.dirname(os.getcwd()), 'userApp', 'application', 'static', 'dist', 'img', 'ico')
    print('ico_dir: ', ico_dir)
    return send_from_directory(ico_dir, 'favicon.ico')


@catalog_bp.errorhandler(400)
def key_error(e):
    return render_template('400.html', error=e), 400


@catalog_bp.errorhandler(500)
def internal_server_error(e):
    return render_template('generic.html', error=e), 500


@catalog_bp.errorhandler(Exception)
def unhandled_exception(e):
    return render_template('generic.html', error=e, exception=Exception), 500
