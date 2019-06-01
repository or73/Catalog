"""
File Path: application/modules/catalog/methods.py
Description: Catalog methods for App - Define Catalog methods
Copyright (c) 2019. This Application has been developed by OR73.
"""
# from setup import db
from application.setup import db
from .models import Catalog
from ..auth import AuthMethod


class CatalogMethod:
    @staticmethod
    def create_catalog(category_id, item_id):
        """
        Create function, which receives a JSON object'
        and creates a new Catalog in the database, extracting all
        of the fields required to populate it with the information
        gathered from the 'session'
        It then return the 'catalog.id' of the new created Catalog.
        :param category_id: Category id to add
        :param item_id: Item id to add
        :return: catalog.id
        """
        print('---------------- create_catalog')

        new_catalog = Catalog(category_id=category_id, item_id=item_id)
        """ Create new_catalog """
        db.session.add(new_catalog)
        """ Add new_catalog to DB """
        db.session.commit()
        """ Commit Adding operation to DB"""

        catalog = Catalog.query.filter_by(category_id=category_id, item_id=item_id).first()
        """ Validate if Catalog link was created """

        if catalog:
            return catalog.get_id()
        else:
            return None

    # -------------------------- Catalog Methods
    @staticmethod
    def add(category_id, item_id):
        print('---------------- Catalog - add: category_id: %s - item_id: %s' % (category_id, item_id))
        link_to_add = Catalog(category_id, item_id)
        db.session.add(link_to_add)
        db.session.commit()

    @staticmethod
    def delete(category_id, item_id):
        print('---------------- Catalog - delete: category_id: %s - item_id: %s' % (category_id, item_id))
        link_to_delete = Catalog.query.filter_by(category_id=category_id, item_id=item_id).first()
        current_db_session = db.session.object_session(link_to_delete)
        current_db_session.delete(link_to_delete)
        current_db_session.commit()

    @staticmethod
    def get_all_catalog_links_grouped_by_category():
        """ Return all links (category_id, item_id) grouped by category"""
        from ..category import CategoryMethod
        from ..item import ItemMethod
        all_categories = CategoryMethod.get_all_categories_order_by_name('asc')
        # Category.query.order_by(Category.name).all()
        """ all_categories ordered by 'name' """
        links_by_category = {}
        """ dictionary to return """

        for category in all_categories:
            category_items_id = CatalogMethod.get_all_items_id_of_category_id(category.get_id())
            """ List with all item_id of a specified category id """
            links_by_category[category.get_name()] = []
            """ New item in 'links_by_category' dictionary """
            for item_id in category_items_id:
                item = ItemMethod.get_item_by_id(item_id)
                links_by_category[category.get_name()].append(item.get_name())
        return links_by_category

    @staticmethod
    def get_all_catalog_links_grouped_by_item():
        """ Return all links (category_id, item_id) grouped by item"""
        from ..category import CategoryMethod
        from ..item import ItemMethod
        all_items = ItemMethod.get_all_items_order_by_name('asc')
        """ all_items ordered by name """
        links_by_item = {}
        """ dictionary to return """

        for item in all_items:
            item_categories_id = CatalogMethod.get_all_categories_id_of_item_id(item.get_id())
            """ List with all category_id of a specified item id """
            links_by_item[item.get_name()] = []
            for category_id in item_categories_id:
                category = CategoryMethod.get_category_by_id(category_id)
                # Category.query.filter_by(id=category_id).first()
                links_by_item[item.get_name()].append(category.get_name())

    @staticmethod
    def get_all_categories_id_of_item_id(item_id):
        """ Return a list with all categories id associated with a provided item_id """
        print('--------------- Catalog - get_all_categories_id_of_item_id')
        list_of_categories_id = list(Catalog.query.filter_by(item_id=item_id).with_entities(Catalog.category_id))
        categories_id_list = []
        for item_duple in list_of_categories_id:
            categories_id_list.append(item_duple[0])
        return categories_id_list

    @staticmethod
    def get_all_items_id_of_category_id(category_id):
        """ Return a list with all items id associated with a provided category id """
        print('---------------- Catalog - get_all_items_id_of_category_id')
        list_of_items_id = list(Catalog.query.filter_by(category_id=category_id).with_entities(Catalog.item_id))
        items_id_list = []
        for item_duple in list_of_items_id:
            items_id_list.append(item_duple[0])
        return items_id_list

    @staticmethod
    def get_all_items_of_category_id(category_id):
        """ Return a list with all items associated with a provided category id """
        print('---------------- Catalog - get_all_items_of_category_id')
        list_of_items_id = list(Catalog.query.filter_by(category_id=category_id).with_entities(Catalog.item_id))
        from ..item import ItemMethod
        items_list = []
        for item_duple in list_of_items_id:
            item = ItemMethod.get_item_by_id(item_duple[0])
            items_list.append(item)
        return items_list

    @staticmethod
    def get_catalog_link(cat_id):
        """ Return a Catalog link specified by Catalog id """
        print('---------------- Catalog - get_catalog_link by id')
        return Catalog.query.filter_by(id=cat_id).first()

    # -------------------------- Category Methods
    @staticmethod
    def delete_list_of_category_items(category_id, items_id_of_category):
        print('--------------- Catalog - delete_list_of_category_items ')
        for item_id in items_id_of_category:
            link_to_delete = Catalog.query.filter_by(category_id=category_id, item_id=item_id).first()
            current_db_session = db.session.object_session(link_to_delete)
            current_db_session.delete(link_to_delete)
            current_db_session.commit()

    @staticmethod
    def get_all_categories_id():
        """ Return a list of all categories id in a Catalog """
        print('---------------- Catalog - get_all_categories_id')
        return Catalog.query.with_entities(Catalog.category_id)

    # -------------------------- Item Methods
    @staticmethod
    def delete_list_of_item_categories(item_id, categories_id_of_item):
        print('--------------- Catalog - delete_list_of_item_categories ')
        for category_id in categories_id_of_item:
            link_to_delete = Catalog.query.filter_by(category_id=category_id, item_id=item_id).first()
            current_db_session = db.session.object_session(link_to_delete)
            current_db_session.delete(link_to_delete)
            current_db_session.commit()

    @staticmethod
    def get_all_items_id():
        """ Return a list of all items id in a Catalog """
        print('---------------- Catalog - get_all_items_id')
        return Catalog.query.with_entities(Catalog.item_id)

    # ------------------------ Auth Methods
    @staticmethod
    def auth_method_get_all_in_dictionary():
        """ Return all link methods in a dictionary """
        return AuthMethod.get_all_in_dictionary()

    # ------------------------ Category Methods
    @staticmethod
    def get_all_categories_name_of_item_id(item_id):
        """ Return a list with all categories name associated with a provided item_id"""
        print('--------------- Catalog - get_all_categories_name_of_item_id')
        # return CatalogMethod.get_all_categories_name_of_item_id(item_id)
        categories_id_list = CatalogMethod.get_all_categories_id_of_item_id(item_id)
        """ Get all categories id associated with an item_id """
        from ..category import CategoryMethod
        categories_name_list = CategoryMethod.get_names_of_categories_id_list(categories_id_list)
        """ Get all categories name provided a categories_id_list """
        return categories_name_list

    @staticmethod
    def category_method_get_all_categories_order_by_name(order):
        """ Return all categories ordered by 'order' """
        print('category_method_get_all_categories_order_by_name(%s) ' % order )
        from ..category import CategoryMethod
        return CategoryMethod.get_all_categories_order_by_name(order)

    # ------------------------ Item Methods
    @staticmethod
    def item_method_get_all_items_name_of_category_id(category_id):
        """ Return a list with all items name associated with a provided category_id """
        print('--------------- Catalog - get_all_items_name_of_category_id')
        items_id_list = CatalogMethod.get_all_items_id_of_category_id(category_id)
        """ Get all items id associated with a category_id """
        from ..item import ItemMethod
        items_name_list = ItemMethod.get_names_of_items_id_list(items_id_list)
        """ Get all items name provided an items_id_list """
        return items_name_list

    @staticmethod
    def item_method_get_all_items_order_by_name(order):
        """ return all items ordered by 'order' """
        from ..item import ItemMethod
        return ItemMethod.get_all_items_order_by_name(order)

    @staticmethod
    def update_catalog(category_item_id, new_categories_items_id_list, category_or_item):
        """
        Update items of a Category
        :param category_item_id: Category_id or Item_id
        :param new_categories_items_id_list:  list of item id's to add to current Category
                or list of category id's to add to current Item
        :param category_or_item: string that identifies if is an update of category or item
        :return: None
        """

        print('------------------ Catalog - update_catalog: %s' % category_or_item)
        current_category_items = []
        if category_or_item == 'category':
            current_category_items = CatalogMethod.get_all_items_id_of_category_id(category_item_id)
            """ Current Category Items """

        elif category_or_item == 'item':
            current_category_items = CatalogMethod.get_all_categories_id_of_item_id(category_item_id)
            """ Current Item Categories """

        categories_items_id_list_to_add = []
        for new_category_item_id in new_categories_items_id_list:
            if new_category_item_id not in current_category_items:
                categories_items_id_list_to_add.append(new_category_item_id)
        """ Validate if 'new_categories_items_id_list' contains any new item, 
                making a comparison between new_categories_items_id_list and 
               'current_category_items' """

        categories_items_id_list_to_delete = []
        for current_category_item_id in current_category_items:
            if current_category_item_id not in new_categories_items_id_list:
                categories_items_id_list_to_delete.append(current_category_item_id)
        """ Validate if 'new_categories_items_id_list' does not contains some of the 'current_category_items' """

        if len(categories_items_id_list_to_add) > 0:
            print('items_id_list_to_add :', categories_items_id_list_to_add)
            if category_or_item == 'category':
                for item_id in categories_items_id_list_to_add:
                    CatalogMethod.add(category_item_id, item_id)
                """ Add new item-category link to Catalog """
            if category_or_item == 'item':
                for category_id in categories_items_id_list_to_add:
                    CatalogMethod.add(category_id, category_item_id)
                """ Add new item-category link to Catalog """
        """ If 'categories_items_list_to_add' contains one or more items, 
               then add item-category link to Catalog """

        if len(categories_items_id_list_to_delete) > 0:
            print('items_id_list_to_delete: ', categories_items_id_list_to_delete)
            if category_or_item == 'category':
                for item_id in categories_items_id_list_to_delete:
                    CatalogMethod.delete(category_item_id, item_id)
                """ Delete item-category link from Catalog"""
            if category_or_item == 'item':
                for category_id in categories_items_id_list_to_delete:
                    CatalogMethod.delete(category_id, category_item_id)
        """ If 'categories_items_list_to_delete' contains one or more items, 
               then delete item-category link from Catalog """
