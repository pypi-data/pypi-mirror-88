import os, sys, logging, time, socket
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient

class PyblobLogger:

    DEBUG_LEVEL = logging.DEBUG
    ERROR_LEVEL = logging.ERROR
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(message)s'
    DIRECTORY_NAME_LENGTH = 5

    ip_address = socket.gethostbyname(socket.gethostname())

    def __init__(self, logger_name, blob_description):
        self.logger_name = logger_name
        self.blob_description = blob_description
        self.setup_debug_logger(self.logger_name)
        self.setup_error_logger(self.logger_name)

    def get_debug_logs_name(self):
        logs_file_name = 'logs_{}_{}.txt'.format(self.ip_address, time.strftime("%Y-%m-%d"))
        return os.path.join(self.blob_description.project_local_path, 'debug/', logs_file_name)

    def get_error_logs_name(self):
        logs_file_name = 'logs_{}_{}.txt'.format(self.ip_address, time.strftime("%Y-%m-%d"))
        return os.path.join(self.blob_description.project_local_path, 'error/', logs_file_name)

    def setup_debug_logger(self, logger_name):
        self.debug_logger = logging.getLogger('DEBUG - ' + logger_name)
        self.debug_logger.setLevel(self.DEBUG_LEVEL)
	 
        file_handler = logging.FileHandler(self.get_debug_logs_name())
        file_handler.setLevel(self.DEBUG_LEVEL)

        formatter = logging.Formatter(self.LOGGING_FORMAT)
        file_handler.setFormatter(formatter)

        self.debug_logger.addHandler(file_handler)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        
        self.debug_logger.addHandler(console_handler)

    def setup_error_logger(self, logger_name):
        self.error_logger = logging.getLogger('ERROR - ' + logger_name)
        self.error_logger.setLevel(self.ERROR_LEVEL)

        file_handler = logging.FileHandler(self.get_error_logs_name())
        file_handler.setLevel(self.ERROR_LEVEL)

        formatter = logging.Formatter(self.LOGGING_FORMAT)
        file_handler.setFormatter(formatter)

        self.error_logger.addHandler(file_handler)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        
        self.error_logger.addHandler(console_handler)

    def get_blob_client(self, file_name):
        blob_connection_string = self.blob_description.connection_string
        container_name = self.blob_description.container_name
        project_path = self.blob_description.project_blob_path

        return BlobClient.from_connection_string(blob_connection_string, 
            container_name=container_name, blob_name=os.path.join(project_path, file_name), retry_total=0)

    def upload_logs_to_blob_storage(self, logs_file_name):
        try:
            penultimate_slash_index = logs_file_name.rindex('/') - self.DIRECTORY_NAME_LENGTH
            blob_client = self.get_blob_client(logs_file_name[penultimate_slash_index:])
        
            index = -1
            if 'debug' in logs_file_name:
                index = logs_file_name.find('debug')
            else: 
                index = logs_file_name.find('error')	

            if index < 0:
                print('Warning: {} file to logs not found'.format(logs_file_name))
            else:
                with open(logs_file_name[index:], "rb") as logs:
                    blob_client.upload_blob(logs, overwrite=True)
        except Exception as ex:
            print('An error has occurred uploading logs:', ex)
            self.__init__(self.logger_name, self.blob_description)

    def debug(self, message):
        self.debug_logger.debug(message)

        logs_file_name = self.get_debug_logs_name()
        self.upload_logs_to_blob_storage(logs_file_name)

    def error(self, message, exception):
        self.error_logger.error((message + ': {}').format(exception))

        logs_file_name = self.get_error_logs_name()
        self.upload_logs_to_blob_storage(logs_file_name)
