from google.cloud import storage
storage_client = storage.Client()

bucket_name = "my-new-bucket-s56"

bucket = storage_client.get_bucket('studyhub-data')

blob = bucket.get_blob('folder/Tree 0.pdf')
bucket.create()
print(blob)