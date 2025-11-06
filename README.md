## 🗂️ **Project Title:** Contacts Manager

### **Objective**

Build a class-based console application that allows users to create, view, edit, delete, and persist contact information using JSON files. The goal is to strengthen your understanding of **object-oriented programming**, **error handling**, and **data modeling** with `dataclasses` and `typing`.

---

## 🔧 **Core Requirements**

### **1. Data Model**

#### `Contact` Class

* Represents an individual contact.
* Use a **`@dataclass`** for cleaner and more structured code.

**Attributes:**

* `first_name: str`
* `last_name: str`
* `email: str`
* `phone: str`
* `address: str | None` (optional)

**Methods:**

* `__str__`: Return a human-readable string representation of the contact.
* `__repr__`: Return a detailed, developer-friendly representation.
* `to_dict()`: Serialize a contact to a dictionary (for JSON saving).
* `from_dict()`: Class method to create a contact from a dictionary.

---

### **2. Contact Manager Class**

#### `ContactManager` Class

* Responsible for managing all contact operations.

**Attributes:**

* `contacts: list[Contact]`
* `storage_file: str` (path to JSON file, e.g., `"contacts.json"`)

**Methods:**

1. **`add_contact(contact: Contact)`**
   Adds a new contact. Should check for duplicates (based on email or phone).
   → Raises a `DuplicateContactError` if a contact already exists.

2. **`remove_contact(identifier: str)`**
   Removes a contact by email or phone.
   → Raises a `ContactNotFoundError` if not found.

3. **`find_contact(identifier: str) -> Contact`**
   Searches for a contact by email, phone, or name.

4. **`edit_contact(identifier: str, **updates)`**
   Updates specific fields of a contact.

5. **`list_contacts()`**
   Returns a list or formatted string of all saved contacts.

6. **`save_to_file()`**
   Writes all contacts to the specified JSON file.

7. **`load_from_file()`**
   Reads contacts from the JSON file and populates the manager.
   → Should handle file not found, invalid JSON, and permission errors gracefully.

---

## ⚙️ **3. Error Handling**

Implement robust error handling using Python’s exception mechanisms:

### **Custom Exceptions**

* `ContactError` — Base exception class.
* `DuplicateContactError(ContactError)`
* `ContactNotFoundError(ContactError)`
* `InvalidContactDataError(ContactError)`

Use `try/except` blocks where appropriate:

* File operations (`FileNotFoundError`, `JSONDecodeError`).
* Input validation (e.g., invalid email format).
* Missing required fields.

---

## 🧩 **4. Input Validation**

* Validate **email format** (basic regex or `str.contains("@")` for now).
* Ensure **phone numbers** are digits or match a pattern like `+123456789`.
* Trim whitespace and standardize name capitalization.

If data is invalid, raise `InvalidContactDataError`.

---

## 💾 **5. JSON Storage Structure**

Example `contacts.json` file:

```json
[
  {
    "first_name": "Alice",
    "last_name": "Brown",
    "email": "alice.brown@example.com",
    "phone": "+1555123456",
    "address": "42 Main St, Springfield"
  },
  {
    "first_name": "Bob",
    "last_name": "Smith",
    "email": "bob.smith@example.com",
    "phone": "+1555987654",
    "address": null
  }
]
```

---

## 🧠 **6. CLI Interaction (Optional Enhancement)**

A simple command-line interface could allow the user to:

* Add a new contact
* View all contacts
* Search for a contact
* Edit contact details
* Delete a contact
* Save and exit

Implement with a basic input loop:

```python
while True:
    print("1. Add Contact | 2. View All | 3. Search | 4. Edit | 5. Delete | 6. Exit")
    choice = input("Enter option: ")
    # Call ContactManager methods accordingly
```

---

## 🧪 **7. Testing (Recommended)**

Write minimal tests or checks for:

* Adding a contact and saving to file.
* Loading contacts from JSON.
* Handling duplicate emails or missing files.
* Editing and removing contacts.

---

## 🧱 **8. Stretch Goals (Optional)**

* Add search by partial name match.
* Sort contacts alphabetically before displaying.
* Add support for grouping (e.g., “friends”, “work”).
* Add export to CSV.
* Add logging for all actions and errors.
