"""
-b - нумеровать только непустые строки;
-E - показывать символ $ в конце каждой строки;
-n - нумеровать все строки;
-s - удалять пустые повторяющиеся строки;
-T - отображать табуляции в виде ^I;
-h - отобразить справку;
"""

import argparse
import sys


def cat(args: argparse.Namespace):
	number_of_empty_line = 0
	number_of_non_empty_line = 1
	number_of_line = 1

	print(args.filename)
	def process_line(line: str):
		nonlocal number_of_empty_line, number_of_non_empty_line, number_of_line

		if line.isspace():
			number_of_empty_line += 1
		else:
			number_of_empty_line = 0
			if args.b:
				print(f"	{number_of_non_empty_line} ", end='')
				number_of_non_empty_line += 1

		if args.squeeze_blank and number_of_empty_line > 1:
			return
		if args.n and not args.b:
			print(f"	{number_of_line} ", end='')
			number_of_line += 1

		line_flags(args, line)

	if args.filename:
		for file in args.filename:
			for line in file:
				process_line(line)
	else:
		for line in sys.stdin:
			process_line(line)


def non_printing_ascii_char(char):
	if char == '\n' or char == '\t':
		return

	if ord(char) <= 31:
		print('^', end='')
		char = chr(ord(char) + 64)
		print(char, end='')
	elif ord(char) == 127:
		print('^', end='')
		print(char, end='')


def line_flags(args: argparse.Namespace, line):
	if line[-1] != '\n':
		line += '\n'

	for char in line:
		if args.v:
			non_printing_ascii_char(char)

		if args.E and char == '\n':
			print("$")
		elif args.T and char == '\t':
			print("^I", end='')
		else:
			print(char, end='')


def parse_arguments():
	parser = argparse.ArgumentParser(prog='my_cat')
	parser.add_argument("-b", help="number non-blank output lines", action="store_true")
	parser.add_argument("-n", help="number all output lines", action="store_true")
	parser.add_argument("-E", help="display end-of-line characters as $", action="store_true")
	parser.add_argument("-T", help="display tabs as ^I", action="store_true")
	parser.add_argument("-v", help='non-printing non-ascii UTF characters', action="store_true")
	parser.add_argument("-s", "--squeeze-blank", help="squeeze multiple adjacent blank lines", action="store_true")
	parser.add_argument("filename", help="filename", type=argparse.FileType('r', encoding='UTF-8'), nargs="*")

	args = parser.parse_args()
	return args


def main():

	cat(parse_arguments())


if __name__ == "__main__":
	main()
