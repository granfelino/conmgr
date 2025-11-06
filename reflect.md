* Could create dictionaries with mappings phone : contact and email : contact for o(1) lookup,
    but I had a chance to use generators with next() which is a really nice pattern to know
* still not good at tdd as it's getting tedious really fast, whih is an indicator i am doing it wrong.
    in tdd i should define behavior i expect. if it's getting too tedious there's a good chance i am doing
    it wrong
* learned about structuring classes, methods, classmethods
* learned this nice pattern: next(x for x in arr if x == cond)
    - good to know if eg. it is guaranteed that the iterable will have 1 element
* used JSON
* used regex
* used and defined __hash__ to use my class in sets
* learned that __repr__ is used to print a string that would help recreate an object instance 
* learned that classmethods are different than static methods in a sense that they have access to the class definition(class attributes, methods)
* static methods do not have access to class instances or class definitions
* learned some more about zipping and unpacking 
    TEST\_CONTACTS = [Contact(*args) for args in zip(*TEST\_DATA)]
    - unpacks TEST\_DATA -> returns a couple of lists
    - zip() binds in tuples elements of respective indices
    - Contact(*args) -> unpacks the tuples of respective elements and uses them as arguments to the constructor

* learned that i can define more complex types by using `type = ...`
* learned how hinting private and protected access is defined and used in python
* learned that private variables and methods are name-mangled but protected ones are not
