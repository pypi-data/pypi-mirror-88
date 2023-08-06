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

Created at 12/12/2020
"""

import os
import shutil
from binaryornot.check import is_binary


class FalseFile(BaseException):

    # raised when file is not in path.

    def __init__(self, path):

        self.path = path

    def __str__(self):

        return 'File "{}" not found in specified path -> {}'.format(os.path.basename(self.path), self.path)


class Bfile:

    def __init__(self, path):

        self.path = path

        self._assure_existance()

        self.filename = os.path.basename(path)

        self.binary = is_binary(self.path)

        self.extension = os.path.splitext(self.path)[1]

    def _assure_existance(self):

        # Assures the existance of a file

        if os.path.isfile(self.path):

            return

        else:

            raise FalseFile(self.path)

    def remove(self):

        # Deletes a file

        os.remove(self.path)
        del self.filename, self.path

    def rename(self, newname):

        # Renames a file

        # Removes the file basename from the directory path and creates a new one based on the name argument
        base_path = self.path.split(self.filename)[0]

        new_filepath = os.path.join(base_path, newname)

        os.rename(self.path, new_filepath)

        self.path = new_filepath
        self.filename = os.path.basename(self.path)
        self.binary = is_binary(self.path)
        self.extension = os.path.splitext(self.path)[1]

    @staticmethod
    def _determine_filename(path, name):

        # Determines an available filename for a certain file

        newdir = os.path.join(path, name)

        if not os.path.isfile(newdir):
            return name

        serial = 1
        while True:

            # Iterates over code to create the filename in the format name-serial

            newname = '{}-{}'.format(name, serial)

            newdir = os.path.join(path, newname)

            # Checks if the new name exists in path, if not, adds 1 to the serial and continues the loop
            if not os.path.isfile(newdir):

                return newname

            else:

                serial += 1
                
    def move_to(self, path):

        # Moves the file to the selected path.

        destiny = os.path.join(path, self.filename)

        if os.path.isfile(destiny):

            os.remove(destiny)

        shutil.move(self.path, destiny)

    def copy_to(self, path):

        # Copies the file to the selected path

        destiny = os.path.join(path, self._determine_filename(path, self.filename))

        shutil.copy(self.path, destiny)

    def write(self, data):

        # Writes data to a file, this wil overwrite any existant data

        # Determines the mode depending on the binary boolean
        if self.binary:
            mode = 'wb'
        else:
            mode = 'w'

        with open(self.path, mode) as file:

            file.write(data)

    def append(self, data):

        # Appends data to a file.

        # Determines the mode depending on the binary boolean
        if self.binary:
            mode = 'ab'
        else:
            mode = 'a'

        with open(self.path, mode) as file:

            file.write(data)

    def get_content(self):

        # Reads the data within a file.

        # Determines the mode depending on the binary boolean
        if self.binary:
            mode = 'rb'
        else:
            mode = 'r'

        with open(self.path, mode) as file:

            return file.read(), file.readlines()
