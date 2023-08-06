from .build import Indexer

__all__ = ["get_or_create_indexer", "get_search_attribute"]


def get_or_create_indexer():
    return Indexer()


def get_search_attribute():
    return Indexer.__SEARCH_ATTRIBUTE__
