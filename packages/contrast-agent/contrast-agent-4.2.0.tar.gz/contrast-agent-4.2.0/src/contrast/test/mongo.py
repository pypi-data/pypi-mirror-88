# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os
import pytest

from pymongo import MongoClient


def mongo_db_exists():
    client = create_mongo_client(serverSelectionTimeoutMS=20)
    db = client.pymongo_test

    try:
        db.posts.count()
    except Exception as e:
        print("EXCEPTION", e)
        return False

    return True


def create_mongo_client(**kwargs):
    mongo_host = [os.environ.get("MONGODB_HOST", "localhost:27017")]
    return MongoClient(host=mongo_host, **kwargs)


skip_no_mongo_db = pytest.mark.skipif(
    not mongo_db_exists(), reason="Host does not have mongodb"
)
