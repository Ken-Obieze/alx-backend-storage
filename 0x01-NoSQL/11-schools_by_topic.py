#!/usr/bin/env python3
"""Module to returns the list of school having a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns a list of schools that have a specific topic.

    Args:
        mongo_collection: pymongo collection object
        topic: string representing the topic to search

    Returns:
        A list of dictionaries representing the schools that have the specified topic.
    """
    schools = mongo_collection.find({"topics": topic})
    return [school for school in schools]
