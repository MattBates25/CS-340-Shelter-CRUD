# animal_shelter.py
from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import ConnectionFailure, OperationFailure


class AnimalShelter(object):  # CRUD operations
    def __init__(self):  # Creates connection to the MongoDB database AAC.
        USER = 'aacuser'
        PASS = 'mtb123'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 31273
        DB = 'AAC'
        COL = 'animals'
        try:  # Attempts connection
            self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER, PASS, HOST, PORT))
            self.database = self.client['%s' % (DB)]
            self.collection = self.database['%s' % (COL)]
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")
            raise

    def create(self, data):  # Inserts document into the collection.
        if data is not None:
            try:  # Attempt to insert document.
                result = self.collection.insert_one(data)
                return result.acknowledged
            except OperationFailure as e:
                print(f"Insert operation failed: {e}")
                return False  # Returns false if there is an operations failure.
        else:
            raise ValueError("Nothing to save, because data parameter is empty.")

    def read(self, query):  # Queries a document from the collection
        if query is not None:
            try:  # Executes the query.
                cursor = self.collection.find(query)
                return list(cursor)
            except OperationFailure as e:
                print(f"Query operation failed: {e}")
                return []  # Returns an empty list if there was an operation failure.
        else:
            raise ValueError("Query parameter is empty.")  # Error if query is None.

    def update(self, query, update_data):  # Queries and then updates a document.
        if query is not None and update_data is not None:
            try:
                result = self.collection.update_many(query, {'$set': update_data})
                return result.modified_count
            except OperationFailure as e:
                print(f"Update operation failed: {e}")
                return 0
        else:
            raise ValueError("The query and/or update_data parameters are empty.")

    def delete(self, query):  # Deletes a document from the collection.
        if query is not None:
            try:
                result = self.collection.delete_many(query)
                return result.deleted_count
            except OperationFailure as e:
                print(f"Delete operation failed: {e}")
                return 0
        else:
            raise ValueError("The query parameter is empty.")
