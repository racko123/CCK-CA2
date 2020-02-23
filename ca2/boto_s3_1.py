import boto3
import botocore
from time import sleep

# Create an S3 resource
s3 = boto3.resource('s3')

full_path = '/home/pi/Desktop/image1.jpg'
file_name = 'image1.jpg'

def takePhotoWithPiCam():
    from picamera import PiCamera
    camera = PiCamera()
    sleep(5)
    camera.capture(full_path)
    sleep(3)

# Set the filename and bucket name
bucket = 'sp-p1828894-s3-bucket' # replace with your own unique bucket name
exists = True

try:
    s3.meta.client.head_bucket(Bucket=bucket)
except botocore.exceptions.ClientError as e:
    error_code = int(e.response['Error']['Code'])
    if error_code == 404:
        exists = False

if exists == False:
  s3.create_bucket(Bucket=bucket,CreateBucketConfiguration={
    'LocationConstraint': 'us-east-1'})

# Take a photo
takePhotoWithPiCam()

# Upload a new file
s3.Object(bucket, file_name).put(Body=open(full_path, 'rb'))
print("File uploaded")
