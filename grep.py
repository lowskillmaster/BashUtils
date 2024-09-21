import argparse
import re
from colorama import init
from operator import xor
from colorama import Fore


def grep(args):
	pass


def n_flag(args: argparse.Namespace):
	count = 1
	count_of_file = len(args.file)
	flags = re.IGNORECASE if args.i else False

	for file in args.file:
		for line in file:
			match_pattern = re.search(args.pattern, line, flags=flags)
			if count_of_file > 1:
				print(f"{file.name}:", end='')

			if xor(bool(match_pattern), args.v): 	#(match_pattern and not args.v) or (not match_pattern and args.v)
				if args.n:
					print(f"{count}:", end='')

				print(f"{line}", end='')
			count += 1


def main():
	# using color print
	init()

	parser = argparse.ArgumentParser(prog='my_grep')

	parser.add_argument('-n', help='print line number with output lines', action='store_true')
	parser.add_argument('-v', help='aboba', action='store_true')
	parser.add_argument('-i',
						help='ignore case distinctions in patterns and datado not ignore case distinctions (default)',
						action='store_true')
	parser.add_argument('-E', '--extended-regexp', action='store_true', help='Use extended regular expressions')
	parser.add_argument('pattern', help='pattern to search', type=str)
	parser.add_argument('file', nargs='*', help='file to search', type=argparse.FileType('r', encoding='UTF-8'))

	args = parser.parse_args()

	n_flag(args)


if __name__ == '__main__':
	main()
