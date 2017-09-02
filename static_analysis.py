# Source code by Dana Iosifovich 2017
import os
import hashlib
import magic
BLOCKSIZE = 65536

class FileAnalysis:
    def __init__(self, file_path):

        self.file_path = file_path
        self.sha256 = self.calc_sha256(file_path)
        self.md5 = self.calc_md5(file_path)
        self.sha1 = self.calc_sha1(file_path)
        # self.file_type = file_type
        # self.size = size
        # self.extension = extension
        # self.sha256 = sha256
    def get_file_type(self):
        magic.from_file(self.file_path, mime=True)
        #return

    def calc_sha256(self):
        hasher = hashlib.sha256()
        with open(self.file_path, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        return hasher.hexdigest()

    def calc_md5(self):
        hasher = hashlib.md5()
        with open(self.file_path, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        return hasher.hexdigest()

    def calc_sha1(self):
        hasher = hashlib.sha1()
        with open(self.file_path, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        return hasher.hexdigest()



