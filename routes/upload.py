from fastapi import APIRouter, UploadFile, File, Depends, Request
from auth.authenticate import authenticate
from PIL import Image
import io
import uuid
import os

upload_router = APIRouter(prefix="/files", tags=["Files"])


@upload_router.post("/")
async def upload_file(request: Request,
                      file: UploadFile = File(...),
                      user: str = Depends(authenticate)):

    unique_id = uuid.uuid4()
    filename = f"image_{unique_id}.webp"

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
        image.save(output, format='WebP', quality=60)
        output.seek(0)
        optimized_image_bytes = output.read()

    directory = "files/"

    if not os.path.exists(directory):
        os.makedirs(directory)
    print(optimized_image_bytes)

    file_path = os.path.join(directory, filename)
    with open(file_path, "wb") as f:
        f.write(optimized_image_bytes)

    url = f"{request.url}" + f"{filename}"

    return {"url": url, "type": file.content_type}
