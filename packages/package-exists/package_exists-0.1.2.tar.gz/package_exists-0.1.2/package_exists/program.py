"""
This module when executed is a program that tests possible package names existing in Pypi repository.

It only stops when you write 'exit'.
"""


from pe_functions import exists
# Here is ambiguous, but refers from package_exists.py module import package_exists() function
# Since the "package_exists" package has the same name it can be very confusing so is better to rename either the module or the function
# while leaving the same name for the package.

package_name = ""
while package_name.lower() != "exit":
    package_name = input(
        "\n\nPlease input the package name to verify whether it currently exists in the Pypi repository:\n\n")
    # print("\n")
    print("")
    exists(package_name)
