# HSE S3 Bucket Utility library used by HSE administration for S3 bucket maintenance, region may be specified else default hosted (US-east-1)
# class methods include: create_bucket, list_buckets (within a region), list_objects (within a bucket), delete_bucket

import logging
import boto3
from botocore.exceptions import ClientError

class HSES3BucketUtility():
    
    # initialise class S3BucketUtility

    def __init__(self):
        return


    # HSE Admin can create a new S3 bucket for COVID19 test results as needed based upon patient volumes

    def create_bucket(bucket_name, region=None):
    # Create bucket, If a region is not specified, the bucket is created by default in region (us-east-1) as per AWS educate
        try:
            if region is None:
                # default region US-east-1
                s3_client = boto3.client('s3')
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                # use region specified as argument above
                s3_client = boto3.client('s3', region_name=region)
                location = {'LocationConstraint': region}
                s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
        except ClientError as e:
            logging.error(e)
            return False
        return True


    # HSE Admin can retrieve list of current S3 buckets used for COVID19 test results for their records, defaults to current region

    def list_buckets():
        # Retrieve the list of existing buckets
        s3_client = boto3.client('s3')
        response = s3_client.list_buckets()
        # Print out all buckets by name
        print('The existing HSE COVID19 test results administration buckets are:')
        for bucket in response['Buckets']:
            print('\t', bucket["Name"])


    # HSE Admin can list out existing COVID19 test results contained within an existing s3 bucket to determine whether to delete

    def list_objects(bucket_name, region=None):
        s3_client = boto3.client('s3')
        # get list of buckets
        response = s3_client.list_objects_v2(
            Bucket=bucket_name
        )
        print('The existing HSE COVID19 test results administration objects within this bucket are:')
        if response['KeyCount'] != 0:
            for content in response['Contents']:
                object_key = content['Key']
                print(object_key)

            
    # HSE Admin can delete an existing S3 bucket (used for COVID19 test results) as needed for patient test result administration

    def delete_bucket(region, bucket_name):
        # Delete a given S3 bucket
        s3_client = boto3.client('s3')
        # first delete all the objects from a bucket, if any objects exist
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if response['KeyCount'] != 0:
            for content in response['Contents']:
                object_key = content['Key']
                print('\t Deleting object...', object_key)
                s3_client.delete_object(Bucket=bucket_name, Key=object_key)
        # delete the bucket
        print('\t Deleting bucket...', bucket_name)
        response = s3_client.delete_bucket(Bucket=bucket_name)


# end of class S3BucketUtility