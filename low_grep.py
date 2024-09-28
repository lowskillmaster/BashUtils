import argparse
import re
from operator import xor
import os


def grep(args):
	pass


def custom_print(*args, end='', **kwargs):
	print(*args, end=end, **kwargs)


def line_flag(args: argparse.Namespace):
	count_of_file = len(args.file)
	print(f"[LOG INFO] args: {args}")
	print(f"[LOG INFO] count_of_file: {count_of_file}")
	flags = re.IGNORECASE if args.i else 0

	# Если передан флаг -e, используем его шаблоны, иначе используем позиционный шаблон
	patterns = args.regexp if args.regexp else [args.pattern]

	pattern_flags = flags | re.VERBOSE if args.extended_regexp else flags

	count_of_match = 0
	filenames_with_matches = []

	for file in args.file:
		if args.r and os.path.isdir(file):
			for root, _, files in os.walk(file):
				for f in files:
					process_file(os.path.join(root, f), patterns, pattern_flags, args, count_of_match,
								 filenames_with_matches)
		else:
			process_file(file, patterns, pattern_flags, args, count_of_match, filenames_with_matches)

	if args.c and not args.l:
		custom_print(count_of_match)
	if args.l:
		for filename in filenames_with_matches:
			custom_print(filename)


def process_file(file, patterns, pattern_flags, args, count_of_match, filenames_with_matches):
	try:
		with open(file, 'r', encoding='UTF-8') as f:
			for line_number, line in enumerate(f, start=1):
				line = line.strip()
				match_found = False

				for pattern in patterns:
					match_pattern = re.search(pattern, line, flags=pattern_flags) if not args.w else re.search(
						rf'\b{pattern}\b', line, flags=pattern_flags)
					if xor(bool(match_pattern),
						   args.v):  # (match_pattern and not args.v) or (not match_pattern and args.v)
						match_found = True
						count_of_match += 1
						if file not in filenames_with_matches:
							filenames_with_matches.append(file)
						break

				if match_found:
					if len(args.file) > 1 and not args.q:
						custom_print(f"{file}:")

					if args.n and not args.l:
						custom_print(f"{line_number}:")

					custom_print(f"{line}\n")
	except Exception as e:
		print(f"low_grep: {file}: No such file or directory")


def main():
	parser = argparse.ArgumentParser(prog='MyGrep')
	parser.add_argument('-n', help='custom_print line number with output lines', action='store_true')
	parser.add_argument('-v', help='invert match (select non-matching lines)', action='store_true')
	parser.add_argument('-i', help='ignore case distinctions in patterns and data', action='store_true')
	parser.add_argument('-E', '--extended-regexp', action='store_true', help='Use extended regular expressions')
	parser.add_argument('-e', '--regexp', action='append', help='Multiple patterns to search', type=str)
	parser.add_argument('-w', action='store_true', help='Match whole words only')
	parser.add_argument('-c', action='store_true', help='Count the number of occurrences of the provided pattern')
	parser.add_argument('-l', action='store_true', help='Display file names with matches only')
	parser.add_argument('-q', action='store_true',
						help='don`t display file names with matches only analog -h in original grep')
	parser.add_argument('-r', action='store_true', help='Recursively search directories')
	group = parser.add_mutually_exclusive_group()
	group.add_argument('pattern', help='pattern to search', type=str, nargs='?', action='store')
	parser.add_argument('file', nargs='+', help='file to search', type=str)

	args = parser.parse_args()

	# Если не передан флаг -e и нет позиционного шаблона, выводим ошибку
	if not args.regexp and not args.pattern:
		parser.error("You must provide at least one pattern using -e or as a positional argument.")

	line_flag(args)


if __name__ == '__main__':
	main()
