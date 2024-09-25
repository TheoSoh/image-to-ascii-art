import re
from image_collection import Image_collection
from serializer import Serializer
import exceptions

class Command_handler:
    # Initialize an instance of Image_collection to handle commands.
    image_collection = Image_collection()

    # List of available commands.
    commands = [
        "load image 'filename'",
        "load image 'filename' as 'alias'",
        "info",
        "render",
        "render 'filename/alias/current'",
        "render 'filename/alias/current' to 'filename'",
        "set 'filename/alias' 'width' 'value' (Original value: 50)",
        "set 'filename/alias' 'height' 'value'",
        "set 'filename/alias' 'brightness' 'value' (Original value: 1.0)",
        "set 'filename/alias' 'contrast' 'value' (Original value: 1.0)",
        "save session as 'filename'",
        "load session 'filename'",
        "quit/exit"
    ]

    # Dictionary mapping command names to regex patterns for parsing input.
    command_patterns = {
        "load_image": re.compile(r'^load image (\S+\.(png|jpe?g))(?: as (\S+))?$', re.IGNORECASE),
        "info": re.compile(r'^info$', re.IGNORECASE),
        "render": re.compile(r'^render(?: (\S+))?(?: to (\S+))?$', re.IGNORECASE),
        "set_image_attribute": re.compile(r'^set (\S+) (width|height|brightness|contrast) (\d+(\.\d+)?)$', re.IGNORECASE),
        "save_session": re.compile(r'^save session as (\S+)$', re.IGNORECASE),
        "load_session": re.compile(r'^load session (\S+)$', re.IGNORECASE),
        'help': re.compile(r'^help$', re.IGNORECASE),
        'quit': re.compile(r'^(quit|exit)$', re.IGNORECASE)
    }
    
    @staticmethod
    def execute_command(command: str):
        """Assumes command is a string. Checks if command matches any of
        the defined regex patterns. If there's a match, store relevant
        values and execute the correct function.
        """
        # Execute the correct function based on the command name.
        match, command_name = Command_handler._check_match(command)

        if command_name == 'load_image':
            filename, alias = match.group(1), match.group(3)
            Command_handler._execute_load_image(filename, alias)
        elif command_name == 'info':
            Command_handler.image_collection.display_info()
            return
        elif command_name == 'render':
            image_name, filename = match.group(1), match.group(2)
            Command_handler._execute_render_ascii_art(image_name, filename)
            return
        elif command_name == 'set_image_attribute':
            image_name, attribute, value = (match.group(1), match.group(2),
                                            match.group(3))
            Command_handler._execute_set_image_attribute(image_name,
                                                        attribute.lower(),
                                                        value)
            return
        elif command_name == 'save_session':
            filename = match.group(1)
            Command_handler.execute_save_session(filename)
            return
        elif command_name == 'load_session':
            filename = match.group(1)
            Command_handler._execute_load_session(filename)
            return
        elif command_name == 'help':
            Command_handler._display_commands()
            return
        elif command_name == 'quit':
            Command_handler._exit_program()
        
    @staticmethod
    def _check_match(command: str):
        # Attempt to match command with each regex pattern.
        for command_name, pattern in Command_handler.command_patterns.items():
            match = re.match(pattern, command)
            if match:
                # Skip to compare the next pattern.
                return match, command_name
        
        # Raise an exception if command doesn't match any pattern.
        raise exceptions.InvalidCommandInputError("-- You entered an invalid"
                                                  + " command --\n(Enter 'help'"
                                                  + " to view all commands)")

    @staticmethod
    def _execute_load_image(filename: str, alias: str|None):
        """Assumes filename is a string and alias is a string or None.
        Displays relevant message if load succeds.
        """
        Command_handler.image_collection.load_image(filename, alias)
        if alias:
            print(f"Successful load: '{filename}' is loaded as \'{alias}\'")
        else:
            print(f"Successful load: '{filename}' is loaded")

    @staticmethod
    def _execute_render_ascii_art(image_name: str,
                               filename: str|None):
        """Assumes image_name is a string and filename is a string or None.
        Executes function to renders ascii-art based on specified image
        either to console or to a txt-file. Displays a message if it
        rendered successfuly to a file.
        """
        Command_handler.image_collection.render_ascii_art(image_name, filename)
        if filename:
            print(f"Successful render: ASCII-art rendered to {filename}.txt")

    @staticmethod
    def _execute_set_image_attribute(image_name: str,
                                  attribute: str,
                                  value: str):
        """Assumes image_collection is an Image_collection object, image_name
        is a string, attribute is a string and value is a string. Calls the
        function that sets the specified attribute of an image. Displays a
        message if the attribute adjustment succeds.
        """
        Command_handler.image_collection.set_image_attribute(image_name, 
                                                             attribute, 
                                                             value)
        print(f"Successful alteration: {attribute.capitalize()} of "
              + f"'{image_name}' is now set to '{value}'")
    
    @staticmethod
    def execute_save_session(filename: str):
        """Assumes image_collection is an Image_collection object and
        filename is a string. Calls the function that saves the images to disk and the 
        current session to specified json-file. Displays a message if
        the current session saved as intended.
        """
        Serializer.serialize(Command_handler.image_collection, filename + ".json")
        print(f"Successful save: Session is saved as '{filename}.json'")

    @staticmethod
    def _execute_load_session(filename: str):
        """Assumes image_collection is an Image_collection object and filename
        is a string. Calls the function that loads a saved session. All images
        in the current session will be replaced with the loaded sessions images.
        An exception is thrown if the data from specified json-file is invalid.
        Displays a message if the session load was successful.
        """
        try:
            Command_handler.image_collection = Serializer.deserialize(filename + ".json")
        except IndexError:
            raise exceptions.SessionLoadError(f"-- Load failed: '{filename}.json'"
                                              + " contain invalid data --")
        print(f"Successful load: '{filename}.json' loaded as current session")
    
    @staticmethod
    def _display_commands():
        """Displays all available commands."""
        print("=== Available commands ===")
        for command_text in Command_handler.commands:
            print(command_text)
    
    @staticmethod
    def _exit_program():
        """Turns off the program."""
        print("Program shutting down...")
        exit(0)