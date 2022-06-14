from django.db.models.signals import post_delete
from .models import QuestionImage, StateIcon
from django.dispatch import receiver


@receiver(post_delete, sender=QuestionImage, dispatch_uid='questionimage_deleted_signal')
def delete_questionimage_from_filesystem_if_present(sender, instance, using, **kwargs):
    print("Signal to delete Question image was received")
    # Delete image from folder on machine
    try:
        instance.path.delete(save=False)
    except:
        print(f"Something went wrong when deleting the QuestionImage image file at: {instance.path.name}")
        
    
    
    
@receiver(post_delete, sender=StateIcon, dispatch_uid='stateicon_deleted_signal')
def delete_stateicon_from_filesystem_if_present(sender, instance, using, **kwargs):
    print("Signal to delete StateIcon was received")
    # Delete image from folder on machine
    try:
        instance.path.delete(save=False)
    except: 
        print(f"Something went wrong when deleting the StateIcon image file at: {instance.path.name}")
    