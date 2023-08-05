class BlobDescription:

    def __init__(self, connection_string, container_name, project_blob_path, project_local_path):
        self.connection_string = connection_string
        self.container_name = container_name
        self.project_blob_path = project_blob_path
        self.project_local_path = project_local_path
