from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def upload(params):
    """
    module string
    """

    # Set variables provided by Ansible task
    connection_string = params.get("connection_string")
    container_name = params.get("container_name")
    blob_name = params.get("blob_name")
    src = params.get("src")

    # Create a BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Create a ContainerClient object
    container_client = blob_service_client.get_container_client(container_name)

    # Set the name of your file and its path
    file_name =  blob_name
    file_path = src

    # Create a BlobClient object for your file
    blob_client = container_client.get_blob_client(file_name)

    # Upload your file to Blob Storage
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)
    
    return "FILE HAS BEEN UPLOADED"

if __name__ == "__main__":
    params= {"connection_string": ,
             "container_name": ,
             "blob_name": ,
             "src": }
    test= upload(params)
    print(test)
