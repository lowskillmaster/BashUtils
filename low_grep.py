import argparse
import re
import os

def custom_print(*args: object, end: object = '', **kwargs: object) -> None:
    print(*args, end=end, **kwargs)

def parse_patterns(args: argparse.Namespace) -> list:
    patterns = []
    if args.regexp:
        patterns.extend(args.regexp)
    if args.pattern:
        patterns.append(args.pattern)
    if args.pattern_file:
        try:
            with open(args.pattern_file, 'r', encoding='UTF-8') as f:
                patterns.extend(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            custom_print(f"{args.pattern_file}: No such file or directory")
    if not patterns:
        raise ValueError("No pattern provided")
    return patterns

def get_flags(args: argparse.Namespace) -> int:
    flags = re.IGNORECASE if args.i else 0
    if args.extended_regexp:
        flags |= re.VERBOSE
    return flags

def process_file(file: str, patterns: list, pattern_flags: int, args: argparse.Namespace, root: str = None):
    matches = []
    try:
        with open(file, 'r', encoding='UTF-8') as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()
                for pattern in patterns:
                    if args.w:
                        pattern = rf'\b{pattern}\b'
                    match_patterns = re.finditer(pattern, line, flags=pattern_flags)
                    if args.o:
                        for match in match_patterns:
                            if bool(match) != args.v:
                                matches.append((line_number, match.group()))
                    else:
                        if bool(re.search(pattern, line, flags=pattern_flags)) != args.v:
                            matches.append((line_number, line))
                            break
    except FileNotFoundError:
        custom_print(f"{file}: No such file or directory")
    return matches

def print_matches(matches: list, file: str, args: argparse.Namespace, root: str = None):
    if args.c:
        custom_print(f"{len(matches)}\n")
    elif args.l:
        if matches:
            custom_print(f"{file}\n")
    else:
        for line_number, match in matches:
            if len(args.file) > 1 and not args.q:
                if root:
                    custom_print(f"{os.path.join(root, file)}:")
                else:
                    custom_print(f"{file}:")
            if args.n:
                custom_print(f"{line_number}:")
            custom_print(f"{match}\n")

def grep(args: argparse.Namespace):
    patterns = parse_patterns(args)
    pattern_flags = get_flags(args)

    for file in args.file:
        if args.r and os.path.isdir(file):
            for root, _, files in os.walk(file):
                for f in files:
                    full_path = os.path.join(root, f)
                    matches = process_file(full_path, patterns, pattern_flags, args, root)
                    if matches: custom_print(f"{full_path}:")
                    print_matches(matches, full_path, args, root)
        else:
            matches = process_file(file, patterns, pattern_flags, args)
            print_matches(matches, file, args)
def main():
    parser = argparse.ArgumentParser(prog='MyGrep')
    parser.add_argument('-n', help='print line number with output lines', action='store_true')
    parser.add_argument('-v', help='invert match (select non-matching lines)', action='store_true')
    parser.add_argument('-i', help='ignore case distinctions in patterns and data', action='store_true')
    parser.add_argument('-E', '--extended-regexp', action='store_true', help='Use extended regular expressions')
    parser.add_argument('-w', action='store_true', help='Match whole words only')
    parser.add_argument('-c', action='store_true', help='Count the number of occurrences of the provided pattern')
    parser.add_argument('-l', action='store_true', help='Display file names with matches only')
    parser.add_argument('-o', action='store_true', help='Output matches only')
    parser.add_argument('-q', action='store_true',
                        help="don't display file names with matches only (analog -h in original grep)")
    parser.add_argument('-r', action='store_true', help='Recursively search directories')

    pattern_group = parser.add_argument_group('Pattern Options')
    pattern_group.add_argument('-e', '--regexp', action='append', help='Multiple patterns to search', type=str)
    pattern_group.add_argument('-f', '--pattern-file', action='store', help='Read pattern from file')
    pattern_group.add_argument('pattern', help='pattern to search', type=str, nargs='?')

    parser.add_argument('file', nargs='+', help='file to search', type=str)

    args = parser.parse_args()

    if not args.regexp and not args.pattern and not args.pattern_file:
        parser.error("You must provide at least one pattern using -e, as a positional argument, or using -f.")
    print("[INFO]]", args)
    grep(args)


if __name__ == '__main__':
    main()
