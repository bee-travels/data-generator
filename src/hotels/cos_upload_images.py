import json
import uuid
import ibm_boto3
from ibm_botocore.client import Config
from ibm_botocore.exceptions import ClientError


# Constants for IBM COS values
# Current list avaiable at https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
COS_API_KEY_ID = "COS_API_KEY_ID"
# eg "W00YiRnLW4a3fTjMB-odB-2ySfTrFBIQQWanc--P3byk"
COS_RESOURCE_CRN = "COS_RESOURCE_CRN"
COS_AUTH_ENDPOINT = "COS_AUTH_ENDPOINT"
# eg "crn:v1:bluemix:public:cloud-object-storage:global:a/3bf0d9003abfb5d29761c3e97696b71c:d6f04d83-6c4f-4a62-a165-696756d63903::"
COS_ENDPOINT = "COS_ENDPOINT"

def load_config():
    with open('config.json') as json_data:
        data = json.load(json_data)
    return data

data = load_config()

# Create resource
cos = ibm_boto3.resource("s3",
                         ibm_api_key_id=data[COS_API_KEY_ID],
                         ibm_service_instance_id=data[COS_RESOURCE_CRN],
                         ibm_auth_endpoint=data[COS_AUTH_ENDPOINT],
                         config=Config(signature_version="oauth"),
                         endpoint_url=data[COS_ENDPOINT]
                         )




def create_bucket(bucket_name):
    COS_BUCKET_LOCATION = "us-standard"
    print("Creating new bucket: {0}".format(bucket_name))
    try:
        cos.Bucket(bucket_name).create(
            CreateBucketConfiguration={
                "LocationConstraint": COS_BUCKET_LOCATION
            }
        )
        print("Bucket: {0} created!".format(bucket_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to create bucket: {0}".format(e))

def delete_item(bucket_name, item_name):
    print("Deleting item: {0}".format(item_name))
    try:
        cos.Object(bucket_name, item_name).delete()
        print("Item: {0} deleted!".format(item_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to delete item: {0}".format(e))

def create_text_file(bucket_name, item_name, file_text):
    print("Creating new item: {0}".format(item_name))
    try:
        cos.Object(bucket_name, item_name).put(
            Body=file_text, ACL="public-read"
        )
        print("Item: {0} created!".format(item_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to create text file: {0}".format(e))

def get_url(bucket_name, item_name):
    return data[COS_ENDPOINT]+"/"+bucket_name+"/"+item_name

def get_buckets():
    print("Retrieving list of buckets")
    try:
        buckets = cos.buckets.all()
        bucket_list = []
        for bucket in buckets:
            bucket_list.append(bucket.name)
        return bucket_list
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve list buckets: {0}".format(e))

def get_bucket_contents(bucket_name):
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        files = cos.Bucket(bucket_name).objects.all()
        file_list = []
        for file in files:
            file_list.append(file.key)
        return file_list
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))

def get_item(bucket_name, item_name):
    print("Retrieving item from bucket: {0}, key: {1}".format(bucket_name, item_name))
    try:
        file = cos.Object(bucket_name, item_name).get()
        print(file)
        print("File Contents: {0}".format(file["Body"].read()))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve file contents: {0}".format(e))

def delete_bucket(bucket_name):
    print("Deleting bucket: {0}".format(bucket_name))
    try:
        files = get_bucket_contents(bucket_name)
        for file in files:
            delete_item(bucket_name, file)
        cos.Bucket(bucket_name).delete()
        print("Bucket: {0} deleted!".format(bucket_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to delete bucket: {0}".format(e))

def multi_part_upload(bucket_name, item_name, file_path):
    try:
        print("Starting file transfer for {0} to bucket: {1}\n".format(item_name, bucket_name))
        # set 5 MB chunks
        part_size = 1024 * 1024 * 5

        # set threadhold to 15 MB
        file_threshold = 1024 * 1024 * 15

        # set the transfer threshold and chunk size
        transfer_config = ibm_boto3.s3.transfer.TransferConfig(
            multipart_threshold=file_threshold,
            multipart_chunksize=part_size
        )

        # the upload_fileobj method will automatically execute a multi-part upload
        # in 5 MB chunks for all files over 15 MB
        with open(file_path, "rb") as file_data:
            cos.Object(bucket_name, item_name).upload_fileobj(
                Fileobj=file_data,
                Config=transfer_config,
                ACL="public-read"
            )

        print("Transfer for {0} Complete!\n".format(item_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to complete multi-part upload: {0}".format(e))

def log_error(msg):
    print("UNKNOWN ERROR: {0}\n".format(msg))

def get_uuid():
    return str(uuid.uuid4().hex)

def main():
    try:
        # new_bucket_name = "py.bucket." + get_uuid()
        # new_text_file_name = "py_file_" + get_uuid() + ".txt"
        # new_text_file_contents = "This is a test file from Python code sample!!!"
        #
        # # create a new bucket
        # create_bucket(new_bucket_name)
        #
        # # get the list of buckets
        # print(get_buckets())

        # create a new text file
        # create_text_file(new_bucket_name, new_text_file_name, new_text_file_contents)

        # get the list of buckets
        buckets = get_buckets()
        for bucket in buckets:
            delete_bucket(bucket)


        # # get the list of files from the new bucket
        # get_bucket_contents(new_bucket_name)
        #
        # # get the text file contents
        # get_item(new_bucket_name, new_text_file_name)


    except Exception as e:
        log_error("Main Program Error: {0}".format(e))

if __name__ == "__main__":
    main()