# -*- coding: utf-8 -*-

import pytest
import re
import sys

from moustache_fusion.exceptions import CommandException, CorruptedPdfException, EncryptedPdfException, \
    MimeTypePdfException, ProtectedPdfException
from moustache_fusion.utilities import Pdf
from tests.helpers import get_fixture_path

sys.path.append('/app/moustache_fusion')


@pytest.mark.parametrize('path, expected', [
    ('main10p_m3p_i3p_m1p_i1p_m2p/main.pdf', 10),
    ('inner_3_pages/lorem_ipsum.pdf', 3),
    ('inner_1_page/edgar_allan_poe_murders.pdf', 1)
])
def test_get_page_count_success(path, expected):
    assert expected == Pdf.get_page_count(get_fixture_path(path))


def test_get_page_count_failure_command_exception():
    with pytest.raises(CommandException) as exc_info:
        path = get_fixture_path('main10p_m3p_i3p_m1p_i1p_m2p/success_with_annexes_pages_numbered_false.json')
        Pdf.get_page_count(path)

    assert exc_info.value.message == 'Error trying to get page count'
    assert exc_info.value.returncode == 1
    assert re.match(r'Syntax Warning: May not be a PDF file', exc_info.value.stderr) is not None
    assert exc_info.value.command == '/usr/bin/pdfinfo ' \
           + '/app/tests/fixtures/main10p_m3p_i3p_m1p_i1p_m2p/success_with_annexes_pages_numbered_false.json'


@pytest.mark.parametrize('path, pattern, expected', [
    ('main11p_m3p_i1p_m1p_i1pr_i1_m1p_i1pr_m1p_i1p/main.pdf', 'PDF_1', [4, 6]),
    ('main11p_m3p_i1p_m1p_i1pr_i1_m1p_i1pr_m1p_i1p/main.pdf', 'PDF_2', [7, 9]),
    ('main11p_m3p_i1p_m1p_i1pr_i1_m1p_i1pr_m1p_i1p/main.pdf', 'PDF_3', [11]),
    ('main11p_m3p_i1p_m1p_i1pr_i1_m1p_i1pr_m1p_i1p/main.pdf', 'PDF_4', []),
])
def test_get_get_pattern_pages_success(path, pattern, expected):
    assert expected == Pdf.get_pattern_pages(get_fixture_path(path), pattern)


def test_validate_success():
    assert Pdf.validate(get_fixture_path('main10p_m3p_i3p_m1p_i1p_m2p/main.pdf')) is None


@pytest.mark.parametrize('path, exception_class, exception_message', [
    (
            'main10p_m3p_i3p_m1p_i1p_m2p/main.odt',
            MimeTypePdfException,
            'MIME type is not "application/pdf" (found "application/vnd.oasis.opendocument.text")'
    ),
    (
            'main10p_m3p_i3p_m1p_i1p_m2p/main-corrupted.pdf',
            CorruptedPdfException,
            'PDF seems to be corrupted'
    ),
    (
            'inner_3_pages/lorem_ipsum-corrupted.pdf',
            CorruptedPdfException,
            'PDF seems to be corrupted'
    ),
    (
            'main10p_m3p_i3p_m1p_i1p_m2p/main-with_document_open_password.pdf',
            EncryptedPdfException,
            'Cannot open encrypted PDF'
    ),
    (
            'main10p_m3p_i3p_m1p_i1p_m2p/main-with_permission_password.pdf',
            ProtectedPdfException,
            'Cannot process protected PDF'
    ),
    (
            'inner_1_page/edgar_allan_poe_murders-with_permission_password.pdf',
            ProtectedPdfException,
            'Cannot process protected PDF'
    )
])
def test_validate_failure_invalid_pdf_exception(path, exception_class, exception_message):
    with pytest.raises(exception_class) as exc_info:
        Pdf.validate(get_fixture_path(path))

    assert exc_info.value.args[0] == exception_message
