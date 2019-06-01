"""
File Path: application/modules/category/methods.py
Description: Category methods for App - Define Category methods
Copyright (c) 2019. This Application has been developed by OR73.
"""
# from setup import db
from application.setup import db
from .models import Category


class CategoryMethod:
    @staticmethod
    def create_category(name, description, owner):
        """
        Create function, which receives a JSON object'
        and creates a new Category in the database, extracting all
        of the fields required to populate it with the information
        gathered from the 'session'
        It then return the 'category.id' of the new created Category.
        :param name: Category name
        :param description: Category description
        :param owner: Category owner
        :return: category.id
                """
        print('-------------------- Category - create_category')
        new_category = Category(name=name,
                                description=description,
                                owner=owner)
        db.session.add(new_category)
        db.session.commit()
        # Validate if user was created
        category = Category.query.filter_by(name=name).first()
        if category:
            return category
        else:
            return 'Category could not be created'

    @staticmethod
    def delete_by_id(category_id):
        """ Delete a category by its id """
        print('-------------------- Category - delete_by_id')
        category = Category.query.filter_by(id=category_id).first()
        current_db_session = db.session.object_session(category)
        current_db_session.delete(category)
        current_db_session.commit()

    @staticmethod
    def delete_by_name(category_name):
        """ Delete a category by its name """
        print('-------------------- Category - delete_by_id')
        category = Category.query.filter_by(name=category_name).first()
        current_db_session = db.session.object_session(category)
        current_db_session.delete(category)
        current_db_session.commit()

    @staticmethod
    def get_all_category_names():
        """ return a list of all category names """
        print('-------------------- Category - get_all_category_names')
        return Category.query.with_entities(Category.name)

    @staticmethod
    def get_all_category_names_by_provided_category_ids(category_ids):
        """ return a list of category names, by provided category ids """
        print('-------------------- Category - get_all_category_names_by_provided_category_ids')
        category_names_list = []
        for category_id in category_ids:
            category = CategoryMethod.get_category_by_id(category_id=category_id)
            category_names_list.append(category.get_name())
        return category_names_list

    @staticmethod
    def get_all_categories_order_by_name(order_type):
        """ return all categories ordered by name """
        print('-------------------- Category - get_all_categories_order_by_name')
        if order_type == 'desc':
            return list(Category.query.order_by(Category.name.desc()).all())
        return list(Category.query.order_by(Category.name).all())

    @staticmethod
    def get_category_by_id(category_id):
        """ return a category by its provided id """
        print('-------------------- Category - get_category_by_id')
        return Category.query.filter_by(id=category_id).first()

    @staticmethod
    def get_category_by_name(category_name):
        """ return a category by its provided name """
        print('-------------------- Category - get_category_by_name')
        return Category.query.filter_by(name=category_name).first()

    @staticmethod
    def get_id_by_name(category_name):
        """ return category_id by provided category_name """
        print('-------------------- Category - get_id_by_name')
        category = Category.query.filter_by(name=category_name).first()
        return category.get_id()

    @staticmethod
    def get_name_by_id(category_id):
        """ return category_name by provided category_id """
        print('-------------------- Category - get_name_by_id')
        category = Category.query.filter_by(id=category_id).first()
        return category.get_name()

    @staticmethod
    def get_names_of_categories_id_list(categories_id_list):
        """ return a list of categories name from a provided categories_id_list """
        print('-------------------- Category - get_names_of_categories_id_list')
        category_name_list = []
        for category_id in categories_id_list:
            category = Category.query.filter_by(id=category_id).first()
            category_name_list.append(category.get_name())
        return category_name_list

    @staticmethod
    def get_owner_by_id(category_id):
        """ return category_owner by provided category_id """
        print('-------------------- Category - get_owner_by_id')
        category = Category.query.filter_by(id=category_id).first()
        return category.get_owner()

    @staticmethod
    def get_owner_by_name(category_name):
        """ return category_owner by provided category_name """
        print('-------------------- Category - get_owner_by_name')
        category = Category.query.filter_by(name=category_name).first()
        return category.get_owner()

    @staticmethod
    def update_category(category_id, new_name, new_description, new_items):
        """ update_category returns a list of deleted items or empty if none was deleted,
               and a list of new items or empty if nones was added
        :param category_id: Category_id
        :param new_name: New Category name
        :param new_description: New Category description
        :param new_items: updated Category Items list (items name)
        """
        from ..item import ItemMethod
        category = CategoryMethod.get_category_by_id(category_id)
        """ Category to be modified/updated """

        """ Compare & Update 'name' & 'description' data """
        if category.get_name() != new_name:
            category.set_name(new_name)
            db.session.merge(category)
            db.session.commit()
        if category.get_description() != new_description:
            category.set_description(new_description)
            db.session.merge(category)
            db.session.commit()

        new_items_id_list = ItemMethod.get_id_list_by_provided_name_list(new_items)
        """ Create list of item id from list of item name """
        from ..catalog import CatalogMethod
        CatalogMethod.update_catalog(category_id, new_items_id_list, 'category')
        """ Update Catalog """

    @staticmethod
    def update_description_by_id(category_id, new_description):
        """ update category description """
        print('-------------------- Category - update_description_by_id')
        category = Category.query.filter_by(id=category_id).first()
        if category:
            category.set_description(description=new_description)
            category.set_last_update()
            category.session.merge()
            category.session.commit()

    @staticmethod
    def update_description_by_name(name, new_description):
        """ update category description """
        print('-------------------- Category - update_description_by_name')
        category = Category.query.filter_by(name=name).first()
        if category:
            category.set_description(description=new_description)
            category.set_last_update()
            category.session.merge()
            category.session.commit()

    @staticmethod
    def update_name_by_id(category_id, new_name):
        """ update category name """
        print('-------------------- Category - update_name_by_name')
        category = Category.query.filter_by(id=category_id).first()
        if category:
            category.set_name(name=new_name)
            category.set_last_update()
            db.session.merge()
            db.session.commit()
            return True
        return False

    @staticmethod
    def update_name_by_name(category_name, new_name):
        """ update category name """
        print('-------------------- Category - update_name_by_name')
        category = Category.query.filter_by(name=category_name).first()
        if category:
            category.set_name(name=new_name)
            category.set_last_update()
            db.session.merge()
            db.session.commit()
            return True
        return False

    @staticmethod
    def validate_if_some_item_in_new_items_list_already_exist(new_items_list):
        """ validate if some item of a provided 'items_list' exist already in catalog
            the comparison is made by name, and if an item exist its id is added to a
            list, ant finally the list with ids is returned"""
        from ..item import ItemMethod
        print('-------------------- Category - validate_if_some_item_in_new_items_list_already_exist')
        item_id_list = []
        for new_item_name in new_items_list:
            item = ItemMethod.get_item_by_name(new_item_name)
            if item:
                item_id_list.append(item.get_id())
        return item_id_list

    # --------------------- Auth Methods
    @staticmethod
    def auth_method_get_current_user_id():
        """ Return current user_id """
        from ..auth import AuthMethod
        return AuthMethod.get_current_user_id()

    # --------------------- Catalog Methods
    @staticmethod
    def catalog_method_create_catalog(category_id, item_id):
        from ..catalog import CatalogMethod
        return CatalogMethod.create_catalog(category_id, item_id)

    @staticmethod
    def catalog_method_get_all_items_id_of_category_id(category_id):
        """ Return all items_id of an specified category_id """
        from ..catalog import CatalogMethod
        return CatalogMethod.get_all_items_id_of_category_id(category_id)

    @staticmethod
    def catalog_method_get_all_items_name_by_provided_category_id(category_id):
        """ Return a list of items_name by a provided category_id """
        from ..catalog import CatalogMethod
        return CatalogMethod.item_method_get_all_items_name_of_category_id(category_id)

    @staticmethod
    def catalog_method_delete_list_of_category_items(category_id, items_id_of_category):
        """ Delete list of category items """
        from ..catalog import CatalogMethod
        CatalogMethod.delete_list_of_category_items(category_id, items_id_of_category)

    # --------------------- Item Methods
    @staticmethod
    def item_method_get_all_items_order_by_name(order):
        """ Return all items ordered by name """
        from ..item import ItemMethod
        return ItemMethod.get_all_items_order_by_name(order)

    @staticmethod
    def item_method_get_id_by_name(item):
        """ Return item_id by its name """
        from ..item import ItemMethod
        return ItemMethod.get_id_by_name(item)
