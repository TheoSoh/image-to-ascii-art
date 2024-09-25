import json
from image_collection import Image_collection
from image_wrapper import Image_wrapper

class Serializer:
    @staticmethod
    def serialize(image_collection: Image_collection, filename: str):
        """Assumes image_collection is an Image_collection object and filename is
        a string. Checks if current session has any loaded images. If it contain
        loaded images, transform current session's data to json format. Renders
        transformed session data to specified json-file.
        """
        image_collection.check_empty_image_collection()
        data = Serializer._transform_data_to_json_format(image_collection)
        with open(filename, "x") as json_file:
            json.dump(data, json_file, indent=4)

    @staticmethod
    def deserialize(filename: str):
        """Assumes filename is a string that include file suffix '.json'.
        Instanciates an Image_collection object. Fetches data from the 
        specified json-file and instanciates new Image_wrapper objects 
        based on fetched data. Returns Image_collection object 
        containing loaded images from the saved session.
        """
        image_collection = Image_collection()
        with open(filename, "r") as json_file:
            session_data = json.load(json_file)

            # Instanciate Image_wrapper objects based on the number of saved images and their individual data
            for image in session_data["images"]:
                image_collection._check_filename_existance(image["filename"])  # Validate loaded filename.
                image_collection._validate_alias(image["alias"])  # Validate loaded alias.
                target_size = image["target_size"]
                target_width = target_size[0]  # Fetch only the width of saved target size.
                image_wrapper = Image_wrapper(image["filename"], image["alias"],
                                              target_width, image["brightness"],
                                              image["contrast"])
                image_collection.add_image_to_collection(image_wrapper)  # Add image_wrapper instance to list of images.

                current_image_data = session_data["current_image"]
                if image["filename"] == current_image_data["filename"]:
                    image_collection.current_image = image_wrapper
        return image_collection

    @staticmethod
    def _transform_data_to_json_format(image_collection: Image_collection):
        """Assumes image_collection is an Image_collection object.
        Transforms the object's data to json-format
        """
        session_data = {
            "images": [], 
            "current_image": None
        }
        for image_wrapper in image_collection.images:
            image_wrapper.image.save(image_wrapper.filename)  # Save image on disk (overwrites file if already exists).

            image_data = {
                "filename": image_wrapper.filename,
                "alias": image_wrapper.alias,
                "size": image_wrapper.size,
                "target_size": image_wrapper.target_size,
                "brightness": image_wrapper.brightness,
                "contrast": image_wrapper.contrast
            }
            session_data["images"].append(image_data)

            if image_wrapper.filename == image_collection.current_image.filename:
                session_data["current_image"] = image_data

        return session_data