#!/usr/bin/env python3
"""Module to list document."""


def list_all(mongo_collection):
    cursor = mongo_collection.find()
    documents = [document for document in cursor]
    return documents
