DOCUMENTATION = r'''
---
module: azure_blob
author:
    - Ryan Gorden (@ryan.gorden)
'''
EXAMPLES = r'''
# upload a file
- name: Add file to Azure Blob Storage
    azure_blob:
    connection_string: "{{ connection_string }}"
    container_name: "{{ container_name }}"
    blob_name: "{{ file_name }}"
    src: "{{ file_path }}"
'''

ANSIBLE_METADATA = {"metadata_version": "1.0", "status": ["stable"], "supported_by": "ryangorden"}

from ansible.errors import AnsibleError # pulled from ntc 
from ansible.module_utils.basic import AnsibleModule
import json
# from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

try:
    from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

    HAS_AZURE = True
except ImportError:
    HAS_AZURE= False

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

def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        connection_string=dict(type='str', required=True),
        container_name=dict(type='str', required=True),
        blob_name=dict(type='str', required=True),
        src=dict(type='str', required=True),
    )

    # Validate required extra libraries imported successfully
    if not HAS_AZURE:
        module.fail_json(msg="azure-storage-blob Python library not found.")

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )


    try:
        # in the event of a successful module execution, you will want to
        # simple AnsibleModule.exit_json(), passing the results from backup_config
        file_upload = upload(module.params)
        module.exit_json(config=file_upload, changed=True)
    except AnsibleError as e:
        raise AnsibleError(e)
    except Exception:

        # during the execution of the module, if there is an exception or a
        # conditional state that effectively causes a failure, run
        # AnsibleModule.fail_json() to pass in the message and the result
        # Validate required extra libraries imported successfully
        module.fail_json(msg="Error running upload()) azure_blob.py module: ")

if __name__ == "__main__":

    main()
