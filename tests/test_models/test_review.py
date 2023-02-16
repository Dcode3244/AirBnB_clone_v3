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
Model = models.review.Review
Review = models.review.Review
module_doc = models.review.__doc__
path1 = "models/review.py"
path2 = "tests/test_models/test_review.py"


class DocsTest(unittest.TestCase):
    """Test to check behaviors"""

    @classmethod
    def setUpClass(self):
        """setting up tests"""
        self.self_funcs = inspect.getmembers(Model, inspect.isfunction)

    def test_module_docstring(self):
        """Test module docstring"""
        self.assertIsNot(module_doc, None,
                         "review.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "test_review.py needs a docstring")

        """Test classes doctring"""
        self.assertIsNot(BaseModel.__doc__, None,
                         "Review class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) >= 1,
                        "Review class needs a docstring")

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
    @mock.patch('models.review')
    def test_instances(self, mock_storage):
        """Testing that object is correctly created"""
        instance = Review()
        self.assertIs(type(instance), Review)
        instance.name = "Holbies foravaaaa"
        instance.state_id = "111-222"
        instance.user_id = "123-123"
        instance.text = "some texting here"

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
        self.assertEqual(instance.user_id, "123-123")
        self.assertEqual(instance.text, "some texting here")

    def test_datetime(self):
        """testing correct datetime assignation
        correct assignation of created_at and updated_at"""
        created_at = datetime.now()
        instance1 = Review()
        updated_at = datetime.now()
        self.assertEqual(created_at <= instance1.created_at <=
                         updated_at, False)
        time.sleep(0.1)
        created_at = datetime.now()
        instance2 = Review()
        updated_at = datetime.now()
        self.assertFalse(created_at <= instance2.created_at <= updated_at, True)
        self.assertEqual(instance1.created_at, instance1.created_at)
        self.assertEqual(instance2.updated_at, instance2.updated_at)
        self.assertNotEqual(instance1.created_at, instance2.created_at)
        self.assertNotEqual(instance1.updated_at, instance2.updated_at)

    def test_uuid(self):
        """testing uuid"""
        instance1 = Review()
        instance2 = Review()
        for instance in [instance1, instance2]:
            tuuid = instance.id
            with self.subTest(uuid=tuuid):
                self.assertIs(type(tuuid), str)

    def test_dictionary(self):
        """testing to_dict correct funtionality"""
        """Testing that object is correctly created"""
        instance3 = Review()
        self.assertIs(type(instance3), Review)
        instance3.name = "Holbies foravaaaa"
        instance3.place_id = "222"
        instance3.user_id = "555"
        instance3.text = "some texting here"
        new_inst = instance3.to_dict()
        expectec_attrs = ["id",
                          "created_at",
                          "updated_at",
                          "name",
                          "place_id",
                          "user_id",
                          "text",
                          "__class__"]
        self.assertCountEqual(new_inst.keys(), expectec_attrs)
        self.assertEqual(new_inst['__class__'], 'Review')
        self.assertEqual(new_inst['name'], 'Holbies foravaaaa')
        self.assertEqual(new_inst['place_id'], '222')
        self.assertEqual(new_inst['user_id'], '555')
        self.assertEqual(new_inst['text'], 'some texting here')

    def test_str_method(self):
        """testing str method, checking output"""
        instance4 = Review()
        strr = "[Review] ({}) {}".format(instance4.id, instance4.__dict__)
        self.assertEqual(strr, str(instance4))

    @mock.patch('models.storage')
    def test_save_method(self, mock_storage):
        """test save method and if it updates
        "updated_at" calling storage.save"""
        instance4 = Review()
        created_at = instance4.created_at
        updated_at = instance4.updated_at
        instance4.save()
        new_created_at = instance4.created_at
        new_updated_at = instance4.updated_at
        self.assertNotEqual(updated_at, new_updated_at)
        self.assertEqual(created_at, new_created_at)
        self.assertTrue(mock_storage.save.called)
=======
    def test_review_func_docstrings(self):
        """Test for the presence of docstrings in Review methods"""
        for func in self.review_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestReview(unittest.TestCase):
    """Test the Review class"""
    def test_is_subclass(self):
        """Test if Review is a subclass of BaseModel"""
        review = Review()
        self.assertIsInstance(review, BaseModel)
        self.assertTrue(hasattr(review, "id"))
        self.assertTrue(hasattr(review, "created_at"))
        self.assertTrue(hasattr(review, "updated_at"))

    def test_place_id_attr(self):
        """Test Review has attr place_id, and it's an empty string"""
        review = Review()
        self.assertTrue(hasattr(review, "place_id"))
        if models.storage_t == 'db':
            self.assertEqual(review.place_id, None)
        else:
            self.assertEqual(review.place_id, "")

    def test_user_id_attr(self):
        """Test Review has attr user_id, and it's an empty string"""
        review = Review()
        self.assertTrue(hasattr(review, "user_id"))
        if models.storage_t == 'db':
            self.assertEqual(review.user_id, None)
        else:
            self.assertEqual(review.user_id, "")

    def test_text_attr(self):
        """Test Review has attr text, and it's an empty string"""
        review = Review()
        self.assertTrue(hasattr(review, "text"))
        if models.storage_t == 'db':
            self.assertEqual(review.text, None)
        else:
            self.assertEqual(review.text, "")

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        r = Review()
        new_d = r.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in r.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        r = Review()
        new_d = r.to_dict()
        self.assertEqual(new_d["__class__"], "Review")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], r.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], r.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        review = Review()
        string = "[Review] ({}) {}".format(review.id, review.__dict__)
        self.assertEqual(string, str(review))
>>>>>>> 7011bd7fa44cfcbd29c7b265614aea8ae8c08092
