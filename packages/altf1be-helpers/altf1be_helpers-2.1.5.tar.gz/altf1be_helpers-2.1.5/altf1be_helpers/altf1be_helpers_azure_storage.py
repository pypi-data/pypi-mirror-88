# -*- coding: utf-8 -*-

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import logging
from pathlib import Path
from werkzeug.utils import secure_filename

logging.getLogger("urllib3").setLevel(logging.WARNING)
home_directory = str(Path.home())

class AltF1BeAzureStorage:
    """
        Create, Retrieve, Update Delete files using Azure Table Storage using Python v12 SDK

        See https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python

    """
    def __init__(self):
        pass
    
    def upload_file_stream(self, form):

        directoryClient = DirectoryClient(
            connection_string=os.environ["microsoft_azure_storage_connection_string"],
            container_name=os.environ["microsoft_azure_storage_container_name"],
        )
        
        print(f"file: {file}")
        file_filename = secure_filename(file.filename)
        dest = os.path.join(secure_filename(form.robots.data), form.cleaning_date.data.strftime(form.cleaning_date.format), file_filename)
        directoryClient.upload_file_stream(data=file, dest=dest)


if __name__ == "__main__":
