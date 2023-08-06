# coding: utf-8

"""Perform an HTTP GET on an URL and print the status code."""

import sys

import requests


def get_url_and_print_status_code():
    """Perform an HTTP GET and print the return status."""
    response = requests.get(sys.argv[1])
    print(response.status_code)


if __name__ == "__main__":
    get_url_and_print_status_code()
