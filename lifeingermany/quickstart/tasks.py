from quickstart.models import State, StateIcon, QuestionImage, Question, Answer
from celery import shared_task
from enum import IntEnum

class ImageType(IntEnum):
    STATE_ICON = 0
    QUESTION_IMAGE = 1
    
class DownloadType(IntEnum):
    STATE = 0
    NO_STATE = 1


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
    try:
        decodedImageType = ImageType(imageTypeValue)
    except:
        print("Image Type passed could not be decoded")
        decodedImageType = None
    
    if url is not None and isinstance(decodedImageType, ImageType):
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
        print(f"Invalid image type ({imageTypeValue}) requested OR url ({url}) is None")
        return None
    
    
    
@shared_task
def download_page(downloadTypeValue, *args):
    try:
        decodedDownloadType = DownloadType(downloadTypeValue)
    except:
        print("Download Type passed could not be decoded")
        decodedDownloadType = None
        
    if isinstance(decodedDownloadType, DownloadType):
        if decodedDownloadType == DownloadType.STATE:
            if len(args) == 2:
                stateId = create_state_id(args[0], args[1])
                if stateId:
                    try:
                        state = State.objects.get(pk = stateId)
                    except Exception as e:
                        print(e)
                        return None
                
                else:
                    print("StateId returned is none")
                    return None
            else:
                print("State must have two arguments, name and id")
                return None
            
        else:
            # Download for non state questions
            stateId = None
            if len(args) != 1 or not isinstance(args[0], int):
                print(f"download could not be done for page with args: {args}")
                return None
            
        downloadUrl = f"https://www.lebenindeutschland.eu/fragenkatalog/{args[0]}"
        import requests
        from bs4 import BeautifulSoup
        data = requests.get(downloadUrl)
        
        if data.status_code == 200:
            # Download was successful
            print(f"Initial page download for page with id: {args[0]} was successful")
            
            soup = BeautifulSoup(data.text, "html.parser")
            qns_html = soup.select('div.p-4.bg-white.shadow')
            # Remove first element which is not a question div
            del qns_html[0]
            
            for qn_html in qns_html:
                try:
                    qn_text = qn_html.find_all("h3")[0]
                    qn_text = qn_text.string.replace("\n","").split(":")[-1].strip()
                    
                    qn_image = qn_html.find_all('img')
                    
                    if len(qn_image) == 1:
                        qn_image_url = f'https://www.lebenindeutschland.eu{qn_image[0]["src"]}'
                    else:
                        qn_image_url = None
                    
                    question_id = create_question_id(text=qn_text, imageUrl=qn_image_url, stateId = stateId)
                    try:
                        question = Question.objects.get(pk = question_id)
                    except Exception as e:
                        print("Could not create question, returning")
                        print(e)
                        return None
                    
                    answers_html = qn_html.find_all("span")
                    
                    for ans_html in answers_html:
                        ans_html = ans_html.string.replace("—","").replace("\n","")

                        if "✓" in ans_html:
                          is_correct = True
                        else:
                          is_correct = False
                        
                        ans_html = ans_html.replace("✓","").strip()
                        if ans_html:
                            answer = Answer()
                            answer.text = ans_html
                            answer.is_correct = is_correct
                            answer.question = question
                            answer.save()
                        
                except e as Exception:
                    print(e)
                    # If anything goes wrong (return)
                    print("Something went wrong when traversing questions")
                    return None
        else:
            # Something went wrong
            print(f"Initial page download for page with id: {args[0]} was NOT successful, returning...")
            return None
        
    else:
        print("Invalid Download type requested")
        return None
    
    
    
    # TODO: Wait a few seconds before returning
    return None

@shared_task
def create_state_id(stateId, stateName):
    from celery import chain
    from celery.result import allow_join_result
    iconUrl = f"https://www.lebenindeutschland.eu/img/states/{stateId}.png"
    iconSig = download_image.s(iconUrl, ImageType.STATE_ICON)
    # Chain the download of the icon with the creation of the state such that
    # the result of the download is used in the creation of the state and the stateId is returned or None
    with allow_join_result():
        return chain(iconSig | create_state.s(stateId, stateName))().get()

@shared_task
def create_state(iconId, id, name):
    if iconId and name:
        try:
            icon = StateIcon.objects.get(pk = iconId)
            if icon:
                state = State()
                state.icon = icon
                state.name = name
                state.code = id
                # Saving state
                state.save()
                # Returning state DB ID
                return state.id
            else:
                print(f"The icon with ID: {iconId} could not be found")
                return None
        except Exception as e:
            print(e)
            return None
    else:
        print(f"IconId OR State Name is None, for State with ID: {id} & Name: {name}")
        return None
    
@shared_task
def create_question_id(imageUrl, text, stateId):
    from celery import chain
    from celery.result import allow_join_result
    imageSig = download_image.s(imageUrl, ImageType.QUESTION_IMAGE)
    # Chain the download of the image with the creation of the Question such that
    # the result of the image download is used in the creation of the Question and the questionId is returned or None
    with allow_join_result():
        return chain(imageSig | create_question.s(text, stateId))().get()

@shared_task
def create_question(imageId, text, stateId):
    if text:
        
        # Try to retrieve question image if present
        try:
            image = QuestionImage.objects.get(pk = imageId)
        except Exception as e:
            print(e)
            image = None
          
        # Try to retrieve State if present  
        try:
            state = State.objects.get(pk = stateId)
        except Exception as e:
            print(e)
            state = None
        
        question = Question()
        question.image = image
        question.text = text
        question.state = state
        try:             
            # Saving Question
            question.save()
            # Returning Question DB ID
            return question.id
        except Exception as e:
            print(e)
            return None
    else:
        print(f"Question text with value {text} is corrupted")
        return None

@shared_task    
def populate_database():
    # Empty DB
    # Delete State Icons, will delete all States, their Questions and Answers
    StateIcon.objects.all().delete()
    
    # Delete remaining data i.e. QuestionImages, Questions and Answers that do not belong to states
    QuestionImage.objects.all().delete()
    Question.objects.all().delete()
    
    from celery import group
    from celery.result import allow_join_result
    with allow_join_result():
        gr = group(download_others.s(), download_states.s())
        return gr().get()
    
 
@shared_task    
def download_states():
    try:
        statesList = [
                  ("bw", "Baden-Württemberg"),
                  ("by", "Bayern"),
                  ("be", "Berlin"),
                  ("bb", "Brandenburg"),
                  ("hb", "Bremen"),
                  ("hh", "Hamburg"),
                  ("he", "Hessen"),
                  ("mv", "Mecklenburg-Vorpommern"),
                  ("ni", "Niedersachsen"),
                  ("nw", "Nordrhein-Westfalen"),
                  ("rp", "Rheinland-Pfalz"),
                  ("sl", "Saarland"),
                  ("sn", "Sachsen"),
                  ("st", "Sachsen-Anhalt"),
                  ("sh", "Schleswig-Holstein"),
                  ("th", "Thüringen"),
                  ]
        for statetuple in statesList:
            download_page(DownloadType.STATE, statetuple[0], statetuple[1])
            import time
            time.sleep(2)
            
        return True
            
    except Exception as e:
        print(e)
        return False
 
@shared_task    
def download_others():
    try:
        for pageId in range(1,11,1):
            download_page(DownloadType.NO_STATE, pageId)
            import time
            time.sleep(2)
            
        return True
    
    except Exception as e:
        print(e)
        return False
        