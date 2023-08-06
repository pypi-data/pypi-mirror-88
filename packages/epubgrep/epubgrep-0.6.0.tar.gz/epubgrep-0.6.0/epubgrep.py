#!/usr/bin/env python3
import argparse
import concurrent.futures
import logging
import os.path
import re
import sys
import zipfile

from typing import Any, Dict, List, Optional, Tuple

import epub_meta

logging.basicConfig(format='%(levelname)s:%(funcName)s:%(message)s',
                    level=logging.INFO)
log = logging.getLogger('epubgrep')


def get_chapter_title(mdata: List[Dict[str, Any]], fname: str) \
        -> Optional[Tuple[str, int]]:
    if mdata is not None:
        found_list = [(x['title'], x['index'])
                      for x in mdata if x['src'] == fname]
        if len(found_list) > 0:
            chap_title = found_list[0][0].strip(' \t.0123456789')
            return chap_title, found_list[0][1]
        else:
            return ('Unknown', 0)


def _colorize_found(dline: str, res: re.Match, col: bool) -> str:
    out = ''
    if col:
        found_line = dline.replace(
            res.group(1),
            "\033[31;1m" + res.group(1) + "\033[31;0m")
        out += '{}\n'.format(found_line)
    else:
        out += dline + '\n'
    return out


def _multiline_search(inf, sought_RE, printed_booktitle, filename,
                      counting, w_counting, metadata, zif) -> Tuple[int, str]:
    out = ""
    count = 0
    decoded_str = inf.read().decode(errors='replace')
    res = sought_RE.search(decoded_str)
    if res:
        if not printed_booktitle:
            out += '{}\n'.format(filename)
            printed_booktitle = True
        if counting or w_counting:
            count += 1
        else:
            chap_info = get_chapter_title(metadata.toc,
                                          zif.filename)
            out += "{}. {}:\n\n".format(chap_info[1], chap_info[0])
            out += '{}\n\n'.format(res.group(0))
    return count, out


def _singleline_search(inf, sought_RE, out_title, filename, counting,
                       w_counting, printed_booktitle, metadata, zif, color,
                       count) -> Tuple[int, str]:
    out = ""
    count = 0
    printed_title = False
    for line in inf:
        decoded_line = line.decode(errors='replace').strip()
        res = sought_RE.search(decoded_line)
        if res:
            if not out_title:
                out_title = '{}'.format(filename)
            if counting or w_counting:
                count += 1
            else:
                if not printed_booktitle:
                    out += out_title + '\n'
                    printed_booktitle = True
                if not printed_title:
                    chap_info = get_chapter_title(metadata.toc,
                                                  zif.filename)
                    if chap_info is not None:
                        out += "{}. {}:\n\n".format(chap_info[1],
                                                    chap_info[0])
                        printed_title = True
            if not (counting or w_counting):
                out += _colorize_found(decoded_line, res, color)
    return count, out


def _description_search(mdata: dict, sre: re.Pattern, fname: str,
                        col: bool) -> str:
    out = ''
    decoded_line = mdata['description']
    if decoded_line is None:
        return out

    res = sre.search(decoded_line)
    if res:
        title = '{}'.format(fname)
        out += title + '\n'
        out += _colorize_found(decoded_line, res, col)
    return out


def grep_book(filename: str, pattern: str, flags: int, desc: bool = False,
              counting: bool = False, w_counting: bool = False,
              color: bool = False) -> Optional[str]:
    assert os.path.isfile(filename), "{} is not EPub file.".format(filename)
    sought_RE = re.compile('(' + pattern + ')', flags)
    count = 0
    icount = 0
    out_title = ''
    out = ''
    iout = ''

    mline = flags & re.M == re.M

    try:
        metadata = epub_meta.get_epub_metadata(filename)
    except (epub_meta.EPubException, KeyError, IndexError):
        log.exception('Failed to open {}'.format(filename))
        return None
    book = zipfile.ZipFile(filename)
    printed_booktitle = False

    if desc:
        return _description_search(metadata, sought_RE, filename, color)

    for zif in book.infolist():
        with book.open(zif) as inf:
            if mline:
                icount, iout = _multiline_search(inf, sought_RE,
                                                 printed_booktitle, filename,
                                                 counting, w_counting,
                                                 metadata, zif)
                count += icount
                out += iout
            else:
                icount, iout = _singleline_search(inf, sought_RE, out_title,
                                                  filename, counting,
                                                  w_counting,
                                                  printed_booktitle, metadata,
                                                  zif, color, count)
                count += icount
                out += iout

    if count > 0:
        if counting:
            out += '{:02d}:{}'.format(count, out_title)
        if w_counting:
            size = metadata['file_size_in_bytes']
            out += '{:05d}:{}'.format(int((count/size)*1e5), out_title)

    return out


def main():
    parser = argparse.ArgumentParser(description='Grep through EPub book')
    parser.add_argument('pattern')
    parser.add_argument('files', nargs='+')
    parser.add_argument('-c', '--count',
                        action='store_true',
                        help="just counts of found patterns")
    parser.add_argument('-C', '--weighted-count',
                        action='store_true',
                        help="counts of found patterns as a proportion of whole text")
    parser.add_argument('-d', '--description',
                        action='store_true',
                        help="search just in descriptions")
    parser.add_argument('-i', '--ignore-case',
                        action='store_true',
                        help="make search case insensitive")
    parser.add_argument('-o', '--color', '--colour',
                        action='store_false',
                        help="Do NOT mark found patterns with color")
    parser.add_argument('-m', '--multi-line',
                        action='store_true',
                        help="make search multi line")
    args = parser.parse_args()
    # log.debug('args = %s', args)

    search_flags = 0
    if args.ignore_case:
        search_flags |= re.I

    if args.multi_line:
        search_flags |= re.M | re.S

    with concurrent.futures.ProcessPoolExecutor() as executor:
        fut_to_fname = {executor.submit(grep_book,
                                        os.path.realpath(filename),
                                        args.pattern, search_flags,
                                        args.description,
                                        args.count, args.weighted_count,
                                        args.color):
                        filename for filename in args.files}
    for future in concurrent.futures.as_completed(fut_to_fname):
        try:
            data = future.result()
            if data:
                data = data.rstrip()
            if (data is not None) and len(data) > 0:
                print(data)
        except (BrokenPipeError, KeyboardInterrupt):
            sys.exit()


if __name__ == '__main__':
    main()
