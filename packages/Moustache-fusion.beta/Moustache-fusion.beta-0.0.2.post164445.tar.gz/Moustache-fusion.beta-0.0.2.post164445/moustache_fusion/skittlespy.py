# -*- coding: utf-8 -*-

import subprocess
from PyPDF2 import PdfFileWriter, PdfFileReader
import copy
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import tempfile

from moustache_fusion.logger import logger
from moustache_fusion.datatransfer import SwapRequest
from moustache_fusion.exceptions import CommandException, MoustacheSwapOverflowException, PatternNonUniqueException, \
    PatternNotFoundException
from moustache_fusion.utilities import alphabet_generator, PATHS, Pdf


def set_inner_pdfs_page_count(swap_request: SwapRequest):
    """
    Read page count for every annexe file.
    """
    logger().debug('Reading page count for every inner PDF document...')

    for pdf in swap_request.inner_pdfs:
        try:
            pdf.length = Pdf.get_page_count(pdf.path)
        except CommandException as exc:
            exc.message = '%s for annexe "%s"' % (exc.message, pdf.name)
            raise exc

    logger().debug('...reading page count for every inner PDF document done')


def set_annexe_pattern_pages(swap_request: SwapRequest):
    """
    Try to find all pages mentioning the patterns.
    """
    logger().debug('Searching for patterns in main document "%s" ...' % swap_request.main_pdf.path)

    new_annexes = []
    for pdf in swap_request.inner_pdfs:
        logger().debug('...searching for pattern "%s" ...' % pdf.pattern)

        pages = Pdf.get_pattern_pages(swap_request.main_pdf.path, pdf.pattern)
        if len(pages) == 0:
            msgstr = 'Pattern "%s" not found in main document %s'
            raise PatternNotFoundException(msgstr % (pdf.pattern, swap_request.main_pdf.path))

        for page in pages:
            new_pdf = copy.deepcopy(pdf)
            new_pdf.start = page
            new_annexes.append(new_pdf)

    logger().debug('...searching for patterns in main document "%s" done' % swap_request.main_pdf.path)
    swap_request.inner_pdfs = new_annexes


def replace_annexes(swap_request: SwapRequest, temp_directory):
    """
    create and execute script to replace annexes
    cmd = "/usr/bin/pdftk A=main.pdf B=annexe.pdf cat A1-10 B A12-end output generated.pdf"
    """
    # generate handles (/usr/bin/pdftk A=main.pdf B=annexe.pdf)
    # Sort inner PDF documents by position
    swap_request.inner_pdfs.sort(key=lambda pdf: pdf.start)

    handles_generator = alphabet_generator()

    swap_request.main_pdf.handle = next(handles_generator)
    cmd = "{0} {1}={2} ".format(PATHS['pdftk'], swap_request.main_pdf.handle, swap_request.main_pdf.path)

    for pdf in swap_request.inner_pdfs:
        pdf.handle = next(handles_generator)
        cmd += "{0}={1} ".format(pdf.handle, pdf.path)

    # (cat A1-10 B A12-end output generated.pdf)
    cmd += "cat "
    current = 1
    max_pages = Pdf.get_page_count(swap_request.main_pdf.path)

    for pdf in swap_request.inner_pdfs:
        if current <= pdf.start - 1:
            cmd += "{0}{1}-{2} {3} ".format(
                swap_request.main_pdf.handle,
                current,
                pdf.start - 1,
                pdf.handle
            )
        elif current == pdf.start:
            cmd += "{0} ".format(pdf.handle)
        else:
            msgstr = 'Trying to insert inner PDF "%s" at page %d while current page is already %d'
            raise MoustacheSwapOverflowException(msgstr % (pdf.name, pdf.start, current))

        if current + pdf.length > max_pages + 1:
            msgstr = 'Trying to insert inner PDF "%s" with %d page(s) at page %d while the main document only has \
%d page(s)'
            raise MoustacheSwapOverflowException(msgstr % (pdf.name, pdf.length, current, max_pages))

        current = pdf.start + pdf.length

    # Check if there are remaining pages from the main PDF document
    if current <= max_pages:
        cmd += "{0}{1}-end".format(swap_request.main_pdf.handle, current)

    output_file = tempfile.NamedTemporaryFile(dir=temp_directory, delete=False, suffix='.pdf').name
    cmd += " output {0}".format(output_file)

    logger().debug(cmd)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout_content, stderr_content = process.communicate()
    if process.returncode != 0:
        raise CommandException(
            'Error while replacing inner PDF documents in main PDF document',
            command=cmd,
            returncode=process.returncode,
            stdout=stdout_content,
            stderr=stderr_content
        )

    return output_file


def add_inner_pdfs_page_numbers(swap_request, temp_directory):
    logger().debug('Adding page numbers to inner PDF files...')

    for inner_pdf in swap_request.inner_pdfs:
        msgstr = '...adding page numbers to inner PDF file "%s" (alias "%s")...'
        logger().debug(msgstr % (inner_pdf.name, inner_pdf.alias))
        original_file = PdfFileReader(open(inner_pdf.path, 'rb'))

        output = PdfFileWriter()
        start = inner_pdf.start
        end = start + inner_pdf.length
        increment = 0
        while start < end:
            packet = io.BytesIO()
            # @todo: get real page size / orientation
            # @see https://pythonhosted.org/PyPDF2/PageObject.html#PyPDF2.pdf.PageObject
            le_can = canvas.Canvas(packet, pagesize=A4)
            le_can.setFont(swap_request.options.fontName, swap_request.options.fontSize)
            le_can.drawString(swap_request.options.pos_x, swap_request.options.pos_y, "{0}".format(start))
            le_can.save()

            # move to the beginning of the buffer
            packet.seek(0)
            new_pdf = PdfFileReader(packet)

            logger().debug("%s cur=%d [%d-%d]" % (inner_pdf.path, increment, start, end))
            page = original_file.getPage(increment)
            page.mergePage(new_pdf.getPage(0))
            output.addPage(page)
            increment += 1
            start += 1

        # finally, write "output" to a real file
        result_path = tempfile.NamedTemporaryFile(delete=False, dir=temp_directory, suffix='.pdf').name
        output_stream = open(result_path, 'wb')
        output.write(output_stream)
        output_stream.close()
        logger().debug("%s to %s" % (inner_pdf.path, result_path))
        inner_pdf.path = result_path

    logger().debug('...done adding page numbers to inner PDF files')


def check_patterns(swap_request: SwapRequest) -> None:
    """
    Check that all patterns are unique or raise an exception.
    @todo: merge with checks done in WS (MIME, non-corrupted PDF, ...)
    """
    found = {}
    logger().debug('%s' % swap_request.inner_pdfs)
    for pdf in swap_request.inner_pdfs:
        if pdf.pattern in found:
            msgstr = 'Non unique pattern "%s" found for file "%s" (already found for file "%s")'
            raise PatternNonUniqueException(msgstr % (pdf.pattern, pdf.name, found[pdf.pattern]))
        found[pdf.pattern] = pdf.name


def swap(swap_request: SwapRequest, temp_directory: str) -> str:
    logger().debug('skittles starts')

    # @todo: in WS
    check_patterns(swap_request)

    set_inner_pdfs_page_count(swap_request)
    set_annexe_pattern_pages(swap_request)

    if swap_request.with_annexes_pages_numbered:
        add_inner_pdfs_page_numbers(swap_request, temp_directory)
    else:
        logger().debug('No page number to add')

    output_file = replace_annexes(swap_request, temp_directory)
    logger().debug('file created: %s' % output_file)
    return output_file


def get_available_fonts() -> list:
    """
    Returns a list of all available fonts to use when inserting page numbers.
    """
    from reportlab.pdfbase import pdfmetrics
    result = []
    for font_name in pdfmetrics.standardFonts:
        result.append(font_name)
    return result
