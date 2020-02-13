# Author: Noah Gaeta -- Date: 02/28/2019
from Webcrawler import Webcrawler
import argparse
import os


def main():
	parser = argparse.ArgumentParser(description='Webcrawler that obtains urls.')
	parser.add_argument('--url', default="https://www.derivative-calculator.net/", help='the start url')
	parser.add_argument('--amount', default=1000, help='')
	parser.add_argument('--clean', default=False, action='store_true', help='removes urls.json file')
	args = parser.parse_args()
	if args.clean and os.path.exists("urls.json"):
		os.remove("urls.json")
	webcrawler = Webcrawler(args.url, args.amount)
	webcrawler.start_crawl()


if __name__ == "__main__":
	exit(main())
