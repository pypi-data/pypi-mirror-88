""" This module named 'pe_functions' contains a function for determining existence of a package name in Pypi repository."""

import requests

"""
Dependencies:
- requests
"""


def exists(package_name):
    """
    This function determines existence of a package name in Pypi repository and prints a warning of package name availability.

    Parameters:
    package_name (str): Name of package as found in Pypi repository.

    Returns:
    Boolean: True if it exists of False if it does not exist.
    """

    response = requests.get("https://pypi.org/project/" + package_name)
    if response.status_code == 200:
        print(
            f"Unfortunately, '{package_name}' already exists in the Pypi repository.\nPlease, try another available package name for publishing within pypi.org")
        return True
    else:
        print(f"Fortunately, '{package_name}' does not exist in Pypi repository and is currently available for publishing within pypi.org.\nHurry up, before someone takes it!")
        return False
