"""
© Copyright Alexandre Silva - 2020

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Created at 26/11/2020
"""

import os
import shutil


class FalseDirectory(BaseException):

    # raised when directory is not in path.

    def __init__(self, path):

        self.path = path

    def __str__(self):

        return 'Directory "{}" not found in specified path -> {}'.format(os.path.basename(self.path), self.path)


class Bdir:

    # Better Directory Class

    def __init__(self, path):

        self.path = path

        self._assure_existance()

        self.dirname = os.path.basename(path)

        self.contents = self.get_contents(path)

    def _assure_existance(self):

        # Assures the existance of a directory

        if os.path.isdir(self.path):

            return

        else:

            raise FalseDirectory(self.path)

    def remove(self):

        # Deletes a directory

        shutil.rmtree(self.path)
        del self.contents, self.dirname, self.path

    def rename(self, newname):

        # Renames a directory

        # Removes the directory basename from the directory path and creates a new one based on the name argument
        base_path = self.path.split(self.dirname)[0]

        new_filepath = os.path.join(base_path, newname)

        os.rename(self.path, new_filepath)

        self.path = new_filepath
        self.dirname = os.path.basename(self.path)

    @staticmethod
    def _determine_dirname(path, name):

        # Determines an available dirname for a certain dir

        newdir = os.path.join(path, name)

        if not os.path.isdir(newdir):

            return name

        serial = 1
        while True:

            # Iterates over code to create the dirname in the format name-serial

            newname = '{}-{}'.format(name, serial)

            newdir = os.path.join(path, newname)

            # Checks if the new name exists in path, if not, adds 1 to the serial and continues the loop
            if not os.path.isdir(newdir):

                return newname

            else:

                serial += 1

    def get_contents(self, path):

        # Returns the contents of a folder in a JSON Serializable format.
        # Recursive Function

        name = os.path.basename(path)

        # Adds the path of the directory into the first section of it's list
        dirtree = {name: {'*path': path}}

        # for loop to recursively search for directories and files in the specified path
        for item in os.listdir(path):
            # Item is any object, be it a dir or a file.

            itempath = os.path.join(path, item)

            if os.path.isdir(itempath):
                # Updates the dirtree with a recursive search of the itempath itself

                dirtree[name].update(self.get_contents(itempath))

            else:

                # Updates the dirtree with the item, followed by its path.
                update = {item: itempath}
                dirtree[name].update(update)

        return dirtree

    def find(self, target):

        # Returns a specific item located inside the directory, however, only the first match.

        # for loop to search for the target inside the directory
        for key in self.contents[self.dirname]:

            if key == "*path":
                # Skip path

                continue

            # Key value in the JSON
            key_value = self.contents[self.dirname][key]

            value_type = type(key_value)

            if value_type is dict:
                # If the value type is a dictionary, create another instance of Bdir and recursively search for the target inside of it

                path = key_value["*path"]

                if key == target:

                    return path

                directory = Bdir(path)

                # Recursive search start; Returns a response -> path
                response = directory.find(target)

                if response is not None:

                    # Returns the response carrying it to the initial recursion

                    return response

                # Deletes the used BDir Class inside the recursion to save resources and free memory
                del directory

            elif value_type is str and key == target:

                return key_value
    
    def find_all(self, target):

        # Returns a list of specific files in a directory

        matches = list()

        # wrapper for the matchlist
        def _findall_wrapper(contents, dirname):
            for key in contents[dirname]:

                if key == "*path":
                    # Skip path

                    continue

                # Key value in the JSON
                key_value = contents[dirname][key]

                value_type = type(key_value)

                if value_type is dict:
                    # If the value type is a dictionary, create another instance of Bdir and recursively search for the target inside of it

                    path = key_value["*path"]

                    if key == target:
                        matches.append(key_value)

                    directory = Bdir(path)
                    ct = directory.contents
                    # Recursive search start; Returns a path

                    _findall_wrapper(ct, directory.dirname)

                    # Deletes the used BDir Class inside the recursion to save resources and free memory
                    del directory, ct

                elif value_type is str and key == target:

                    matches.append(key_value)

        # Start the find
        _findall_wrapper(self.contents, self.dirname)

        if not matches:
            return None

        else:
            return matches

    def move_to(self, path):

        # Moves the directory to the selected path.

        destiny = os.path.join(path, self.dirname)

        if not os.path.isdir(destiny):

            os.mkdir(destiny)

        else:

            # Assures that the destination is an empty directory, overwrites the existing directory.
            shutil.rmtree(destiny)
            os.mkdir(destiny)

        # Copies the directory tree and deletes the already existant one.
        shutil.copytree(self.path, destiny, dirs_exist_ok=True)
        shutil.rmtree(self.path)

        # Updates self.path with the new location
        self.path = destiny

    def copy_to(self, path):

        # Copies the directory to the selected path

        destiny = os.path.join(path, self._determine_dirname(path, self.dirname))

        if not os.path.isdir(destiny):

            os.mkdir(destiny)

        shutil.copytree(self.path, destiny, dirs_exist_ok=True)
