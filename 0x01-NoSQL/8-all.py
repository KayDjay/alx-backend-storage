#!/usr/bin/env python3

"""
Python function that lists all documents in a collection
"""


def list_all(mongo_collection):
    """
    Retrieve all documents from MongoDB collection.

    Args:
      mongo_collection (pymongo.collection.Collection):
      The MongoDB collection to retrieve documents from.

    Returns:
      pymongo.cursor.Cursor: A cursor object containing
      all the retrieved documents.
    """

    return [document for document in mongo_collection.find()]