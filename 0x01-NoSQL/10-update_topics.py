#!/usr/bin/env python3
"""Module to change all topics to base name."""


def update_topics(mongo_collection, name, topics):
    """
    Updates all topics of a school document based on the school name.

    Args:
        mongo_collection: pymongo collection object
        name: string representing the school name to update
        topics: list of strings representing the topics to update

    Returns:
        The number of documents updated.
    """
    result = mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
    return result.modified_count
