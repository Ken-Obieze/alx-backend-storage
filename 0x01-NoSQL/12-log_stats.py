#!/usr/bin/env python3
"""Module to return logs."""


from pymongo import MongoClient

def print_stats(collection):
    """Print some stats about the Nginx logs stored in MongoDB"""
    total_logs = collection.count_documents({})

    print(f"{total_logs} logs")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"\t{count}\t{method}")

    count = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"\t{count}\tmethod=GET, path=/status")

if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    db = client.logs
    collection = db.nginx
    print_stats(collection)
