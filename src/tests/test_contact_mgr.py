from conmgr.contact import Contact
from conmgr.contact_mgr import ContactManager
from conmgr.exceptions import DuplicatePhoneError, DuplicateEmailError
import pathlib as pl
import pytest

CONTACTS_ATTR = "contacts"
EMAIL_SET_ATTR = "_email_set"
PHONE_SET_ATTR = "_phone_set"
STORE_ATTR = "store_path"

ADD_CON_METHOD = "add_contact"
FIND_CON_METHOD = "find_contact"
REMOVE_CON_METHOD = "remove_contact"
EDIT_CON_METHOD = "edit_contact"
LIST_ALL_METHOD = "list_all" 

TEST_FIRST_NAMES = ["jake", "luke"]
TEST_LAST_NAMES = ["smith", "jackson"]
TEST_EMAILS = ["jake.smith@mail.com", "luke12jackson@meil.com"]
TEST_PHONES = ["999999999", "123123123"]
TEST_ADDRS = ["pl. Defilad 1, 00-901 Warsaw", "ul. Wiejska 4/6/8, 00-902 Warszawa"]

TEST_DATA = [
        TEST_FIRST_NAMES,
        TEST_LAST_NAMES,
        TEST_EMAILS,
        TEST_PHONES,
        TEST_ADDRS
    ]

TEST_CONTACTS = [Contact(*args) for args in zip(*TEST_DATA)]
TEST_STORE_PATH = "conmgr"

ADD_CON = Contact("mike", "wazowski", "mike@maile.com", "333333333", "somewhere")

@pytest.fixture
def con_mgr(tmp_path):
    store = tmp_path / TEST_STORE_PATH
    store.mkdir()
    return ContactManager(TEST_CONTACTS, str(store))

def test_has_attr(con_mgr):
    assert hasattr(con_mgr, CONTACTS_ATTR)
    assert hasattr(con_mgr, STORE_ATTR)
    assert hasattr(con_mgr, PHONE_SET_ATTR)
    assert hasattr(con_mgr, EMAIL_SET_ATTR)

def test_attr_val(con_mgr, tmp_path):
    store_path = str(tmp_path / TEST_STORE_PATH)
    assert TEST_CONTACTS == getattr(con_mgr, CONTACTS_ATTR)
    assert store_path == str(getattr(con_mgr, STORE_ATTR).parent)

def test_has_add_contact():
    assert ADD_CON_METHOD in vars(ContactManager).keys()

def test_add_contact_val(con_mgr):
    con_mgr.add_contact(ADD_CON)
    assert ADD_CON in con_mgr.contacts
    assert ADD_CON.phone in con_mgr._phone_set
    assert ADD_CON.email in con_mgr._email_set

def test_add_contact_raises(con_mgr):
    _ = ""
    con_mgr.add_contact(ADD_CON)

    with pytest.raises(DuplicatePhoneError):
        con_mgr.add_contact(Contact(_, _, "test@mail.com", ADD_CON.phone, _))

    with pytest.raises(DuplicateEmailError):
        con_mgr.add_contact(Contact(_, _, ADD_CON.email, "666666666", _))

def test_has_find_contact():
    assert FIND_CON_METHOD in vars(ContactManager).keys()

def test_find_contact_no_val(con_mgr):
    with pytest.raises(ValueError):
        con_mgr.find_contact()

def test_find_contact_email(con_mgr):
    test_mail = TEST_EMAILS[0]
    actual = con_mgr.find_contact(email=test_mail)
    assert actual == TEST_CONTACTS[0]

def test_find_contact_phone(con_mgr):
    test_phone = TEST_PHONES[0]
    actual = con_mgr.find_contact(phone=test_phone)
    assert actual == TEST_CONTACTS[0]

def test_has_remove_contact():
    assert REMOVE_CON_METHOD in vars(ContactManager).keys()

def test_remove_contact_phone(con_mgr):
    con_mgr.remove_contact(phone=TEST_PHONES[0])
    assert TEST_CONTACTS[0] not in con_mgr.contacts
    assert TEST_PHONES[0] not in con_mgr._phone_set
    assert TEST_EMAILS[0] not in con_mgr._email_set

def test_remove_contact_email(con_mgr):
    con_mgr.remove_contact(email=TEST_EMAILS[0])
    assert TEST_CONTACTS[0] not in con_mgr.contacts
    assert TEST_PHONES[0] not in con_mgr._phone_set
    assert TEST_EMAILS[0] not in con_mgr._email_set

def test_remove_contact_raises(con_mgr):
    with pytest.raises(ValueError):
        con_mgr.remove_contact()

def test_has_edit_contact():
    assert EDIT_CON_METHOD in vars(ContactManager).keys()

def test_edit_contact_phone(con_mgr):
    val = "test"
    test_phone = TEST_PHONES[0]
    con_mgr.edit_contact(
            test_phone,
            first_name=val,
            last_name=val,
            email=val,
            phone=val,
            address=val)
    ret = con_mgr.find_contact(phone=val)

    assert con_mgr.find_contact(phone=test_phone) is None
    assert ret.first_name == val
    assert ret.last_name == val
    assert ret.email == val
    assert ret.phone == val
    assert ret.address == val

def test_edit_contact_raises(con_mgr):
    with pytest.raises(ValueError):
        con_mgr.edit_contact("test")

def test_has_list_all():
    assert LIST_ALL_METHOD in vars(ContactManager).keys()

def test_to_json(con_mgr):
    ret = con_mgr.to_json()
    assert isinstance(ret, dict)
    assert "contacts" in ret.keys()
    assert "store_path" in ret.keys()

def test_to_file(con_mgr):
    con_mgr.to_file()
    assert con_mgr.store_path.exists()

def test_from_file(con_mgr):
    con_mgr.to_file()
    ret = ContactManager.from_file(con_mgr.store_path)
    assert ret.contacts == con_mgr.contacts
    assert ret.store_path == con_mgr.store_path

def test_from_file_raises(con_mgr):
    with pytest.raises(ValueError):
        con_mgr.from_file(pl.Path("/notavalidpath"))
    with pytest.raises(ValueError):
        con_mgr.from_file(pl.Path("/etc"))
    with pytest.raises(ValueError):
        con_mgr.from_file(pl.Path("/etc/locale.conf"))
