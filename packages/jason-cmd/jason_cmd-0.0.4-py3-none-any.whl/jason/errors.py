#!/usr/bin/env python3

import sys


class Type:
    def __init__(self, typename):
        self.typename = typename
        self.config = Config(self.typename)

        self.reason = self.config.reason
        self.code = self.config.code


    def call(self):
        """Calls the error"""
        print(f"{self.config.typename}: {self.config.reason}")

        assert int(self.config.code) # Gotta be an int
        sys.exit(int(self.config.code))


class Config:
    def __init__(self, typename):
        self.typename = typename
        self.reason = f"{self.typename}"
        self.code = 1
