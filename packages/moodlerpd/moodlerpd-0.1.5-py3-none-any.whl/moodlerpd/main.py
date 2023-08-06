#!/usr/bin/env python3
# coding=utf-8

import os
import argparse
import logging
import sys
import traceback

from logging.handlers import RotatingFileHandler

from moodlerpd.client.client_service import ClientService
from moodlerpd.config.config_service import ConfigService
from moodlerpd.downloads.download_service import DownloadService
from moodlerpd.downloads.fake_download_service import FakeDownloadService
from moodlerpd.utils.path_tools import PathTools

import moodlerpd.utils.process_lock as process_lock


def _dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError('"%s" is not a valid path. Make sure the directory exists.'
                                         % (str(path)))


def get_parser():
    """
    Creates a new arguments parser
    """
    parser = argparse.ArgumentParser(
        description='moodlerpd that downloads course content fast from moodle'
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        '--version', action='version', version='moodlerpd v0.1.5', help='Print program version'
    )

    group.add_argument(
        '--log-responses',
        default=False,
        action='store_true',
        help='To generate a responses.log file'
             + ' in which all JSON responses from Moodles are logged'
             + ' along with the requested URL.',
    )

    parser.add_argument(
        '-p',
        '--path',
        default='.',
        type=_dir_path,
        help=(
                'Sets the location of the configuration,'
                + ' logs and downloaded files. PATH must be an'
                + ' existing directory in which you have read and'
                + ' write access. (default: current working'
                + ' directory)'
        ),
    )

    parser.add_argument(
        '-t',
        '--threads',
        default=5,
        type=int,
        help='Sets the number of download threads. (default: %(default)s)',
    )

    parser.add_argument(
        '-v',
        '--verbose',
        default=False,
        action='store_true',
        help='Print various debugging information',
    )

    parser.add_argument(
        '--skip-cert-verify',
        default=False,
        action='store_true',
        help='If this flag is set, the SSL certificate '
             + 'is not verified. This option should only be used in '
             + 'non production environments.',
    )

    parser.add_argument(
        '--no-download',
        default=False,
        action='store_true',
        help='If this flag is set, no files are downloaded.'
             + ' This allows the local database to be updated without'
             + ' having to download all files.',
    )

    return parser


def run_app(storage_path, verbose=False, skip_cert_verify=False,
            without_downloading_files=False, log_responses=False):
    log_formatter = logging.Formatter('%(asctime)s  %(levelname)s  {%(module)s}  %(message)s',
                                      '%Y-%m-%d %H:%M:%S')

    log_file = os.path.join(storage_path, 'moodlerpd.log')

    file_log_handler = RotatingFileHandler(
        log_file, mode='a', maxBytes=1 * 1024 * 1024, backupCount=2, encoding='utf-8', delay=False
    )

    file_log_handler.setFormatter(log_formatter)

    if verbose:
        file_log_handler.setLevel(logging.DEBUG)
    else:
        file_log_handler.setLevel(logging.INFO)

    app_log = logging.getLogger()

    if verbose:
        app_log.setLevel(logging.DEBUG)
    else:
        app_log.setLevel(logging.INFO)

    app_log.addHandler(file_log_handler)

    stream_log_handler = logging.StreamHandler(sys.stdout)

    app_log.addHandler(stream_log_handler)

    logging.info("moodlerpd started...")

    try:
        logging.info('Loading config in directory "%s"', storage_path)
        config = ConfigService(storage_path)
        config.load()
    except BaseException as e:
        logging.error('Error while trying to load the config! %s', e, extra={'exception': e})
        sys.exit(-1)

    PathTools.restricted_filenames = config.get_restricted_filenames()

    try:
        process_lock.lock(storage_path)

        client = ClientService(config, storage_path, skip_cert_verify, log_responses)

        logging.info('Checking for changes for the configured Moodle-Account....')

        changed_courses = client.fetch_state()

        if without_downloading_files:
            downloader = FakeDownloadService(changed_courses, client, storage_path)
        else:
            downloader = DownloadService(changed_courses, client, storage_path, skip_cert_verify)

        downloader.run()

        changed_courses_to_notify = client.recorder.changes_to_notify()

        if len(changed_courses_to_notify) > 0:

            logging.info('Changed found in the Moodle-Account')

            client.recorder.notified(changed_courses_to_notify)

        else:
            logging.info('No changes found for the configured Moodle-Account.')

        process_lock.unlock(storage_path)

        logging.info('All done. Exiting...')

    except BaseException as e:
        if not isinstance(e, process_lock.LockError):
            process_lock.unlock(storage_path)

        error_formatted = traceback.format_exc()
        logging.error(error_formatted, extra={'exception': e})
        sys.exit(-1)


def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)

    run_app(args.path, args.verbose, args.skip_cert_verify,
            args.no_download, args.log_responses)
