import unittest
import os
import exceptions
from image_collection import Image_collection
from image_wrapper import Image_wrapper
from serializer import Serializer

class TestImageCollection(unittest.TestCase):
    def setUp(self):
        self.collection = Image_collection()
        # Assumes image-file "slalom.jpg" is in cwd.
        self.collection.load_image("slalom.jpg", "some alias")
        self.test_to_filename = "test_render_file"

    def test_initialization_and_add_method(self):
        self.assertEqual(len(self.collection.images), 1)
        self.assertEqual(self.collection.current_image, self.collection.images[0])
        self.assertIsInstance(self.collection.current_image, Image_wrapper)
    
    def test_empty_collection(self):
        self.collection.images.clear()
        with self.assertRaises(exceptions.EmptyImageCollectionError):
            self.collection.check_empty_image_collection()

    def test_check_filename_existance(self):
        with self.assertRaises(exceptions.InvalidInputError):
            self.collection._check_filename_existance(self.collection.images[0].filename)

    def test_validate_alias(self):
        with self.assertRaises(exceptions.InvalidInputError):
            self.collection._validate_alias(self.collection.images[0].alias)
        with self.assertRaises(exceptions.InvalidInputError):
            self.collection._validate_alias("current")
        self.assertIsNone(self.collection._validate_alias(None))

    def test_find_image_wrapper(self):
        image_wrapper = self.collection._find_image_wrapper("slalom.jpg")
        self.assertIsInstance(image_wrapper, Image_wrapper)
        with self.assertRaises(exceptions.ImageNotFoundError):
            self.collection._find_image_wrapper("name that dont exist")

    def test_render_ascii_art_to_file(self):
        with self.assertRaises(exceptions.ImageNotFoundError):
            self.collection.render_ascii_art("name that dont exist",
                                             self.test_to_filename)
        self.collection.render_ascii_art(self.collection.images[0].filename,
                                         self.test_to_filename)
        self.assertTrue(os.path.exists("./ascii_images/"
                                       + self.test_to_filename 
                                       + ".txt"))
    
    def test_set_image_attribute_errors(self):
        with self.assertRaises(exceptions.ImageNotFoundError):
            self.collection.set_image_attribute("name that dont exist", "width", "40")
        with self.assertRaises(exceptions.InvalidInputError):
            self.collection.set_image_attribute(self.collection.images[0].filename,
                                                "width", "invalid_input_value")
        with self.assertRaises(exceptions.InvalidInputError):
            self.collection.set_image_attribute(self.collection.images[0].filename,
                                                "height", "-1")
        with self.assertRaises(exceptions.InvalidInputError):
            self.collection.set_image_attribute(self.collection.images[0].filename,
                                                "brightness", "-1")
        with self.assertRaises(exceptions.InvalidInputError):
            self.collection.set_image_attribute(self.collection.images[0].filename,
                                                "contrast", "-1")
            
    def test_set_image_attribute_brightness(self):
        original_brightness = self.collection.images[0].brightness
        self.collection.set_image_attribute(self.collection.images[0].filename,
                                            "brightness", "1.2")
        self.assertIsInstance(self.collection.images[0].brightness, float)
        self.assertEqual(self.collection.images[0].brightness, 1.2)
        self.assertNotEqual(self.collection.images[0].brightness, original_brightness)
        
    def test_set_image_attribute_contrast(self):
        original_contrast = self.collection.images[0].contrast
        self.collection.set_image_attribute(self.collection.images[0].filename,
                                            "contrast", "1.6")
        self.assertIsInstance(self.collection.images[0].contrast, float)
        self.assertEqual(self.collection.images[0].contrast, 1.6)
        self.assertNotEqual(self.collection.images[0].contrast, original_contrast)

    def tearDown(self):
        # Delete temporary files.
        if os.path.exists("./ascii_images/" + self.test_to_filename):
            os.remove("./ascii_images/" + self.test_to_filename)

class TestSerializer(unittest.TestCase):
    def setUp(self):
        self.collection = Image_collection()
        # Assumes image-file "slalom.jpg" is in cwd.
        self.collection.load_image("slalom.jpg", None)
        self.test_file = "test_serialization.json"

    def test_serialize(self):
        Serializer.serialize(self.collection, self.test_file)
        self.assertTrue(os.path.exists(self.test_file))

    def test_deserialize(self):
        Serializer.serialize(self.collection, self.test_file)
        deserialized_collection = Serializer.deserialize(self.test_file)
        self.assertIsInstance(deserialized_collection, Image_collection)
        self.assertEqual(len(deserialized_collection.images), 1)
        self.assertIsInstance(deserialized_collection.images[0], Image_wrapper)

    def tearDown(self):
        # Delete temporary file.
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
if __name__ == '__main__':
    unittest.main()