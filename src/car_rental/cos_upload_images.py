import json
import os
import uuid
import ibm_boto3

from ibm_botocore.client import Config
from ibm_botocore.exceptions import ClientError

# Constants for IBM cos values
# Current list available at https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
COS_API_KEY_ID = "COS_API_KEY_ID"
# eg "W00YiRnLW4a3fTjMB-odB-2ySfTrFBIQQWanc--P3byk"
COS_RESOURCE_CRN = "COS_RESOURCE_CRN"
COS_AUTH_ENDPOINT = "COS_AUTH_ENDPOINT"
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
    buckets = get_buckets()
    if bucket_name in buckets:
        print("bucket already exists")
        return
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
            ACL="public-read",
            Body=file.read()
        )
    except ClientError as be:
        print("Client ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to create text file: {0}".format(e))


def get_url(bucket_name, item_name):
    return data[COS_ENDPOINT] + "/" + bucket_name + "/" + item_name


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
    print("done!")

def get_item(bucket_name, item_name):
    print("Retrieving item from bucket: {0}, key: {1}".format(
        bucket_name, item_name))
    try:
        cos.Object(bucket_name, item_name).download_file(
            "download-" + item_name)
    except ClientError as be:
        print("Client ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve file contents: {0}".format(e))


def delete_bucket(bucket_name):
    print("Deleting bucket: {0}".format(bucket_name))
    try:
        items = get_bucket_contents(bucket_name)
        for item in items:
            delete_item(bucket_name, item)
        cos.Bucket(bucket_name).delete()
        return True
    except ClientError as be:
        print("Client ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to delete bucket: {0}".format(e))
    return False


def log_error(msg):
    print("UNKNOWN ERROR: {0}\n".format(msg))


def get_uuid():
    return str(uuid.uuid4().hex)


def get_all_file_path(folder_path):
    files = []
    for filename in os.listdir("./"+folder_path):
        files.append("./"+folder_path+"/"+filename)
    return files


def get_all_file(folder_path):
    return os.listdir("./" + folder_path)


def upload_all_files(bucket_name, folder_path):
    file_names = get_all_file(folder_path)
    file_paths = get_all_file_path(folder_path)

    for i in range(len(file_names)):
        create_file(bucket_name, file_paths[i], file_names[i])


def get_urls(bucket_name):
    files = get_bucket_contents(bucket_name)
    urls = []
    for file in files:
        urls.append(get_url(bucket_name, file))
    return urls


def write_array_to_file(arr, file_name):
    f = open(file_name, "w+")
    for line in arr:
        f.write("%s\n" % line)
    f.close()


def write_json_to_file(json_data, file_name):
    print("writing json to file")
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=True, indent=2)


def match_url_to_file(urls, folder_path):
    data = {}
    files = get_all_file(folder_path)
    for file in files:
        for url in urls:
            if file in url:
                data[file] = url
                break
    return data

def main():
    try:
        bucket_name = "bee-travels-cars"
        folder_name = "car-images"
        # delete_bucket(bucket_name)
        create_bucket(bucket_name)
        print(bucket_name)
        upload_all_files(bucket_name, folder_name)

        urls = get_urls(bucket_name)
        urls_json = match_url_to_file(urls, folder_name)
        # write_array_to_file(urls, "urls.txt")
        write_json_to_file(urls_json, "urls.json")
    except Exception as e:
        log_error("Main Program Error: {0}".format(e))


if __name__ == "__main__":
    main()
