from flask import Flask
import boto3

s3 = boto3.resource('s3')

DEBUG = True
PORT = 5000

app = Flask(__name__)

@app.route('/')
def index():
    return 'hi'

# for bucket in s3.buckets.all():
#     print(bucket.name)

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)