#!/usr/bin/env python3
"""Module to return sorted student by average score."""


def top_students(mongo_collection):
    """Returns all students sorted by average score.

    Args:
        mongo_collection: pymongo collection object.

    Returns:
        List of dictionaries containing student information sorted by average score.
    """
    pipeline = [
        {
            '$addFields': {
                'averageScore': {
                    '$avg': '$topics.score'
                }
            }
        },
        {
            '$sort': {
                'averageScore': -1
            }
        }
    ]
    return list(mongo_collection.aggregate(pipeline))
