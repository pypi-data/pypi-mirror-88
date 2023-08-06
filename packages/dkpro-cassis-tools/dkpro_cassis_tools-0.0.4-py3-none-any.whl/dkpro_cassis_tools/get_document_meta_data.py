from cassis import Cas
from dkpro_cassis_tools.ns import DOCUMENT_METADATA


def get_document_meta_data(cas: Cas):
    document_meta_data_all = cas.select(DOCUMENT_METADATA)
    try:
        document_meta_data = next(document_meta_data_all)
    except StopIteration:
        document_meta_data = None

    return document_meta_data