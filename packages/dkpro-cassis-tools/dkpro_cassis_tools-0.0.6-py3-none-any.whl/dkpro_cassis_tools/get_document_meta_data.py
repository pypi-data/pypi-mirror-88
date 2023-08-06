from cassis import Cas
from dkpro_cassis_tools.ns import DOCUMENT_METADATA


def get_document_meta_data(cas: Cas):
    document_meta_data_all = cas.select(DOCUMENT_METADATA)
    if document_meta_data_all:
        return document_meta_data_all[0]
    return None