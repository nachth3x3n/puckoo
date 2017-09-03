# Source code by Dana Iosifovich 2017
import os
import hashlib
import magic
import string
import re
BLOCKSIZE = 65536


class FileAnalysis:
    def __init__(self, file_path):
        self.file_path = file_path
        self.sha256 = self.calc_hash("sha256")
        self.sha256 = self.calc_hash("md5")
        self.sha256 = self.calc_hash("sha1")
        self.file_type = self.get_file_type()
        self.size = self.get_file_size()

    def get_file_type(self):
        filetype = magic.from_file(self.file_path, mime=True)
        return filetype

    def ext_match_type(self):
        """Checks if file's extension matches its type"""
        extension = os.path.splitext(self.file_path)[1]
        ftype = self.get_file_type()
        if extension == ftype:
            return True
        else:
            return False

    def get_file_size(self):
        """returns file size in KBs"""
        size = (os.path.getsize(self.file_path)) / 1024.0
        return size

    def calc_hash(self, hash_type):
        """
        Calculates hash of the given file
        :param hash_type: Type of hash method, i.e md5, sha256, sha1...
        :return: returns the calculated hash
        """
        hasher = hashlib.hash_type()
        with open(self.file_path, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        return hasher.hexdigest()

    # def calc_sha256(self):
    #     hasher = hashlib.sha256()
    #     with open(self.file_path, 'rb') as afile:
    #         buf = afile.read(BLOCKSIZE)
    #         while len(buf) > 0:
    #             hasher.update(buf)
    #             buf = afile.read(BLOCKSIZE)
    #     return hasher.hexdigest()
    #
    # def calc_md5(self):
    #     hasher = hashlib.md5()
    #     with open(self.file_path, 'rb') as afile:
    #         buf = afile.read(BLOCKSIZE)
    #         while len(buf) > 0:
    #             hasher.update(buf)
    #             buf = afile.read(BLOCKSIZE)
    #     return hasher.hexdigest()
    #
    # def calc_sha1(self):
    #     hasher = hashlib.sha1()
    #     with open(self.file_path, 'rb') as afile:
    #         buf = afile.read(BLOCKSIZE)
    #         while len(buf) > 0:
    #             hasher.update(buf)
    #             buf = afile.read(BLOCKSIZE)
    #     return hasher.hexdigest()

    def strings(self):
        """extracts strings of the binary file"""
        with open(self.file_path, "rb") as f:
            result = ""
            for c in f.read():
                if c in string.printable:
                    result += c
                    continue
                if len(result) >= min:
                    yield result
                result = ""
            if len(result) >= min:  # catch result at EOF
                yield result

    def find_urls(self, strings):
        """
        Searches the binary strings for urls
        :param strings: A list of strings extracted from the binary file
        :return: Returns a list of urls that were found in the strings
        """
        urls = []
        for f_string in strings:
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', f_string)
        return urls

    def find_cnc(self, strings):
        """
        searches in the most stupid way for cnc commands
        :param strings: A list of strings extracted from the binary file
        :return: returns a list of cnc related calls that were found (if any)
        """
        cnc_calls = []
        for a_string in strings:
            if "rcv" or "send" or "exec" in a_string:
                # TODO: work on it to be less dumb + return the contect and not the whole string
                cnc_calls.append(a_string)
        return cnc_calls

