"""
MongoDB helper functions for storing unstructured data related to properties
(e.g. supporting legal/inspection documents, and an activity log of views/actions).
This is separate from the relational MySQL data (Property, Transaction models)
and demonstrates the hybrid MySQL + MongoDB architecture.
"""
from datetime import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient
from django.conf import settings

_client = None


def get_client():
    global _client
    if _client is None:
        _client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=3000)
    return _client


def get_db():
    return get_client()[settings.MONGO_DB_NAME]


# ---------- Property documents (e.g. legal docs, inspection reports) ----------

def add_document(property_id, title, description=""):
    db = get_db()
    doc = {
        "property_id": property_id,
        "title": title,
        "description": description,
        "created_at": datetime.utcnow(),
    }
    result = db.property_documents.insert_one(doc)
    return str(result.inserted_id)


def get_documents(property_id):
    db = get_db()
    docs = list(db.property_documents.find({"property_id": property_id}).sort("created_at", -1))
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs


def delete_document(document_id):
    db = get_db()
    db.property_documents.delete_one({"_id": ObjectId(document_id)})


# ---------- Activity log (property views, transaction events) ----------

def log_activity(property_id, action, actor_username, extra=None):
    db = get_db()
    entry = {
        "property_id": property_id,
        "action": action,
        "actor": actor_username,
        "extra": extra or {},
        "timestamp": datetime.utcnow(),
    }
    db.activity_log.insert_one(entry)


def get_activity_for_property(property_id, limit=20):
    db = get_db()
    entries = list(
        db.activity_log.find({"property_id": property_id}).sort("timestamp", -1).limit(limit)
    )
    for e in entries:
        e["_id"] = str(e["_id"])
    return entries
