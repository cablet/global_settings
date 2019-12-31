

"""
A quick Singlton class for reading yaml or json files. This will make is quick and easy
to use settings files throughout a program
"""
import sys
import importlib.util
import json



class Borg:
    _shared_data = {}

    def __init__(self):
        self.__dict__ = self._shared_data

        
class GlobalSettings(Borg):
    """This class now shares all its attributes among its various instances"""

    def __init__(self, **kwargs):
        Borg.__init__(self)
        self._shared_data.update(kwargs)

    def __str__(self):
        return str(self._shared_data)

    def get(self, name, default=None):
        """ return value for key if it exists, if not return default """
        return self._shared_data.get(name, default)

    def set(self, name, value):
        """ set value for key. If key does not exist, a new dict entry will be created """
        self._shared_data[name] = value

    def read_yaml_file(self, path):
        """ read in a yaml text file and populate Singleton's dict with entries.
        """
        name = 'yaml'
        spec = importlib.util.find_spec(name)
        if spec is not None:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            sys.modules[name] = module
            import yaml

            try:
                read_file = open(path, 'r')
                ldata = yaml.load(read_file, Loader=yaml.SafeLoader)

            except IOError as e:
                err = "I/O error({0}): {1} {2}".format(e.errno, e.strerror, path)
                print(err)

            except yaml.YAMLError as e:
                err = "Error in configuration file: {}".format(e)
                print(err)

            else:
                self._shared_data.update(ldata)
        else:
            print("PyYaml module not found. Unable to read yaml file")



    def read_json_file(self, path):
        """ read in a json text file and populate Singleton's dict with entries"""
        try:
            read_file = open(path, 'r')
            ldata = json.load(read_file)

        except IOError as e:
            err = "I/O error({0}): {1} {2}".format(e.errno, e.strerror, path)
            print(err)

        except json.JSONDecodeError:
            err = "JSON Error: Error decoding JSON file. Please check the formatting of the file"
            print(err)


        else:
            self._shared_data.update(ldata)









"""" Testing"""


#Let's create a singleton object and add our first acronym
x = GlobalSettings(HTTP="Hyper Text Transfer Protocol")
# Print the object
print(x) 

#Let's create another singleton object and if it refers to the same attribute dictionary by adding another acronym.
y = GlobalSettings(SNMP="Simple Network Management Protocol")
# Print the object
print(y)

z = GlobalSettings(Dork='You are such a frickin\' dork!')
print(z)




z.read_json_file("test_data.json")
print(z)

z.read_yaml_file("test_data.yml")
print(z)
