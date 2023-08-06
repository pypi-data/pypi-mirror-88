from dkpro_cassis_tools import load_cas_from_zip_file
from dkpro_cassis_tools.get_document_meta_data import get_document_meta_data


def test_get_document_meta_data():
    with open('data/cas.zip', 'rb') as f:
        cas = load_cas_from_zip_file(f)
    document_meta_data = get_document_meta_data(cas)
    assert document_meta_data.documentTitle == 'Test'
    assert document_meta_data.documentId == 'Ángela'
