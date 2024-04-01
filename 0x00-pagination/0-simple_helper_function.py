#!/usr/bin/env python3

""" An helper function
"""


def index_range(page, page_size):
    """ Returs index range of a page
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return (start_index, end_index)
