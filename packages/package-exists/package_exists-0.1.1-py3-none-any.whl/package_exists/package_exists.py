import requests


def package_exists(package_name):

    response = requests.get("https://pypi.org/project/" + package_name)
    if response.status_code == 200:
        print(
            f"Unfortunately, '{package_name}' already exists in the Pypi repository.\nPlease, try another available package name for publishing within pypi.org")
        return True
    else:
        print(f"Fortunately, '{package_name}' does not exist in Pypi repository and is currently available for publishing within pypi.org.\nHurry up, before someone takes it!")
        return False
