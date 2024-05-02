from fastapi import HTTPException, status
from models.models import User as UserModel
from services.gcstorage import GCStorageService
from db_config.connection import settings
from PIL import Image
import io
import uuid

BUCKET_URL = settings.BUCKET_URL
BUCKET_NAME = settings.BUCKET_NAME


class FilesService():

    def __init__(self):
        pass

    async def delete_file(self, db, username, filename):
        user = db.query(UserModel).filter(
            UserModel.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User does not exits")

        result = await GCStorageService().delete_file_from_bucket(
            filename=filename, bucket_name=BUCKET_NAME)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Cloud Storage not available")

        return

    async def upload_file(self, db, username, file):
        user = db.query(UserModel).filter(
            UserModel.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User does not exits")

        unique_id = uuid.uuid4()
        filename = f"image_{unique_id}.webp"
        result = False

        content = await file.read()
        image = Image.open(io.BytesIO(content))
        image = image.convert('RGB')

        max_width = 1920
        max_height = 1080

        if image.width > max_width or image.height > max_height:
            width_ratio = max_width / image.width
            height_ratio = max_height / image.height
            resize_ratio = min(width_ratio, height_ratio)

            new_width = int(image.width * resize_ratio)
            new_height = int(image.height * resize_ratio)

            image = image.resize((new_width, new_height))

        with io.BytesIO() as output:
            image.save(output, format='WebP', quality=80)
            output.seek(0)
            result = await GCStorageService().upload_file_to_bucket(
                filename=filename, file=output, bucket_name=BUCKET_NAME)

        url = f'{BUCKET_URL}/{filename}'

        if not result:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Cloud Storage not available")

        return url
