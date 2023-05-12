#!/usr/bin/env python3
"""Module for insertion."""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document into a MongoDB collection based on kwargs.

    Args:
        mongo_collection: pymongo collection object
        **kwargs: keyword arguments to add to the document

    Returns:
        The _id of the newly inserted document.
    """
    document = {}
    for key, value in kwargs.items():
        document[key] = value
    result = mongo_collection.insert_one(document)
    return result.inserted_id

