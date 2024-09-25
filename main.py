from command_handler import Command_handler
import exceptions

def main():
    """The main body of the program."""
    print("Welcome to ASCII Art Studio!", "(Enter \'help\' for commands)",
          "Enter command below:", sep="\n")
    # exits loop when user quit program.
    while True:
        command = input("AAS: ")
        try:
            Command_handler.execute_command(command)
        except exceptions.InvalidCommandInputError as e:
            print(e)
        except exceptions.EmptyImageCollectionError as e:
            print(e)
        except FileNotFoundError:
            print("-- File not found: The filename you entered could"
                  + " not be found --")
        except exceptions.ImageNotFoundError as e:
            print(e)
        except FileExistsError:
            print("-- Invalid filename: The file you entered already"
                  + " exist --")
        except exceptions.InvalidInputError as e:
            print(e)
        except exceptions.SessionLoadError as e:
            print(e)
        except Exception as e:
            print(f"-- An unexcpected error occured: {e} --")

# Start the main program
if __name__ == '__main__':
    main()