from conmgr.contact import Contact
import pytest

FIRST_NAME_ATTR = "first_name"
LAST_NAME_ATTR = "last_name"
EMAIL_ATTR = "email"
PHONE_ATTR = "phone"
ADDR_ATTR = "address"

TEST_FIRST_NAME = "jake"
TEST_LAST_NAME = "smith"
TEST_EMAIL = "jake.smith@mail.com"
TEST_PHONE = "999999999"
TEST_ADDR = "pl. Defilad 1, 00-901 Warsaw"

CON_ATTRIBUTES = {
    FIRST_NAME_ATTR : TEST_FIRST_NAME,
    LAST_NAME_ATTR : TEST_LAST_NAME,
    EMAIL_ATTR : TEST_EMAIL,
    PHONE_ATTR : TEST_PHONE,
    ADDR_ATTR : TEST_ADDR
}

STR_METHOD = "__str__"
REPR_METHOD = "__repr__"
EQ_METHOD = "__eq__"
HASH_METHOD = "__hash__"
TO_DICT_METHOD = "to_dict"
FROM_DICT_METHOD = "from_dict"

@pytest.fixture
def contact():
    return Contact(
            TEST_FIRST_NAME,
            TEST_LAST_NAME,
            TEST_EMAIL,
            TEST_PHONE,
            TEST_ADDR)

@pytest.fixture
def contact_opt():
    return Contact(
            TEST_FIRST_NAME,
            TEST_LAST_NAME,
            TEST_EMAIL,
            TEST_PHONE)

def test_contact_has_attr(contact):
    for attr in CON_ATTRIBUTES.keys():
        assert hasattr(contact, attr)

def test_contact_attr_val(contact):
    for attr, actual_val in CON_ATTRIBUTES.items():
        assert actual_val == getattr(contact, attr) 

def test_email_invalid():
    _ = ""
    with pytest.raises(ValueError):
        Contact(_, _, "asdf", TEST_PHONE, _)

def test_phone_invalid():
    _ = ""
    with pytest.raises(ValueError):
        Contact(_, _, "asdf", TEST_PHONE, _)

def test_contact_attr_opt(contact_opt):
    assert hasattr(contact_opt, ADDR_ATTR)
    assert contact_opt.address is None

def test_contact_has_str():
    assert STR_METHOD in vars(Contact).keys()

def test_contact_has_repr():
    assert REPR_METHOD in vars(Contact).keys()

def test_contact_has_eq():
    assert EQ_METHOD in vars(Contact).keys()

def test_contact_eq_val(contact):
    _ = ""

    c1 = Contact(
            _,
            _,
            TEST_EMAIL,
            "123123123",
            _)

    c2 = Contact(
            _,
            _,
            "test@mail.com",
            TEST_PHONE,
            _)

    assert c1 == contact
    assert c2 == contact
    assert c1 != c2

def test_contact_has_hash():
    assert HASH_METHOD in vars(Contact).keys()

def test_contact_hash_val():
    c1 = Contact(
            TEST_FIRST_NAME,
            TEST_LAST_NAME,
            TEST_EMAIL,
            TEST_PHONE,
            TEST_ADDR)

    c2 = Contact(
            TEST_FIRST_NAME,
            TEST_LAST_NAME,
            TEST_EMAIL,
            TEST_PHONE,
            TEST_ADDR)

    assert hash(c1) == hash(c2)

def test_contact_has_to_dict():
    assert TO_DICT_METHOD in vars(Contact).keys()

def test_contact_to_dict_val(contact):
    ret = contact.to_dict()
    assert ret == CON_ATTRIBUTES

def test_contact_has_from_dict():
    assert FROM_DICT_METHOD in vars(Contact).keys()

def test_contact_from_dict_val(contact):
    contact_from_dict = Contact.from_dict(CON_ATTRIBUTES)
    assert contact == contact_from_dict
