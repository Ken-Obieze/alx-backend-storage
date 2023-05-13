#!/usr/bin/env python3
"""
Module for log stats.
"""

from pymongo import MongoClient


def log_stats():
    """
    Provides some stats about the Nginx logs stored in MongoDB.
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    total_logs = logs_collection.count_documents({})

    methods = logs_collection.aggregate([
        {"$group": {"_id": "$method", "count": {"$sum": 1}}}
    ])

    status = logs_collection.aggregate([
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ])

    ips = logs_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    print(f"{total_logs} logs")

    print("Methods:")
    for method in methods:
        print(f"\tmethod {method['_id']}: {method['count']}")

    print("Status check:")
    for code in status:
        if str(code['_id'])[0] == '4':
            print(f"\t{code['_id']}: {code['count']}")

    print("IPs:")
    for ip in ips:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    log_stats()

