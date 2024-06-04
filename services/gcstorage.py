from google.cloud import storage


class GCStorageService():

    def __init__(self):
        pass

    async def upload_file_to_bucket(self, filename: str, file,
                                    bucket_name: str):
        storage_client = storage.Client()

        try:
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob(filename)
            blob.upload_from_file(file)
            blob.make_public()
            return True
        except Exception as e:
            print(e)
            return False

    async def delete_file_from_bucket(self, filename: str, bucket_name: str):
        storage_client = storage.Client()
        try:
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob(filename)
            blob.delete()
            return True
        except Exception as e:
            print(e)
            return False
        pass
