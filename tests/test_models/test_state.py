#!/usr/bin/python3
"""User test"""
from datetime import datetime
import inspect
import models
<<<<<<< HEAD
import pep8 as pycodestyle
=======
from models import state
>>>>>>> 7011bd7fa44cfcbd29c7b265614aea8ae8c08092
from models.base_model import BaseModel
from models.engine.db_storage import DBStorage
import time
import unittest
from unittest import mock
Model = models.state.State
State = models.state.State
module_doc = models.state.__doc__
path1 = "models/state.py"
path2 = "tests/test_models/test_state.py"


<<<<<<< HEAD
class DocsTest(unittest.TestCase):
    """Test to check behaviors"""
=======
    def test_pep8_conformance_state(self):
        """Test that models/state.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/state.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")
>>>>>>> 7011bd7fa44cfcbd29c7b265614aea8ae8c08092

    @classmethod
    def setUpClass(self):
        """setting up tests"""
        self.self_funcs = inspect.getmembers(Model, inspect.isfunction)

    def test_module_docstring(self):
        """Test module docstring"""
        self.assertIsNot(module_doc, None,
                         "state.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "test_state.py needs a docstring")

        """Test classes doctring"""
        self.assertIsNot(BaseModel.__doc__, None,
                         "State class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) >= 1,
                        "State class needs a docstring")

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
    @mock.patch('models.state')
    def test_instances(self, mock_storage):
        """Testing that object is correctly created"""
        instance = State()
        self.assertIs(type(instance), State)
        instance.name = "Holbies foravaaaa"

        expectec_attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str
        }
        # testing types and attr names
        for attr, types in expectec_attrs_types.items():
            with self.subTest(attr=attr, typ=types):
                self.assertIn(attr, instance.__dict__)
                self.assertIs(type(instance.__dict__[attr]), types)
        self.assertEqual(instance.name, "Holbies foravaaaa")

<<<<<<< HEAD
    def test_datetime(self):
        """testing correct datetime assignation
        correct assignation of created_at and updated_at"""
        created_at = datetime.now()
        instance1 = State()
        updated_at = datetime.now()
        self.assertEqual(created_at <= instance1.created_at <=
                         updated_at, False)
        time.sleep(0.1)
        created_at = datetime.now()
        instance2 = State()
        updated_at = datetime.now()
        self.assertFalse(created_at <= instance2.created_at <= updated_at, True)
        self.assertEqual(instance1.created_at, instance1.created_at)
        self.assertEqual(instance2.updated_at, instance2.updated_at)
        self.assertNotEqual(instance1.created_at, instance2.created_at)
        self.assertNotEqual(instance1.updated_at, instance2.updated_at)

    def test_uuid(self):
        """testing uuid"""
        instance1 = State()
        instance2 = State()
        for instance in [instance1, instance2]:
            tuuid = instance.id
            with self.subTest(uuid=tuuid):
                self.assertIs(type(tuuid), str)

    def test_dictionary(self):
        """testing to_dict correct funtionality"""
        """Testing that object is correctly created"""
        instance3 = State()
        self.assertIs(type(instance3), State)
        instance3.name = "Holbies"
        new_inst = instance3.to_dict()
        expectec_attrs = ["id",
                          "created_at",
                          "updated_at",
                          "name",
                          "__class__"]
        self.assertCountEqual(new_inst.keys(), expectec_attrs)
        self.assertEqual(new_inst['__class__'], 'State')
        self.assertEqual(new_inst['name'], 'Holbies')

    def test_str_method(self):
        """testing str method, checking output"""
        instance4 = State()
        strr = "[State] ({}) {}".format(instance4.id, instance4.__dict__)
        self.assertEqual(strr, str(instance4))

    @mock.patch('models.storage')
    def test_save_method(self, mock_storage):
        """test save method and if it updates
        "updated_at" calling storage.save"""
        instance4 = State()
        created_at = instance4.created_at
        updated_at = instance4.updated_at
        instance4.save()
        new_created_at = instance4.created_at
        new_updated_at = instance4.updated_at
        self.assertNotEqual(updated_at, new_updated_at)
        self.assertEqual(created_at, new_created_at)
        self.assertTrue(mock_storage.save.called)
=======
class TestState(unittest.TestCase):
    """Test the State class"""
    def test_is_subclass(self):
        """Test that State is a subclass of BaseModel"""
        state = State()
        self.assertIsInstance(state, BaseModel)
        self.assertTrue(hasattr(state, "id"))
        self.assertTrue(hasattr(state, "created_at"))
        self.assertTrue(hasattr(state, "updated_at"))

    def test_name_attr(self):
        """Test that State has attribute name, and it's as an empty string"""
        state = State()
        self.assertTrue(hasattr(state, "name"))
        if models.storage_t == 'db':
            self.assertEqual(state.name, None)
        else:
            self.assertEqual(state.name, "")

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        s = State()
        new_d = s.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in s.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        s = State()
        new_d = s.to_dict()
        self.assertEqual(new_d["__class__"], "State")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], s.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], s.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        state = State()
        string = "[State] ({}) {}".format(state.id, state.__dict__)
        self.assertEqual(string, str(state))
>>>>>>> 7011bd7fa44cfcbd29c7b265614aea8ae8c08092
