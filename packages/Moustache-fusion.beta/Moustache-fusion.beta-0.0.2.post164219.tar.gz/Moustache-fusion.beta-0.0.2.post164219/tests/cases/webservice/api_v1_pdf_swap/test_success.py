# -*- coding: utf-8 -*-

import sys

from tests.helpers.api import api_v1_pdf_swap_helper
from tests.helpers.comparison import compare_response_to_reference, expected_same_exported_images

sys.path.append('/app/moustache_fusion')


def test_main1p_i1p(client, tmpdir):
    """
    Test replacement of the first and unique page.
    """
    data = {
        'main': 'main1p_i1p/main.pdf',
        'data': 'main1p_i1p/data.json',
        'inner': [
            'inner_1_page/edgar_allan_poe_murders.pdf'
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 46000 <= response.content_length <= 47000

    case_path = 'webservice/api_v1_pdf_swap/main1p_i1p'
    assert compare_response_to_reference(tmpdir, response, case_path) == expected_same_exported_images(1)


def test_main1p_m1p(client, tmpdir):
    """
    Test when there is nothing to replace.
    @todo: 410 if there is nothing to replace
    """
    data = {
        'main': 'main1p_m1p/main.pdf',
        'data': 'main1p_m1p/data.json',
        'inner': []
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 14000 <= response.content_length <= 15000

    case_path = 'webservice/api_v1_pdf_swap/main1p_m1p'
    assert compare_response_to_reference(tmpdir, response, case_path) == expected_same_exported_images(1)


def test_main4p_m1p_i1p_m1p_i1p(client, tmpdir):
    """
    Test main document and inner documents alternation, starting with a page from the main document and ending with an
    inner document.
    """
    data = {
        'main': 'main4p_m1p_i1p_m1p_i1p/main.pdf',
        'data': 'main4p_m1p_i1p_m1p_i1p/data.json',
        'inner': [
            'inner_1_page/dylan_thomas_night.pdf',
            'inner_1_page/dylan_thomas_wood.pdf'
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 103000 <= response.content_length <= 104000

    case_path = 'webservice/api_v1_pdf_swap/main4p_m1p_i1p_m1p_i1p'
    assert compare_response_to_reference(tmpdir, response, case_path) == expected_same_exported_images(4)


def test_main4p_i1p_m1p_i1p_m1p(client, tmpdir):
    """
    Test main document and inner documents alternation, starting with an inner document and ending with a page from the
    main document.
    """
    data = {
        'main': 'main4p_i1p_m1p_i1p_m1p/main.pdf',
        'data': 'main4p_i1p_m1p_i1p_m1p/data.json',
        'inner': [
            'inner_1_page/dylan_thomas_night.pdf',
            'inner_1_page/dylan_thomas_wood.pdf'
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 103000 <= response.content_length <= 104000

    case_path = 'webservice/api_v1_pdf_swap/main4p_i1p_m1p_i1p_m1p'
    assert compare_response_to_reference(tmpdir, response, case_path) == expected_same_exported_images(4)


def test_main10p_m3p_i3p_m1p_i1p_m2p_numbered_false(client, tmpdir):
    data = {
        'main': 'main10p_m3p_i3p_m1p_i1p_m2p/main.pdf',
        'data': 'main10p_m3p_i3p_m1p_i1p_m2p/success_with_annexes_pages_numbered_false.json',
        'inner': [
            'inner_3_pages/lorem_ipsum.pdf',
            'inner_1_page/edgar_allan_poe_murders.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 141000 <= response.content_length <= 142000

    case_path = 'webservice/api_v1_pdf_swap/main10p_m3p_i3p_m1p_i1p_m2p_numbered_false'
    assert compare_response_to_reference(tmpdir, response, case_path) == expected_same_exported_images(10)


def test_main10p_m3p_i3p_m1p_i1p_m2p_numbered_true(client, tmpdir):
    data = {
        'main': 'main10p_m3p_i3p_m1p_i1p_m2p/main.pdf',
        'data': 'main10p_m3p_i3p_m1p_i1p_m2p/success_with_annexes_pages_numbered_true.json',
        'inner': [
            'inner_3_pages/lorem_ipsum.pdf',
            'inner_1_page/edgar_allan_poe_murders.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 205000 <= response.content_length <= 206000

    case_path = 'webservice/api_v1_pdf_swap/main10p_m3p_i3p_m1p_i1p_m2p_numbered_true'
    assert compare_response_to_reference(tmpdir, response, case_path) == expected_same_exported_images(10)


def test_main10p_m3p_i3p_m1p_i1p_m2p_numbered_true_with_embedded_odt(client, tmpdir):
    data = {
        'main': 'main10p_m3p_i3p_m1p_i1p_m2p/main-with_embedded_odt.pdf',
        'data': 'main10p_m3p_i3p_m1p_i1p_m2p/success_with_annexes_pages_numbered_true.json',
        'inner': [
            {'inner_3_pages/lorem_ipsum-with_embedded_odt.pdf': 'lorem_ipsum.pdf'},
            {'inner_1_page/edgar_allan_poe_murders-with_embedded_odt.pdf': 'edgar_allan_poe_murders.pdf'},
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 205000 <= response.content_length <= 206000

    case_path = 'webservice/api_v1_pdf_swap/main10p_m3p_i3p_m1p_i1p_m2p_numbered_true'
    output_dir = 'webservice/api_v1_pdf_swap/main10p_m3p_i3p_m1p_i1p_m2p_numbered_true_with_embedded_odt'
    assert compare_response_to_reference(tmpdir, response, case_path, output_dir) == expected_same_exported_images(10)


def fixme_test_main10p_m3p_i3p_m1p_i1p_m2p_numbered_true_with_pdf_a_1a(client, tmpdir):
    # @fixme: differences PDF vs. PDF/A-1a -> do that with another document, page 4 (LIp1) only
    data = {
        'main': 'main10p_m3p_i3p_m1p_i1p_m2p/main-pdf_a_1a.pdf',
        'data': 'main10p_m3p_i3p_m1p_i1p_m2p/success_with_annexes_pages_numbered_true.json',
        'inner': [
            {'inner_3_pages/lorem_ipsum-pdf_a_1a.pdf': 'lorem_ipsum.pdf'},
            {'inner_1_page/edgar_allan_poe_murders-pdf_a_1a.pdf': 'edgar_allan_poe_murders.pdf'},
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 215000 <= response.content_length <= 216000

    case_path = 'webservice/api_v1_pdf_swap/main10p_m3p_i3p_m1p_i1p_m2p_numbered_true'
    output_dir = 'webservice/api_v1_pdf_swap/main10p_m3p_i3p_m1p_i1p_m2p_numbered_true_with_pdf_a_1a'
    assert compare_response_to_reference(tmpdir, response, case_path, output_dir) == expected_same_exported_images(10)


def test_main11p_m3p_i1p_m1p_i1pr_i1_m1p_i1pr_m1p_i1p(client, tmpdir):
    """
    @info: covers 2 cases
        - some inner PDF are used multiple times
        - the last page is not from the main content
    """
    data = {
        'main': 'main11p_m3p_i1p_m1p_i1pr_i1_m1p_i1pr_m1p_i1p/main.pdf',
        'data': 'main11p_m3p_i1p_m1p_i1pr_i1_m1p_i1pr_m1p_i1p/success_with_annexes_pages_numbered_true.json',
        'inner': [
            'inner_1_page/dylan_thomas_night.pdf',
            'inner_1_page/edgar_allan_poe_murders.pdf',
            'inner_1_page/dylan_thomas_wood.pdf',
        ]
    }
    response = api_v1_pdf_swap_helper(client, data)

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=result.pdf'
    assert response.headers['Content-Type'] == 'application/pdf'
    assert 254000 <= response.content_length <= 255000

    case_path = 'webservice/api_v1_pdf_swap/main11p_m3p_i1p_m1p_i1pr_i1_m1p_i1pr_m1p_i1p'
    assert compare_response_to_reference(tmpdir, response, case_path) == expected_same_exported_images(11)
