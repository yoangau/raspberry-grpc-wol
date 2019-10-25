import argparse


class ArgsParser:
    power_on: str = "poweron"
    power_off: str = "poweroff"
    hard_reset: str = "hardreset"

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Process some integers.')
        self.parser.add_argument('option', type=str, choices=[self.power_on, self.power_off, self.hard_reset])
        self.parser.add_argument("-i", help="path to id_rsa file", required=True, dest='key_file', type=str,
                                 action="store_true")
