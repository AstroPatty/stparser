str2type does exactly what it says in the name: it converts strings to types. The most obvious use case is converting type specifications in configuration files. 

str2type includes two functions: get_type and check_type.


get_type turns a string into a type, or a list of strings into a list of types. It works with built in types as well as those defined in an external module. ::
  
  >>> from str2type import get_type
  >>> get_type("int")
  <class 'int'>
  
  >>> get_type(["int", "float", "str"])
  [<class 'int'>, <class 'float'>, <class 'str'>]
  
  >>> get_type("numpy.ndarray")
  <class 'numpy.ndarray'>
  
