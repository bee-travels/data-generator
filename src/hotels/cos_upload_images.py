import json
import uuid
import ibm_boto3

from ibm_botocore.client import Config
from ibm_botocore.exceptions import ClientError


# Constants for IBM cos values
# Current list avaiable at https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
COS_API_KEY_ID = "COS_API_KEY_ID"
# eg "W00YiRnLW4a3fTjMB-odB-2ySfTrFBIQQWanc--P3byk"
COS_RESOURCE_CRN = "COS_RESOURCE_CRN"
COS_AUTH_ENDPOINT = "COS_AUTH_ENDPOINT"
# eg "crn:v1:bluemix:public:cloud-object-storage:global:a/3bf0d9003abfb5d29761c3e97696b71c:d6f04d83-6c4f-4a62-a165-696756d63903::"
COS_ENDPOINT = "COS_ENDPOINT"

def load_config():
    with open('config.json') as json_data:
        return json.load(json_data)

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
    print("Creating bucket: {0}".format(bucket_name))
    try:
        cos.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                "LocationConstraint": "us-standard"
            }
        )
    except ClientError as be:
        print("Client ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to delete item: {0}".format(e))


def delete_item(bucket_name, item_name):
    print("Deleting item: {0}".format(item_name))
    try:
        cos.Object(bucket_name, item_name).delete()
        print("Item: {0} deleted!".format(item_name))
    except ClientError as be:
        print("Client ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to delete item: {0}".format(e))

def create_file(bucket_name, file_path, file_name):
    file = open(file_path, 'rb')
    print("Creating new item: {0}".format(file_name))
    try:
        cos.Object(bucket_name, file_name).put(
            # ACL="public-read",
            Body=file.read()
        )
    except ClientError as be:
        print("Client ERROR: {0}\n".format(be))
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
        print("Client ERROR: {0}\n".format(be))
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
        print("Client ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))

def get_item(bucket_name, item_name):
    print("Retrieving item from bucket: {0}, key: {1}".format(bucket_name, item_name))
    try:
        cos.Object(bucket_name, item_name).download_file("download-"+item_name)
    except ClientError as be:
        print("Client ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve file contents: {0}".format(e))

def delete_bucket(bucket_name):
    print("Deleting bucket: {0}".format(bucket_name))
    try:
        cos.delete_bucket(
            Bucket=bucket_name
        )
    except ClientError as be:
        print("Client ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to delete bucket: {0}".format(e))


def log_error(msg):
    print("UNKNOWN ERROR: {0}\n".format(msg))

def get_uuid():
    return str(uuid.uuid4().hex)

def main():
    try:
        bucket_name = "mofi-bee-travels-hotels"


        create_bucket(bucket_name)

        # create_file(bucket_name,
        #             "./card.png",
        #             "card.png")

        # get_url(bucket_name, "card.png")
        # delete_bucket(bucket_name)

        # get_item(bucket_name, "card.png")

        # for filename in os.listdir(os.getcwd()+"/hotel-images"):
        #     print(filename)

        # with open(os.getcwd()+"/hotel-images/55e9d54b4a5bb108f5d08460962b347d173cdbe24e50744e762f72d2944ec5_1280.jpg") as file:
        #     create_file(bucket_name, "image.jpg", file)


        # # create a new bucket
        # create_bucket(new_bucket_name)
        #
        # # get the list of buckets
        # print(get_buckets())

        # create a new text file
        # create_text_file(new_bucket_name, new_text_file_name, new_text_file_contents)

        # get the list of buckets
        # buckets = get_buckets()
        # for bucket in buckets:
        #     delete_bucket(bucket)


        # multi_part_upload()

        # # get the list of files from the new bucket
        # get_bucket_contents(new_bucket_name)
        #
        # # get the text file contents
        # get_item(new_bucket_name, new_text_file_name)


    except Exception as e:
        log_error("Main Program Error: {0}".format(e))

if __name__ == "__main__":
    main()