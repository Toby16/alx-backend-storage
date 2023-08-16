#!/usr/bin/env python3
"""
List all documents in Python
"""


def list_all(mongo_collection):
    """
    Lists all documents in a collection
    """
    list_value = [doc for doc in mongo_collection.find()]
    return list_value
