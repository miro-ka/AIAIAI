import logging
import configargparse
from colorama import Fore, Back, Style
from common.ascii_pics import ascii_print_aiaiai
from data.fetch import Fetch


"""
    Lightweight program for fetching / back-filling historical data from exchanges
"""


def main(args):
    fetch_from = args.fetch_from
    fetch_to = args.fetch_to
    logging.info("Starting to fetch data from epoch:" + str(fetch_from) + " to: " + str(fetch_to))
    res = Fetch().fetch(
        fetch_from=int(args.fetch_from),
        fetch_to=int(args.fetch_to),
        ticker=args.ticker,
        pairs='all',
        path='tmp'
    )
    return None


def intro_text():
    print(Fore.GREEN)
    ascii_print_aiaiai()
    print(Style.RESET_ALL)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    intro_text()

    p = configargparse.ArgParser(default_config_files=['aiaiai.conf'])
    p.add('-c', '--my-config', is_config_file=True, default='aiaiai.conf', help='config file path')
    p.add('--fetch_from', required=True, help='Fetch data from epoch UTC')
    p.add('--fetch_to', required=True,  help='Fetch data to epoch UTC')
    p.add('--ticker', required=True, help='Data ticker 300, 900, 1800, 7200, 14400, and 86400')

    options = p.parse_args()
    main(options)
