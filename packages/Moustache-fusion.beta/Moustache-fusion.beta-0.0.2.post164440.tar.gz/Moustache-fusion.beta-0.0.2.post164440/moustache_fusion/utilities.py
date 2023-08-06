# -*- coding: utf-8 -*-

import errno
import magic
import os
import subprocess

from itertools import count, product
from moustache_fusion.exceptions import CommandException, CorruptedPdfException, EncryptedPdfException, \
    MimeTypePdfException, ProtectedPdfException
from string import ascii_uppercase
from PyPDF2 import PdfFileReader

# Paths for all binaries needed in the Pdf utility class or the service.
PATHS = {
    'pdfgrep': '/usr/bin/pdfgrep',
    'pdfinfo': '/usr/bin/pdfinfo',
    'pdftk': '/usr/bin/pdftk'
}


def sequence_generator(iterables):
    """
    @see https://stackoverflow.com/a/14382997
    """
    for n in count(1):
        for s in product(iterables, repeat=n):
            yield ''.join(s)


def alphabet_generator():
    """
    Alphabet de lettre (A,B, ..., AB, AC).
    """
    return sequence_generator(ascii_uppercase)


class Pdf():
    @staticmethod
    def check_binaries():
        """
        Check that all binaries we need exist and are executable.
        """
        for alias, path in PATHS.items():
            if os.path.exists(path) is False:
                raise FileNotFoundError(errno.ENOENT, 'Binary not found', path)
            if os.access(path, os.X_OK) is False:
                raise PermissionError(errno.ENOEXEC, 'Binary is not executable', path)

    @staticmethod
    def validate(path: str):
        """
        Assert that
            - the file is a PDF
            - it is not encrypted or protected (using pdfinfo)
            - it is not corrupted (using PyPDF2.PdfFileReader)
        :raises
            CommandException
            CorruptedPdfException
            EncryptedPdfException
            MimeTypePdfException
            ProtectedPdfException
        """
        # 1. Check MIME type
        mime = magic.from_file(path, mime=True)
        if mime != 'application/pdf':
            msgstr = 'MIME type is not "application/pdf" (found "%s")'
            raise MimeTypePdfException(msgstr % mime)

        # 2. Check for a possible encrypted or protected PDF
        cmd = '{0} {1}'.format(PATHS['pdfinfo'], path)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True)
        stdout_content, stderr_content = process.communicate()

        if process.returncode == 1 and 'Incorrect password' in stderr_content:
            msgstr = 'Cannot open encrypted PDF'
            raise EncryptedPdfException(msgstr)
        elif process.returncode == 0 and 'Encrypted:      yes' in stdout_content:
            msgstr = 'Cannot process protected PDF'
            raise ProtectedPdfException(msgstr)
        elif process.returncode != 0:
            raise CommandException(
                'Error trying to check for a possible encrypted or protected PDF',
                command=cmd,
                returncode=process.returncode,
                stdout=process.stdout.decode('utf-8'),
                stderr=process.stderr.decode('utf-8')
            )

        # 3. Check for a possible corrupted PDF
        try:
            with open(path, 'rb') as file:
                PdfFileReader(file)
        except Exception:
            raise CorruptedPdfException('PDF seems to be corrupted')

    @staticmethod
    def get_page_count(path: str) -> int:
        """
        Returns the number of pages of a PDF document or raises a CommandException.
        """
        process = subprocess.run([PATHS['pdfinfo'], path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if process.returncode != 0:
            raise CommandException(
                'Error trying to get page count',
                command='%s %s' % (PATHS['pdfinfo'], path),
                returncode=process.returncode,
                stdout=process.stdout.decode('utf-8'),
                stderr=process.stderr.decode('utf-8')
            )

        lines = process.stdout.decode('utf-8').split()
        try:
            pageinfo = lines.index('Pages:')
        except ValueError:
            raise CommandException(
                'Could not find "Pages:" in output',
                command='%s %s' % (PATHS['pdfinfo'], path),
                returncode=process.returncode,
                stdout=process.stdout.decode('utf-8'),
                stderr=process.stderr.decode('utf-8')
            )

        line = lines[pageinfo + 1]
        if not line.isdigit():
            raise CommandException(
                'Could not find integer page count from output',
                command='%s %s' % (PATHS['pdfinfo'], path),
                returncode=process.returncode,
                stdout=process.stdout.decode('utf-8'),
                stderr=process.stderr.decode('utf-8')
            )

        return int(line)

    @staticmethod
    def get_pattern_pages(path: str, pattern: str) -> list:
        """
        Find all pages mentioning a pattern.
        Cache is used because a pattern can be used multiple times (pdfgrep 2.0+).
        """
        result = []

        cmd = '{0} --cache --color never --page-number "{1}" {2}'.format(PATHS['pdfgrep'], pattern, path)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True)
        stdout_content, stderr_content = process.communicate()

        if process.returncode == 0:
            stdout_content = stdout_content.split()
            for line in stdout_content:
                value = line.split(':')[0]
                if not value.isdigit():
                    msgstr = 'Could not read start page from line "%s"'
                    raise RuntimeError(msgstr % line)
                result.append(int(value))
        elif process.returncode != 1:
            raise CommandException(
                'Error trying to get pages with pattern "%s"' % pattern,
                command='%s %s' % (PATHS['pdfinfo'], path),
                returncode=process.returncode,
                stdout=process.stdout.decode('utf-8'),
                stderr=process.stderr.decode('utf-8')
            )

        return result
