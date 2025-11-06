"""
Exceptions module.

Contains custom exceptions used in ContactManager class.
"""

from conmgr.contact import Contact

class ContactError(Exception):
    """
    Base class for Contact exceptions.
    """
    pass

class DuplicateEmailError(ContactError):
    """
    An exception thrown when an attempt to add a contact with an email
    already present in the instance is made.
    """

    def __init__(self, con: Contact):
        super().__init__(f"Email {con.email} already exists.")

class DuplicatePhoneError(ContactError):
    """
    An exception thrown when an attempt to add a contact with a phone number
    already present in the instance is made.
    """

    def __init__(self, con: Contact):
        super().__init__(f"Phone {con.phone} already exists.")
