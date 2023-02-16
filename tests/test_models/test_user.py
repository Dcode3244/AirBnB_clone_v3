#!/usr/bin/python3
"""User test"""
from datetime import datetime
import inspect
import models
import pep8 as pycodestyle
from models.base_model import BaseModel
<<<<<<< HEAD
from models.engine.db_storage import DBStorage
import time
=======
import pep8
>>>>>>> 7011bd7fa44cfcbd29c7b265614aea8ae8c08092
import unittest
from unittest import mock
Model = models.user.User
User = models.user.User
module_doc = models.user.__doc__
path1 = "models/user.py"
path2 = "tests/test_models/test_user.py"


class DocsTest(unittest.TestCase):
    """Test to check behaviors"""

    @classmethod
    def setUpClass(self):
        """setting up tests"""
        self.self_funcs = inspect.getmembers(Model, inspect.isfunction)

    def test_module_docstring(self):
        """Test module docstring"""
        self.assertIsNot(module_doc, None,
                         "user.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "test_user.py needs a docstring")

        """Test classes doctring"""
        self.assertIsNot(BaseModel.__doc__, None,
                         "User class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) >= 1,
                        "User class needs a docstring")

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
class TestClassModel(unittest.TestCase):
    """testing BaseModel Class"""
    @mock.patch('models.user')
    def test_instances(self, mock_storage):
        """Testing that object is correctly created"""
        instance = User()
        self.assertIs(type(instance), User)
        instance.name = "Holberton"
        instance.number = 89
        instance.email = "Holberton@holbertonshool.com"
        instance.password = "tubbcito-plumplum"
        instance.first_name = "joshua"
        instance.last_name = "joshua2"

        expectec_attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "number": int,
            "email": str,
            "password": str,
            "first_name": str,
            "last_name": str
        }
        # testing types and attr names
        for attr, types in expectec_attrs_types.items():
            with self.subTest(attr=attr, typ=types):
                self.assertIn(attr, instance.__dict__)
                self.assertIs(type(instance.__dict__[attr]), types)
        self.assertEqual(instance.name, "Holberton")
        self.assertEqual(instance.number, 89)
        self.assertEqual(instance.email, "Holberton@holbertonshool.com")
        self.assertEqual(instance.first_name, "joshua")
        self.assertEqual(instance.last_name, "joshua2")

    def test_datetime(self):
        """testing correct datetime assignation
        correct assignation of created_at and updated_at"""
        created_at = datetime.now()
        instance1 = User()
        updated_at = datetime.now()
        self.assertEqual(created_at <= instance1.created_at <=
                         updated_at, False)
        time.sleep(0.1)
        created_at = datetime.now()
        instance2 = User()
        updated_at = datetime.now()
        self.assertFalse(created_at <= instance2.created_at <= updated_at, True)
        self.assertEqual(instance1.created_at, instance1.created_at)
        self.assertEqual(instance2.updated_at, instance2.updated_at)
        self.assertNotEqual(instance1.created_at, instance2.created_at)
        self.assertNotEqual(instance1.updated_at, instance2.updated_at)

    def test_uuid(self):
        """testing uuid"""
        instance1 = User()
        instance2 = User()
        for instance in [instance1, instance2]:
            tuuid = instance.id
            with self.subTest(uuid=tuuid):
                self.assertIs(type(tuuid), str)

        self.assertNotEqual(instance1.id, instance2.id)

    def test_dictionary(self):
        """testing to_dict correct funtionality"""
        """Testing that object is correctly created"""
        instance3 = User()
        self.assertIs(type(instance3), User)
        instance3.name = "Holbies"
        instance3.number = 89
        instance3.email = "Holberton@holbertonshool.com"
        instance3.password = "tubbcito-plumplum"
        instance3.first_name = "joshua"
        instance3.last_name = "joshua2"
        new_inst = instance3.to_dict()
        expectec_attrs = ["id",
                          "created_at",
                          "updated_at",
                          "name",
                          "number",
                          "email",
                          "password",
                          "first_name",
                          "last_name",
                          "__class__"]
        self.assertCountEqual(new_inst.keys(), expectec_attrs)
        self.assertEqual(new_inst['__class__'], 'User')
        self.assertEqual(new_inst['last_name'], 'joshua2')
        self.assertEqual(new_inst['first_name'], 'joshua')
        self.assertEqual(new_inst['name'], 'Holbies')
        self.assertEqual(new_inst['number'], 89)
        self.assertEqual(new_inst['email'], 'Holberton@holbertonshool.com')
        self.assertEqual(new_inst['password'], 'tubbcito-plumplum')

    def test_str_method(self):
        """testing str method, checking output"""
        instance4 = User()
        strr = "[User] ({}) {}".format(instance4.id, instance4.__dict__)
        self.assertEqual(strr, str(instance4))

    @mock.patch('models.storage')
    def test_save_method(self, mock_storage):
        """test save method and if it updates
        "updated_at" calling storage.save"""
        instance4 = User()
        created_at = instance4.created_at
        updated_at = instance4.updated_at
        instance4.save()
        new_created_at = instance4.created_at
        new_updated_at = instance4.updated_at
        self.assertNotEqual(updated_at, new_updated_at)
        self.assertEqual(created_at, new_created_at)
        self.assertTrue(mock_storage.save.called)
=======
    def test_user_func_docstrings(self):
        """Test for the presence of docstrings in User methods"""
        for func in self.user_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestUser(unittest.TestCase):
    """Test the User class"""
    def test_is_subclass(self):
        """Test that User is a subclass of BaseModel"""
        user = User()
        self.assertIsInstance(user, BaseModel)
        self.assertTrue(hasattr(user, "id"))
        self.assertTrue(hasattr(user, "created_at"))
        self.assertTrue(hasattr(user, "updated_at"))

    def test_email_attr(self):
        """Test that User has attr email, and it's an empty string"""
        user = User()
        self.assertTrue(hasattr(user, "email"))
        if models.storage_t == 'db':
            self.assertEqual(user.email, None)
        else:
            self.assertEqual(user.email, "")

    def test_password_attr(self):
        """Test that User has attr password, and it's an empty string"""
        user = User()
        self.assertTrue(hasattr(user, "password"))
        if models.storage_t == 'db':
            self.assertEqual(user.password, None)
        else:
            self.assertEqual(user.password, "")

    def test_first_name_attr(self):
        """Test that User has attr first_name, and it's an empty string"""
        user = User()
        self.assertTrue(hasattr(user, "first_name"))
        if models.storage_t == 'db':
            self.assertEqual(user.first_name, None)
        else:
            self.assertEqual(user.first_name, "")

    def test_last_name_attr(self):
        """Test that User has attr last_name, and it's an empty string"""
        user = User()
        self.assertTrue(hasattr(user, "last_name"))
        if models.storage_t == 'db':
            self.assertEqual(user.last_name, None)
        else:
            self.assertEqual(user.last_name, "")

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        u = User()
        new_d = u.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in u.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        u = User()
        new_d = u.to_dict()
        self.assertEqual(new_d["__class__"], "User")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], u.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], u.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        user = User()
        string = "[User] ({}) {}".format(user.id, user.__dict__)
        self.assertEqual(string, str(user))
>>>>>>> 7011bd7fa44cfcbd29c7b265614aea8ae8c08092
