import argparse
import re


def grep(args):
	pass


def n_flag(args: argparse.Namespace):
	count = 1
	count_of_file = len(args.file)

	for file in args.file:
		for line in file:
			if count_of_file > 1:
				print(f"{file.name}:", end='')
			if args.n and (re.search(args.pattern, line, )):
				print(f"{count}:{line}", end='')
				count += 1
		print()


def main():
	parser = argparse.ArgumentParser(prog='my_grep')

	parser.add_argument('-n', help='print line number with output lines', action='store_true')
	parser.add_argument('-i',
						help='ignore case distinctions in patterns and datado not ignore case distinctions (default)',
						action='store_true')

	parser.add_argument('pattern', help='pattern to search', type=str)
	parser.add_argument('file', nargs='*', help='file to search', type=argparse.FileType('r', encoding='UTF-8'))

	args = parser.parse_args()

	n_flag(args)


if __name__ == '__main__':
	main()
