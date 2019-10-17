#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""dirwatcher assignment"""

__author__ = "tamekiaNelson"

import logging
import datetime
import time
import argparse
import os
import signal

logger = logging.getLogger(__name__)
file_trace_dict = {}
exit_flag = False


def watch_directory(args):
    time.sleep(args.interval)
    dir_files = os.listdir(args.path)
    for f in dir_files:
        if f.endswith(args.ext) and f not in file_trace_dict:
            file_trace_dict[f] = 1
            logger.info("ALERT, now watching file {}".format(f))
    for file in file_trace_dict:
        if file not in dir_files:
            del file_trace_dict[file]
            logger.info(
                "ALERT, file {} was removed from tracking".format(file))
    for file in file_trace_dict:
        last_line = search_text(file, file_trace_dict[file], args.text)
        file_trace_dict[file] = last_line


def search_text(filename, skip_line, magic_text):
    """reports all magic words in file starting after skipped line"""
    i = 0
    with open(filename) as f:
        for i, line in enumerate(f, 1):
            if i < skip_line:
                continue
            if magic_text in line:
                logger.info(
                    "Found search word {} on line {} in file {}".format(
                        magic_text, i, filename))
        # returns last line read of file
        return i


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here
    as well (SIGHUP?)
    Basically it just sets a global flag, and main() will exit it's loop if the
    signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    # log the associated signal name (the python3 way)
    logger.warn('Received ' + signal.Signals(sig_num).name)
    # log the signal name (the python2 way)
    # logger.warn('Received ' + signames[sig_num])
    signames = dict((k, v) for v, k in reversed(
            sorted(signal.__dict__.items()))
                    if v.startswith('SIG') and not v.startswith('SIG_'))
    logger.warn('Received ' + signames[sig_num])
    global exit_flag
    exit_flag = True


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--ext", type=str, default=".txt",
                        help="Text file extension to watch")
    parser.add_argument("-i", "--interval", type=float, default=1.0,
                        help="How often to watch the text files")
    parser.add_argument("path", help="Directory to watch")
    parser.add_argument("magic", help="String to watch for")
    return parser


def main():
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s'
        '[%(threadName)-12s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    logger.setLevel(logging.DEBUG)
    app_start_time = datetime.datetime.now()
    # Hook these two signals from the OS ..
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends either of these
    # to my process.
    parser = create_parser()
    args = parser.parse_args()
    uptime = datetime.datetime.now() - app_start_time
    logger.info("Starting dirwatcher, looking for magic text")
    while not exit_flag:
        try:
            # call my directory watching function..
            watch_directory(args)
            time.sleep(args.interval)
        except OSError as e:
            logger.error("Directory not found {}".format(e))
            time.sleep(5.0)

        except Exception as e:
            # Log an ERROR level message here
            logger.error("Unhandled Exception {}".format(e))
            time.sleep(5.0)
            # This is an UNHANDLED exception
            # put a sleep inside my while loop so I don't peg the cpu
            # usage at 100%
    # final exit point happens here
    # Log a message that we are shutting down
    # Include the overall uptime since program start.
    logger.info(
        '\n'
        '----------------------------------------------------\n'
        '   Stopped {0}\n'
        '   Uptime was {1}\n'
        '----------------------------------------------------\n'
        .format(__file__, str(uptime))
    )


if __name__ == '__main__':
    main()
