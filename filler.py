import configargparse
from colorama import Fore, Back, Style
from common.ascii_pics import ascii_print_aiaiai

"""
    Lightweight program for fetching historical data from exchanges
"""


def main(args):
    return None


def intro_text():
    print(Fore.RED)
    ascii_print_aiaiai()
    print(Style.RESET_ALL)


if __name__ == "__main__":
    intro_text()

    p = configargparse.ArgParser(default_config_files=['aiaiai.conf'])
    p.add('-c', '--my-config', is_config_file=True, default='aiaiai.conf', help='config file path')
    p.add('--fetch_from', required=True,  help='Fetch data from epoch UTC')
    p.add('--fetch_to', required=True,  help='Fetch data to epoch UTC')

    options = p.parse_args()
    main(options)
