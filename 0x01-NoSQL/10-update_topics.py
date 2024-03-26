#!/usr/bin/env python3

"""
Change School Topics
"""


def update_topics(mongo_collection, name, topics):
    """
    Function that changes all topics of a school
    document based on the name
    """
    mongo_collection.update_many(
      {"name": name},
      {"$set": {"topics": topics}}
      )