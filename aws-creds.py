#! /usr/bin/env python3

import argparse
import subprocess
import sys
import os


bash_init_file = "/tmp/.init-file"

def create_init_file(entry_name):
    f = open(bash_init_file, "w")
    f.write(r"PS1='\[\e[41m\]({})\[\e[0m\] \w$ '".format(entry_name))
    f.close()

class KeePassEntry(object):
    """
    Information contained within a KeePass entry
    """
    def __init__(self, username, password):
        self.username=username
        self.password=password

class KeepPassService(object):
    """
    Service that interacts with a KeePass database
    """
    def __init__(self, dbpath):
        self.dbpath = dbpath

    """ 
    Returns the entry with the given name or Nothing if that entry does not
    have sufficient information to define an entry
    """
    def get_entry(self, entry_name):
        output = subprocess.check_output([
            "keepassxc-cli",
            "show", 
            "-a", "UserName", 
            "-a", "Password", 
            "--show-protected", 
            self.dbpath, 
            entry_name
        ], encoding="utf8")
        values=output.splitlines()
        if len(values) < 2:
            print("Entry {} does not contain at least a UserName and Password".format(entry_name))
            return None 

        return KeePassEntry(values[0], values[1])

def create_terminal_with_env_keys(keepass, entry_name):
    try:
        entry = keepass.get_entry(entry_name)
        if (entry is None):
            sys.exit(1)

        os.environ["AWS_ACCESS_KEY_ID"]=entry.username
        os.environ["AWS_SECRET_ACCESS_KEY"]=entry.password
        create_init_file(entry_name)
        subprocess.call(["bash", "--init-file", bash_init_file])
    except subprocess.CalledProcessError as e:
        sys.exit(1)
    finally:
        if os.path.exists(bash_init_file):
            os.remove(bash_init_file)

def main():
    parser = argparse.ArgumentParser(
            description="Load AWS credentials from a keepass DB in to a new bash terminal")
    parser.add_argument("entry_name")
    args = parser.parse_args()
    if ("KEEPASS_DB" not in os.environ):
        print("keepass dbpath not initialized")
        sys.exit(1)

    keepassdbpath = os.environ["KEEPASS_DB"]
    keepass = KeepPassService(keepassdbpath)
    create_terminal_with_env_keys(keepass, args.entry_name)


main()


