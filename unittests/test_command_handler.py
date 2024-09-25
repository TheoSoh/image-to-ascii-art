import unittest
from command_handler import Command_handler
from image_collection import Image_collection
import exceptions

class TestCommandHandler(unittest.TestCase):
    def setUp(self):
        self.handler = Command_handler()

    def test_initialization(self):
        self.assertIsInstance(self.handler.image_collection, Image_collection)

    def test_invalid_command(self):
        with self.assertRaises(exceptions.InvalidCommandInputError):
            self.handler.execute_command("an invalid command")

    def test_empty_collection(self):
        with self.assertRaises(exceptions.EmptyImageCollectionError):
            self.handler.execute_save_session("some filename")
        with self.assertRaises(exceptions.EmptyImageCollectionError):
            self.handler._execute_render_ascii_art("some image name", "some filename")
        with self.assertRaises(exceptions.EmptyImageCollectionError):
            self.handler._execute_set_image_attribute("some image name",
                                                      "some attribute",
                                                      "some value")

if __name__ == '__main__':
    unittest.main()