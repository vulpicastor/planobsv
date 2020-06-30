#!/usr/bin/env python3
#
# Copyright (c) 2020 Lizhou Sha
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import itertools
import os.path as path

def parse_args():
    parser = argparse.ArgumentParser(description="Chain the given observing plans for iTelescope.")
    parser.add_argument(
        '-o', '--output', metavar='FILE', dest="output", type=str, help='Output filename pattern.')
    parser.add_argument('PLAN', nargs='+', help='Unchained observing plans.')
    return parser.parse_args()

def output_names(filename, length):
    root, ext = path.splitext(filename)
    outputs = []
    for i in range(length):
        outputs.append(f'{root}_{i:04d}{ext}')
    return outputs

def write_chained_plan(plan_text, output_file, next_file):
    # Because of the zip_longest in write_chained_plans(), the end of the
    # observation chain is signaled by next_file being None.
    if next_file is not None:
        chain_line = f"#chain {next_file}\n"
    with open(output_file, 'w') as f:
        f.write(plan_text)
        if next_file is not None:
            f.write(chain_line)

def write_chained_plans(input_files, output_files):
    file_cache = dict()
    for infile, outfile, nextfile in itertools.zip_longest(
            input_files, output_files, output_files[1:]):
        if infile in file_cache:
            plan_text = file_cache[infile]
        else:
            with open(infile) as f:
                plan_lines = f.read().splitlines()
            plan_lines.append('')
            plan_text = '\n'.join(plan_lines)
            file_cache[infile] = plan_text
        write_chained_plan(plan_text, outfile, nextfile)


def main():
    args = parse_args()
    length = len(args.PLAN)
    if length < 2:
        raise ValueError('You need to chain at least two files.')
    if length > 9999:
        raise ValueError('Too many input files.')
    output_files = output_names(args.output, length)
    write_chained_plans(args.PLAN, output_files)

if __name__ == '__main__':
    main()
