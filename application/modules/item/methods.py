"""
File Path: application/modules/item/methods.py
Description: Category methods for App - Define Category methods
Copyright (c) 2019. This Application has been developed by OR73.
"""
# from setup import db
from application.setup import db

from ..item import Item


class ItemMethod:
    @staticmethod
    def create_item(name, description, price, owner):
        """
        Create function, which receives a JSON object'
        and creates a new Item in the database, extracting all
        of the fields required to populate it with the information
        gathered from the 'session'
        It then return the 'item.id' of the new created Item.
        :param name: Item name
        :param description: Item description
        :param price: Item price
        :param owner: Item owner
        :return: item.id
        """
        print('-------------------- Item - create_item')
        new_item = Item(name=name,
                        description=description,
                        price=price,
                        owner=owner)
        db.session.add(new_item)
        db.session.commit()
        # Validate if user was created
        item = Item.query.filter_by(name=name).first()
        if item:
            return item
        else:
            return 'Item could not be created'

    @staticmethod
    def delete_by_id(item_id):
        """ delete item by id """
        print('-------------------- Item - delete_by_id')
        item = Item.query.filter_by(id=item_id).first()
        if item:
            current_db_session = db.session.object_session(item)
            current_db_session.delete(item)
            current_db_session.commit()
        return False

    @staticmethod
    def delete_by_name(item_name):
        """ delete item by name """
        print('-------------------- Item - delete_by_name')
        item = Item.query.filter_by(name=item_name).first()
        if item:
            current_db_session = db.session.object_session(item)
            current_db_session.delete(item)
            current_db_session.commit()
        return False

    @staticmethod
    def get_all_item_ids_by_provided_item_ids(item_ids):
        """ return a list of item_names, by provided list of item_ids """
        print('-------------------- Item - get_all_item_ids_by_provided_item_ids')
        item_names_list = []
        for item_id in item_ids:
            item = Item.query.filter_by(id=item_id).first()
            item_names_list.append(item.get_id())
        return item_names_list

    @staticmethod
    def get_all_item_ids_by_provided_item_names(item_names):
        """ return a list of item_ids, by provided list of item_names """
        print('-------------------- Item - get_all_item_ids_by_provided_item_names')
        item_ids_list = []
        for item_name in item_names:
            item = Item.query.filter_by(name=item_name).first()
            item_ids_list.append(item.get_id())
        return item_ids_list

    @staticmethod
    def get_all_item_names(order_type):
        """ return a list with all item names """
        print('-------------------- Item - get_all_item_names')
        if order_type == 'desc':
            return Item.query.order_by(Item.name.desc()).with_entities(Item.name)
        return Item.query.order_by(Item.name).with_entities(Item.name)

    @staticmethod
    def get_all_items_order_by_name(order_type):
        """ return all items ordered by name """
        print('-------------------- Item - get_all_items_order_by_name')
        if order_type == 'desc':
            return list(Item.query.order_by(Item.name.desc()).all())
        return list(Item.query.order_by(Item.name).all())

    @staticmethod
    def get_id_by_name(item_name):
        """ return item_id by its item_name """
        print('-------------------- Item - get_id_by_name')
        return (Item.query.filter_by(name=item_name).first()).get_id()

    @staticmethod
    def get_id_list_by_provided_name_list(items_name_list):
        """ return a list of items_id by a provided list or items_name """
        print('-------------------- Item - get_id_list_by_provided_name_list')
        print('items_name_list: ', items_name_list)
        if len(items_name_list) > 0 and items_name_list:
            item_id_list = []
            for item_name in items_name_list:
                item = ItemMethod.get_item_by_name(item_name=item_name)
                item_id_list.append(item.get_id())
            return item_id_list
        return []

    @staticmethod
    def get_category_id_list_by_provided_category_name_list(category_name_list):
        """ return a list of category_id by a provided list of category_name """
        print('-------------------- Item - get_category_id_list_by_provided_category_name_list')
        print('category_name_list: ', category_name_list)
        if len(category_name_list) and category_name_list:
            from ..category import CategoryMethod
            category_id_list = []
            for category_name in category_name_list:
                category = CategoryMethod.get_category_by_name(category_name)
                category_id_list.append(category.get_id())
            return category_id_list
        return []

    @staticmethod
    def get_item_by_id(item_id):
        """ return Item object by provided item_id """
        print('-------------------- Item - get_item_by_id')
        return Item.query.filter_by(id=item_id).first()

    @staticmethod
    def get_item_by_name(item_name):
        """ return Item object by provided item_name """
        print('-------------------- Item - get_item_by_name')
        return Item.query.filter_by(name=item_name).first()

    @staticmethod
    def get_name_by_id(item_id):
        """ return Item_name by its item_id """
        print('-------------------- Item - get_name_by_id')
        return (Item.query.filter_by(id=item_id).first()).get_name()

    @staticmethod
    def get_names_of_items_id_list(items_id_list):
        """ return a list of items name by provided items_id_list """
        print('-------------------- Item - get_names_of_items_id_list ')
        items_name_list = []
        for item_id in items_id_list:
            item = Item.query.filter_by(id=item_id).first()
            items_name_list.append(item.get_name())
        return items_name_list

    @staticmethod
    def get_owner_by_id(item_id):
        """ return item owner by its id """
        print('-------------------- Item - get_owner_by_id')
        return (Item.query.filter_by(id=item_id).first()).get_owner()

    @staticmethod
    def get_owner_by_name(item_name):
        """ return item owner by its name """
        print('-------------------- Item - get_owner_by_name')
        return (Item.query.filter_by(name=item_name).first()).get_owner()

    @staticmethod
    def update_description_by_id(item_id, new_description):
        """ update item description by its item_id """
        print('-------------------- Item - update_description_by_id')
        item = Item.query.filter_by(id=item_id).first()
        if item:
            item.set_name(new_description)
            item.set_last_update()
            db.session.merge()
            db.session.commit()
            return True
        return False

    @staticmethod
    def update_description_by_name(item_name, new_description):
        """ update item description by its item_name """
        print('-------------------- Item - update_description_by_name')
        item = Item.query.filter_by(name=item_name).first()
        if item:
            item.set_name(new_description)
            item.set_last_update()
            db.session.merge()
            db.session.commit()
            return True
        return False

    @staticmethod
    def update_item(item_id, new_name, new_description, new_price, new_categories):
        """ update_item returns a list of deleted categories or empty if none was deleted,
               and a list of new categories or empty if nones was added
        :param item_id: item_id
        :param new_name: New Item name
        :param new_description: New Item description
        :param new_price: New Item price
        :param new_categories: updated Item categories list (items name)
        """
        print('-------------------- Item - update_item')
        item = ItemMethod.get_item_by_id(item_id)
        """ Item to be modified/updated """

        """ Compare & Update 'name', 'description' & 'price' data """
        if item.get_name() != new_name:
            item.set_name(new_name)
            db.session.merge(item)
            db.session.commit()
        if item.get_description() != new_description:
            item.set_description(new_description)
            db.session.merge(item)
            db.session.commit()
        if item.get_price() != new_price:
            item.set_price(new_price)
            db.session.merge(item)
            db.session.commit()
        from ..catalog import CatalogMethod
        categories_name_of_current_item_by_id = CatalogMethod.get_all_categories_name_of_item_id(item_id)
        """ Current item categories """
        counter = 0
        if len(new_categories) > 0:
            for new_category in new_categories:
                if new_category not in categories_name_of_current_item_by_id:
                    counter += 1
        print('categories_name_of_current_item_by_id: ', categories_name_of_current_item_by_id)
        print('new_categories: ', new_categories)
        print('counter: ', counter)

        """ Make a comparison against new_categories and current_item_categories """
        if counter > 0:
            new_categories_id_list = ItemMethod.get_category_id_list_by_provided_category_name_list(new_categories)
            """ Create list of item id from list of item name """
            CatalogMethod.update_catalog(item_id, new_categories_id_list, 'item')
            """ Update Catalog """

    @staticmethod
    def update_name_by_id(item_id, new_name):
        """ update item name by its item_id """
        print('-------------------- Item - update_name_by_id')
        item = Item.query.filter_by(id=item_id).first()
        if item:
            item.set_name(new_name)
            item.set_last_update()
            db.session.merge()
            db.session.commit()
            return True
        return False

    @staticmethod
    def update_name_by_name(item_name, new_name):
        """ update item name by its item_name """
        print('-------------------- Item - update_name_by_name')
        item = Item.query.filter_by(name=item_name).first()
        if item:
            item.set_name(new_name)
            item.set_last_update()
            db.session.merge()
            db.session.commit()
            return True
        return False

    @staticmethod
    def update_price_by_id(item_id, new_price):
        """ update item price by its item_id """
        print('-------------------- Item - update_price_by_id')
        item = Item.query.filter_by(id=item_id).first()
        if item:
            item.set_name(new_price)
            item.set_last_update()
            db.session.merge()
            db.session.commit()
            return True
        return False

    @staticmethod
    def update_price_by_name(item_name, new_price):
        """ update item price by its item_name """
        print('-------------------- Item - update_name_by_name')
        item = Item.query.filter_by(name=item_name).first()
        if item:
            item.set_name(new_price)
            item.set_last_update()
            db.session.merge()
            db.session.commit()
            return True
        return False

    # --------------------- Auth Methods
    @staticmethod
    def auth_method_get_current_user_id():
        """ Return current_user_id """
        from ..auth import AuthMethod
        return AuthMethod.get_current_user_id()

    # --------------------- Catalog Methods
    @staticmethod
    def catalog_method_create_catalog(category_id, item_id):
        """ Return a new Catalog link """
        from ..catalog import CatalogMethod
        return CatalogMethod.create_catalog(category_id=category_id, item_id=item_id)

    @staticmethod
    def catalog_method_delete_list_of_item_categories(item_id, categories_id_of_item):
        """ Delete a list of item categories """
        from ..catalog import CatalogMethod
        CatalogMethod.delete_list_of_item_categories(item_id, categories_id_of_item)

    @staticmethod
    def catalog_method_get_all_categories_id_of_item_id(item_id):
        """ Return all categories_id of an item_id """
        from ..catalog import CatalogMethod
        return CatalogMethod.get_all_categories_id_of_item_id(item_id)

    @staticmethod
    def catalog_method_get_all_categories_name_of_item_id(item_id):
        """ Return all categories name of an item_id """
        from ..catalog import CatalogMethod
        return CatalogMethod.get_all_categories_name_of_item_id(item_id)

    # --------------------- Category Methods
    @staticmethod
    def category_method_get_all_categories_order_by_name(order):
        """ Return all categories ordered by name """
        from ..category import CategoryMethod
        return CategoryMethod.get_all_categories_order_by_name(order_type=order)

    @staticmethod
    def category_method_get_id_by_name(category_name):
        """ Return category_id by its name """
        from ..category import CategoryMethod
        return CategoryMethod.get_id_by_name(category_name=category_name)
