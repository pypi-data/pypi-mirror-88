#!/usr/bin/env python3

import sys


class System: # Flag system
    def __init__(self):
        self.flags = {}
        self.config = Config() # Let us use the Config class for stuff

    def add(self, *names):
        """Used for adding multiple flags to list self.flags"""
        for name in names:
            self.flags[name] = None

    def addfunc(self, name, target):
        self.flags[name] = target


    def get(self):
        """Get all of the used flags and their values from argv and return them in a dict"""
        found_flags = {}
        found_bad_flag = False # Is there a flag that isn't one we want?

        if self.config.helpflagenabled:
            self.flags["--help"] = None

        for arg in sys.argv[1:]:
            if arg.split(self.config.flagequals)[0].startswith("-") and arg.split(self.config.flagequals)[0] not in self.flags.keys() and self.config.hideerrors == False:
                    print(f"error: invalid flag '{arg.split('=')[0]}'")
                    found_bad_flag = True

            if arg.split(self.config.flagequals)[0] in self.flags:
                try:
                    found_flags[arg.split(self.config.flagequals)[0]] = arg.split(self.config.flagequals)[1]
                except IndexError:
                    found_flags[arg.split(self.config.flagequals)[0]] = None

        if (found_flags == {} and self.config.flagsrequired == True) or (found_bad_flag) or (self.config.argsrequired == True and sys.argv[1:] == []) or (self.config.helpflagenabled == True and "--help" in found_flags):
            if self.config.usagemsg == None:
                if self.config.usagecommandname == None:
                    print(f"usage: {sys.argv[0]} ", end="")

                else:
                    print(f"usage: {self.config.usagecommandname} ", end="")

                flag_count = 0 # Amount of flags we are showing

                for flag in self.flags.keys():
                    if flag_count >= 4:
                        try:
                            print(f"\n{' ' * (len(self.config.usagecommandname) + 8)}", end="")
                        except TypeError:
                            print(f"\n{' ' * (len(sys.argv[0]) + 8)}", end="")

                        flag_count = 0

                    print(f"[{flag}] ", end="")
                    flag_count += 1 # Up the amount of flags we are displaying
                                    # (on one line)

                print("\n" + self.config.extrausagemsg, end="")

                if self.config.helpflagenabled == True and "--help" in found_flags:
                    return None, 2

                else:
                    return None, 1


            else:
                print(self.config.usagemsg)

                if self.config.helpflagenabled == True and "--help" in found_flags:
                    return None, 2

                else:
                    return None, 1

        for flag in self.flags:
            if flag in found_flags:
                try:
                    self.flags[flag][0](self.flags[flag][1:])
                except TypeError:
                    continue

        return found_flags, 0

class Config: # For changing around varibles in an easy way
    def __init__(self):
        self.flagsrequired = False
        self.helpflagenabled = True
        self.argsrequired = False
        self.usagecommandname = None
        self.usagemsg = None
        self.extrausagemsg = ""
        self.hideerrors = False
        self.flagequals = "="
