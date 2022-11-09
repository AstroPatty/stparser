stparser
========

stparser is a small utility for converting strings to types. I built this because I wanted to be able to include type names in arbitrary configuration files, and have them parsed into something I can actully check arguments against.

stparser includes three functions: get_type, check_type, and parse_types.


get_type turns a string into a type, or a list of strings into a list of types. It works with built in types as well as those defined in an external module. ::
  
  >>> from stparser import get_type
  >>> get_type("int")
  <class 'int'>
  
  >>> get_type(["int", "float", "str"])
  [<class 'int'>, <class 'float'>, <class 'str'>]
  
  >>> get_type("numpy.ndarray")
  <class 'numpy.ndarray'>
  
check_type will check any object against anything that is a valid input for get_type. It does not check that the object is *actually* of the given type, just that it can be cast to that type. ::

  >>> from stparser import check_type
  >>> check_type("float", 5.0)
  True  
  
  >>> check_type("float", 5)
  True
  
  >>> check_type(["float", "list"], 5)
  True
  
  >>> check_type("numpy.ndarray", [1, 2, 3,4])
  True
  
  >>> check_type("list", 5)
  TypeError: Type int cannot be cast as type list
  
parse_types will take a list-type or dict-type object and return a copy object with types parsed. It is similar to get_type, except that it will simply pass over strings that cannot be parsed instead of throwing an error. ::

  >>> stparser.parse_types([1, 2, 3, "str", "int"])
  [1, 2, 3, <class 'str'>, <class 'int'>]
  
  >>> stparser.parse_types({1: "a", 2: "b", 3: "bool"})
  {1: 'a', 2: 'b', 3: <class 'bool'>}
  
For dictionaries, this works recursively::

  >>> stparser.parse_types({1: "a", 2: "b", 3: {1: "a", 2: "b", 3:  "bool", 4: "int"}})
  {1: 'a', 2: 'b', 3: {1: 'a', 2: 'b', 3: <class 'bool'>, 4: <class 'int'>}}
