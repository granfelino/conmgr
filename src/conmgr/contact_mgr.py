"""
Contact manager module.

Contains the ContactManager class used to manage Contact class instances.
"""

from conmgr.contact import Contact
from conmgr.exceptions import DuplicatePhoneError, DuplicateEmailError
import copy
import json
import pathlib as pl

type ConMgrJSON = dict[str, list[dict[str, str | None]] | str]

class ContactManager:
    """
    ContactManager class.

    Attributes
    ----------
    contacts : list[Contact]
        A list of contacts managed and stored by the class instance.
    store_path : pl.Path
        A path pointing to a valid file location for storing.
    _phone_set : set[str]
        A set containing phone numbers of all contacts.
    _email_set : set[str]
        A set containing emails of all contacts.

    Methods
    -------
    from_file(path)
        A class method used to create a class instance from a file using the
        `path` argument.
    add_contact(new)
        Adds contact from a Contact instance and performs duplicate checks
        based on phone or email.
    __find_contact_email(email)
        A private function used to find a contact based on its email.
    __find_contact_phone(phone)
        A private function used to find a contact based on its phone number.
    find_contact(phone, email)
        A wrapper function for finding contacts based on an email or a phone 
        number. Performs checks if a contact /w given parameters exists.
    __remove_contact(con)
        A private function used for removing a contact from the class instance.
        Should only be used after checking if a contact is present already.
    remove_contact(phone, email)
        A wrapper function for removing a contact. Performs checks, if a contact
        with such phone or email exists and proceeds with removal if condition
        is true.
    __swap_phone(c, new)
        A private function for swapping a phone number of a contact.
    __swap_email(c, new)
        A private function for swapping an email of a contact.
    edit_contact(phone_id, **updates)
        A function used for updating a contact's attributes. Checks if the 
        phone number is present in contacts and does not update 
        invalid attributes - in such case prints a message to the user.
    list_all()
        Prints a readable version of all contacts contained by the class
        instance.
    to_json()
        Creates a dictionary representation of the class instance, ready to
        be transformed into JSON format.
    to_file()
        Calls to_json() and writes its output to a file, under the path stored
        in the store_path attribute.
    """

    def __init__(self, contacts: list[Contact], store_path: str):
        self.contacts = copy.deepcopy(contacts)
        self.store_path = pl.Path(store_path) / "contacts.json"
        self._phone_set = {x.phone for x in contacts}
        self._email_set = {x.email for x in contacts}

        if len(contacts) != len(self._phone_set):
            raise ValueError("Duplicate phone numbers in contacts list.")
        if len(contacts) != len(self._email_set):
            raise ValueError("Duplicate emails in contacts list.")
        
        tmp_path = pl.Path(store_path)
        if not tmp_path.exists():
            raise ValueError(f"Path does not exist: '{store_path}'")
        if not tmp_path.is_dir():
            raise ValueError("Path does not point to a directory.")

    @classmethod
    def from_file(cls, path: pl.Path):
        """
        A class method used to create a class instance from a file using the
        `path` argument.

        Parameters
        ----------
        path : pl.Path
            A pathlib's Path instance pointing to a file in memory to be loaded
            and transformed into a class instance.

        Returns
        -------
        ContactManager
            An instance of a class.

        Raises
        ------
        ValueError
            If:
                - path does not exists
                - path does not point to a file
                - path does not point to a .json file
                - there are no `contacts` in the JSON file
                - there is not `store_path` in the JSON file
        """

        if not path.exists():
            raise ValueError(f"Path {path} does not exists.")
        if not path.is_file():
            raise ValueError(f"Path {path} does not point to a file.")
        if not path.suffix == ".json":
            raise ValueError(f"Path {path} does not point to a JSON file.")

        ret = None
        with open(path, "r") as f:
            ret = json.load(f)

        if "contacts" not in ret.keys():
            raise ValueError("No contacts in the JSON file.")
        if "store_path" not in ret.keys():
            raise ValueError("No store_path in the JSON file.")

        cons = [Contact.from_dict(x) for x in ret["contacts"]]
        store = pl.Path(ret["store_path"]).parent
        return ContactManager(cons, str(store))


    def add_contact(self, new: Contact) -> None:
        """
        Adds contact from a Contact instance and performs duplicate checks
        based on phone or email. Returns nothing.

        Parameters
        ----------
        new : Contact
            A Contact instance to be added.

        Raises
        ------
        DuplicatePhoneError
            If the new contact's phone is already present.
        DuplicateEmailError
            If the new contact's email is already present.
        """

        if new.phone in self._phone_set:
            raise DuplicatePhoneError(new)

        if new.email in self._email_set:
            raise DuplicateEmailError(new)

        self.contacts.append(new)
        self._phone_set.add(new.phone)
        self._email_set.add(new.email)

    def __find_contact_email(self, email: str) -> Contact:
        """A private function used to find a contact based on its email."""

        return next(x for x in self.contacts if x.email == email)

    def __find_contact_phone(self, phone: str) -> Contact:
        """A private function used to find a contact based on its phone."""

        return next(x for x in self.contacts if x.phone == phone)

    def find_contact(self,
                phone: str | None = None,
                email: str | None = None) -> Contact | None:
        """
        A wrapper function for finding contacts based on an email or a phone 
        number. Performs checks if a contact /w given parameters exists.

        Parameters
        ----------
        phone : str, optional
            A phone number to base the search on.
        email : str, optional
            An email to base the search on.

        Returns
        -------
        Contact, optional
            A contact if found, None, if not.

        Raises
        ------
        ValueError
            If neither phone or email is passed to the function.
        """

        if not phone and not email:
            raise ValueError("Provide at least a phone number or an email.")

        if phone is not None:
            return self.__find_contact_phone(phone) if phone in self._phone_set else None

        return self.__find_contact_email(email) if email in self._email_set else None

    def __remove_contact(self, con: Contact):
        """
        A private function used for removing a contact from the class instance.
        Should only be used after checking if a contact is present already.
        """

        self._phone_set.remove(con.phone)
        self._email_set.remove(con.email)
        self.contacts.remove(con)

    def remove_contact(self, 
                phone: str | None = None,
                email: str | None = None) -> None:
        """
        A wrapper function for removing a contact. Performs checks, if a contact
        with such phone or email exists and proceeds with removal if condition
        is true. Returns nothing.

        Parameters
        ----------
        phone : str, optional
            A phone to base the removal on.
        email : str, optional
            An email to base the removal on.

        Raises
        ------
        ValueError
            If neither a phone or an email is passed to the funtcion.
        """

        if not phone and not email:
            raise ValueError("Provide at least a phone number or an email.")

        if phone is not None:
            ret = self.find_contact(phone=phone)
            if ret is not None:
                self.__remove_contact(ret)
                return

        ret = self.find_contact(email=email)
        if ret is not None:
            self.__remove_contact(ret)
            return

    def __swap_phone(self, c: Contact, new: str) -> None:
        """A private function for swapping a phone number of a contact."""
        self._phone_set.remove(c.phone)
        self._phone_set.add(new)

    def __swap_email(self, c: Contact, new: str) -> None:
        """A private function for swapping an email of a contact."""
        self._email_set.remove(c.email)
        self._email_set.add(new)

    def edit_contact(self, phone_id: str, **updates) -> None:
        """
        A function used for updating a contact's attributes. Checks if the 
        phone number is present in contacts and does not update 
        invalid attributes - in such case prints a message to the user.

        Returns nothing.

        Parameters
        ----------
        phone_id : str
            A phone to find a contact to edit.
        **updates
            A list of attributes with new values to be writtn to the contact.
            The list of valid attributes is this of a Contact class.
            
        Raises
        ------
        ValueError
            If the contact based on the phone_id does not exist.
        """

        c = self.find_contact(phone=phone_id)
        if c is None:
            raise ValueError("Invalid phone identifier.")

        for a, v in updates.items():
            match a:
                case "first_name":
                    c.first_name = v
                case "last_name":
                    c.last_name = v
                case "email":
                    self.__swap_email(c, v)
                    c.email = v
                case "phone":
                    self.__swap_phone(c, v)
                    c.phone = v
                case "address":
                    c.address = v
                case _:
                    print(f"Invalid attribute '{a}'")
    def list_all(self) -> None:
        """Prints a readable version of all contacts contained by the class instance."""

        for c in self.contacts:
            print("====================================")
            print(c)
            print("====================================")

    def to_json(self) -> ConMgrJSON:
        """
        Creates a dictionary representation of the class instance, ready to 
        be transformed into JSON format.
        """

        return {
                "contacts" : [x.to_dict() for x in self.contacts],
                "store_path" : str(self.store_path),
            }

    def to_file(self) -> None:
        """
        Calls to_json() and writes its output to a file, under the path stored
        in the store_path attribute.
        """

        json_str = self.to_json()
        path = str(json_str["store_path"])      #XXX mypy complained that json_str["store_path"] has incompatible type
        with open(path, "w") as f:
            json.dump(json_str, f)
