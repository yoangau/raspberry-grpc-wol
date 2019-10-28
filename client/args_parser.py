import argparse

from common.commands import *


class ArgsParser:

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Process some integers.')
        self.parser.add_argument("-i", required=True, type=str, dest='key_file', action="store")
        self.parser.add_argument('option', type=str, choices=[power_on, power_off, hard_reset])
