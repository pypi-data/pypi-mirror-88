from BlobDescription import BlobDescription
from PyblobLogger import PyblobLogger

class PyblobLogging:

    def get_blob_logger(logger_name, blob_description):
        if not logger_name:
            raise TypeError('Please enter a descriptive logger_name!')
        elif not isinstance(blob_description, BlobDescription):
            raise TypeError('blob_description must be an instance of BlobDescription.')
        return PyblobLogger(logger_name, blob_description)
