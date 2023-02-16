#!/usr/bin/python3
"""User test"""
from datetime import datetime
import inspect
import models
<<<<<<< HEAD
import pep8 as pycodestyle
from models.base_model import BaseModel
from models.engine.db_storage import DBStorage
import time
import unittest
from unittest import mock
Model = models.city.City
City = models.city.City
module_doc = models.city.__doc__
path1 = "models/city.py"
path2 = "tests/test_models/test_city.py"
=======
from models import city
from models.base_model import BaseModel
import pep8
import unittest
City = city.City

>>>>>>> 7011bd7fa44cfcbd29c7b265614aea8ae8c08092


class DocsTest(unittest.TestCase):
    """Test to check behaviors"""

    @classmethod
    def setUpClass(self):
        """setting up tests"""
        self.self_funcs = inspect.getmembers(Model, inspect.isfunction)

    def test_module_docstring(self):
        """Test module docstring"""
        self.assertIsNot(module_doc, None,
                         "city.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "test_city.py needs a docstring")

        """Test classes doctring"""
        self.assertIsNot(BaseModel.__doc__, None,
                         "City class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) >= 1,
                        "City class needs a docstring")

<<<<<<< HEAD
    def test_func_docstrings(self):
        """test func dostrings"""
        for func in self.self_funcs:
            with self.subTest(function=func):
                self.assertIsNot(
                    func[1].__doc__,
                    None,
                    "{:s} method needs a docstring".format(func[0])
                )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )


@unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
class TestBaseModel(unittest.TestCase):
    """testing BaseModel Class"""
    @mock.patch('models.city')
    def test_instances(self, mock_storage):
        """Testing that object is correctly created"""
        instance = City()
        self.assertIs(type(instance), City)
        instance.name = "Holbies foravaaaa"
        instance.state_id = "111-222"

        expectec_attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "state_id": str,
            "name": str
        }
        # testing types and attr names
        for attr, types in expectec_attrs_types.items():
            with self.subTest(attr=attr, typ=types):
                self.assertIn(attr, instance.__dict__)
                self.assertIs(type(instance.__dict__[attr]), types)
        self.assertEqual(instance.name, "Holbies foravaaaa")
        self.assertEqual(instance.state_id, "111-222")

    def test_datetime(self):
        """testing correct datetime assignation
        correct assignation of created_at and updated_at"""
        created_at = datetime.now()
        instance1 = City()
        updated_at = datetime.now()
        self.assertEqual(created_at <= instance1.created_at <=
                         updated_at, False)
        time.sleep(0.1)
        created_at = datetime.now()
        instance2 = City()
        updated_at = datetime.now()
        self.assertFalse(created_at <= instance2.created_at <= updated_at, True)
        self.assertEqual(instance1.created_at, instance1.created_at)
        self.assertEqual(instance2.updated_at, instance2.updated_at)
        self.assertNotEqual(instance1.created_at, instance2.created_at)
        self.assertNotEqual(instance1.updated_at, instance2.updated_at)

    def test_uuid(self):
        """testing uuid"""
        instance1 = City()
        instance2 = City()
        for instance in [instance1, instance2]:
            tuuid = instance.id
            with self.subTest(uuid=tuuid):
                self.assertIs(type(tuuid), str)

    def test_dictionary(self):
        """testing to_dict correct funtionality"""
        """Testing that object is correctly created"""
        instance3 = City()
        self.assertIs(type(instance3), City)
        instance3.name = "Holbies foravaaaa"
        instance3.state_id = "111-222"
        new_inst = instance3.to_dict()
        expectec_attrs = ["id",
                          "created_at",
                          "updated_at",
                          "name",
                          "state_id",
                          "__class__"]
        self.assertCountEqual(new_inst.keys(), expectec_attrs)
        self.assertEqual(new_inst['__class__'], 'City')
        self.assertEqual(new_inst['name'], 'Holbies foravaaaa')
        self.assertEqual(new_inst['state_id'], '111-222')

    def test_str_method(self):
        """testing str method, checking output"""
        instance4 = City()
        strr = "[City] ({}) {}".format(instance4.id, instance4.__dict__)
        self.assertEqual(strr, str(instance4))

    @mock.patch('models.storage')
    def test_save_method(self, mock_storage):
        """test save method and if it updates
        "updated_at" calling storage.save"""
        instance4 = City()
        created_at = instance4.created_at
        updated_at = instance4.updated_at
        instance4.save()
        new_created_at = instance4.created_at
        new_updated_at = instance4.updated_at
        self.assertNotEqual(updated_at, new_updated_at)
        self.assertEqual(created_at, new_created_at)
        self.assertTrue(mock_storage.save.called)
=======
    def test_city_func_docstrings(self):
        """Test for the presence of docstrings in City methods"""
        for func in self.city_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestCity(unittest.TestCase):
    """Test the City class"""
    def test_is_subclass(self):
        """Test that City is a subclass of BaseModel"""
        city = City()
        self.assertIsInstance(city, BaseModel)
        self.assertTrue(hasattr(city, "id"))
        self.assertTrue(hasattr(city, "created_at"))
        self.assertTrue(hasattr(city, "updated_at"))

    def test_name_attr(self):
        """Test that City has attribute name, and it's an empty string"""
        city = City()
        self.assertTrue(hasattr(city, "name"))
        if models.storage_t == 'db':
            self.assertEqual(city.name, None)
        else:
            self.assertEqual(city.name, "")

    def test_state_id_attr(self):
        """Test that City has attribute state_id, and it's an empty string"""
        city = City()
        self.assertTrue(hasattr(city, "state_id"))
        if models.storage_t == 'db':
            self.assertEqual(city.state_id, None)
        else:
            self.assertEqual(city.state_id, "")

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        c = City()
        new_d = c.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in c.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        c = City()
        new_d = c.to_dict()
        self.assertEqual(new_d["__class__"], "City")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], c.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], c.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        city = City()
        string = "[City] ({}) {}".format(city.id, city.__dict__)
        self.assertEqual(string, str(city))
>>>>>>> 7011bd7fa44cfcbd29c7b265614aea8ae8c08092
