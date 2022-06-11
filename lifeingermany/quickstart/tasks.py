from quickstart.models import State, StateIcon, QuestionImage
from celery import shared_task
from enum import IntEnum

class ImageType(IntEnum):
    STATE_ICON = 0
    QUESTION_IMAGE = 1

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def count_states():
    return State.objects.count()


@shared_task
def rename_state_with_code(state_code, name):
    s = State.objects.get(code=state_code)
    s.name = name
    s.save()
   
@shared_task 
def download_image(url, imageTypeValue):
    print(imageTypeValue)
    print(url)
    try:
        decodedImageType = ImageType(imageTypeValue)
        print(decodedImageType)
    except:
        print("Image Type passed could not be decoded")
        decodedImageType = None
    
    if isinstance(decodedImageType, ImageType):
        import requests
        from PIL import Image
        from io import BytesIO
        from django.core.files import File
        
        response = requests.get(url)
        print(f'Request: {response!r}')
    
        if response.status_code == 200:
            content = response.content
            bytes = BytesIO(content)
            try:
                image = Image.open(bytes)
                if image:
                    print("Received an image")
                    image.save(bytes, format='PNG')
                    bytes.seek(0)
                    file_name = url.split("/")[-1]
                    
                    imageToSave = StateIcon()
                    if decodedImageType == ImageType.STATE_ICON:
                        imageToSave = StateIcon()
                    else:
                        imageToSave = QuestionImage()
                    
                    print("Received an image 2")
                    imageToSave.path.save(file_name, File(bytes), save=False)
                    print("Received an image 3")
                    imageToSave.save()
                    print("Received an image 4")
                    return imageToSave.id
                else:
                    print("Did not receive an image")
                    return None
            except Exception as e:
                print("Exception was thrown")
                print(e)
                return None
        else:
            return None
    else:
        print("Invalid image type requested")
        return None