"""
Contact module.

Contains the Contact class.
"""
import re

FIRST_NAME_ATTR = "first_name"
LAST_NAME_ATTR = "last_name"
EMAIL_ATTR = "email"
PHONE_ATTR = "phone"
ADDR_ATTR = "address"

ATTR_LIST = [
    FIRST_NAME_ATTR,
    LAST_NAME_ATTR,
    EMAIL_ATTR,
    PHONE_ATTR,
    ADDR_ATTR
]

ATTR_SET = set(ATTR_LIST)

class Contact:
    """
    A contact class.

    Attributes
    ----------
    first_name : str
    last_name : str
    email : str
    phone : str
    address : str, optional

    Methods
    -------
    from_dict(d)
        Creates a new class instance based on a dictionary.
    to_dict()
        Creates a dictionary representation of a class instance.
    """

    def __init__(self,
            first: str,
            last: str,
            email: str,
            phone: str,
            addr: str | None = None):

        if not re.match(r".*@.*\..*", email):
            raise ValueError(f"Email {email} is invalid.")
        
        if not re.match(r"\d{9}", phone):
            raise ValueError(f"Phone {phone} is invalid.")

        self.first_name = first
        self.last_name = last
        self.email = email
        self.phone = phone
        self.address = addr

    def __str__(self):
        ret = f"""
        Contact:
            - first name:   {self.first_name}
            - last name:    {self.last_name}
            - email:        {self.email} 
            - phone:        {self.phone}
            - address:      {self.address}
        """
        return ret

    def __repr__(self):
        return (f"Contact(first={self.first_name!r}," 
                f" last={self.last_name!r},"
                f" email={self.email!r},"
                f" phone={self.phone!r},"
                f" address={self.address!r})"
        )

    def __eq__(self, other: object):
        if not isinstance(other, Contact):
            return NotImplemented

        return (self.phone == other.phone) or (self.email == other.email)

    def __hash__(self):
        return hash((self.first_name, self.last_name, self.email, self.phone, self.address))

    @classmethod
    def from_dict(cls, d: dict[str, str]):
        """Creates a class instance from a dictionary.

        Parameters
        ----------
        d : dict[str, str]
            Dictionary to create from

        Returns
        -------
        Contact
            A contact instance.

        Raises
        ------
        ValueError
            If wrong argument names are passed to the function.
        """

        if set(ATTR_SET) != set(d.keys()):
            raise ValueError("Bad argument names passed to the constructor.")

        return cls(d[FIRST_NAME_ATTR],
                   d[LAST_NAME_ATTR],
                   d[EMAIL_ATTR],
                   d[PHONE_ATTR],
                   d[ADDR_ATTR])

    def to_dict(self) -> dict[str, str | None]:
        """Transform the class into a dictionary.

        Takes no parameters.

        Returns
        -------
        dict[str, str]
            A dictionary representation of the class.
        """

        return {
            "first_name" : self.first_name,
            "last_name" : self.last_name,
            "email" : self.email,
            "phone" : self.phone,
            "address" : self.address
        }
