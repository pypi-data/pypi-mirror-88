""" The module contains class FileManager() which can be used to create\
    temporary directories for your application. FileManager tracks all\
    the temporary directories. The user is free from keeping track of\
    all temporary directories. All the created temporary directories\
    can be deleted using simple call.
"""
from typing import List, Dict, Any
import tempfile
import shutil
import logging
import hashlib
import os
from file_wizard import logger

log: logging.Logger = logger.initLogger()


class FileManager():
    """Final Manager() contains methods for manipulating files. Some of the \
        methods uses the inbuilt functions from modules tempfile, os, shutils\
            etc.
    """
    __tempFiles: List[str]
    __bufferSize: int

    def __init__(self):
        super().__init__()
        self.__tempFiles = []
        self.__bufferSize = 65536

    @property
    def bufferSize(self):
        """Property gives the buffer size
        """
        return self.__bufferSize

    @bufferSize.setter
    def bufferSize(self, size: int):
        if size > 0:
            self.__bufferSize = size

    def mkdtemp(self, suffix=None, prefix=None, folder=None,
                autoDelete: bool = True):
        """mkdtemp() is a wrapper for the shutil.mkdtemp. The methods also \
            keep track of the temporary folder created.

        Args:
            suffix (optional): Defaults to None.
            prefix (optional): Defaults to None.
            folder (optional): Defaults to None.
            autoDelete (bool, optional): If true directory will be added \
                for auto deletion. Defaults to True.

        Returns:
            fullpath of the created temporary folder.
        """
        temp = tempfile.mkdtemp(suffix=suffix, prefix=prefix, dir=folder)
        log.info("Create temporary folder: %s", temp)
        if autoDelete is True:
            self.__tempFiles.append(temp)
        return temp

    def rmdtemp(self):
        """Removes all the temporary directories.
        """
        for tempFile in self.__tempFiles:
            shutil.rmtree(tempFile)
            log.info("Deleted the folder: %s", tempFile)

    def doubleHash(self, inputFile: str) -> Dict[str, Any]:
        """The function MD5 and SHA1  hash values for the given input files.

        Args:
            inputFile (str): File to be hashed

        Returns:
            Dict[str, Any]: Returns stats (True/False) and MD5 and SHA1\
                hash values.
        """
        hashValues = {}
        if os.path.exists(inputFile) is False:
            hashValues["md5"] = ""
            hashValues["sha1"] = ""
            hashValues["status"] = False
            return hashValues
        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        with open(inputFile, 'rb') as fileHandler:
            while True:
                data = fileHandler.read(self.bufferSize)
                if not data:
                    break
                md5.update(data)
                sha1.update(data)
        log.info("MD5: %s", md5.hexdigest())
        log.info("SHA1: %s", sha1.hexdigest())
        hashValues["status"] = True
        hashValues["md5"] = md5.hexdigest()
        hashValues["sha1"] = sha1.hexdigest()
        return hashValues
