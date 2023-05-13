#!/usr/bin/env python3
"""Module to return logs."""
from pymongo import MongoClient


def print_logs_stats(collection):
    """
    Prints some stats about the Nginx logs stored in the given collection.
    """
    count = collection.count_documents({})
    print(f"{count} logs")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"    method {method}: {count}")

    count = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{count} status check")


if __name__ == "__main__":
    client = MongoClient()
    db = client.logs
    collection = db.nginx
    print_logs_stats(collection)
    client.close()
