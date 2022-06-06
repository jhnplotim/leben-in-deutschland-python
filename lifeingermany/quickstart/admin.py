from django.contrib import admin
from quickstart.models import State, Question, Answer
from django.utils.html import format_html

# Register your models here.

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            html_string = f'<img src="{obj.image.url}" width="30" height="30" />'
            return format_html(html_string)
        else:
            image = '-'
            return image

    def answer_count(self, obj):
        return obj.answer_set.count()

    def correct_count(self, obj):
        return obj.answer_set.filter(is_correct=True).count()
        

    image_tag.short_description = 'Image'

    answer_count.short_description = 'Answers'

    correct_count.short_description = 'Correct Answers'

    list_display = ['text','image_tag', 'state', 'answer_count', 'correct_count']



@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    
    def name_code(self, obj):
        return f'{obj.name} ({obj.code})'

    def image_tag(self, obj):
        html_string = f'<img src="{obj.icon.url}" width="30" height="30" />'
        return format_html(html_string)

    def question_count(self, obj):
        return obj.question_set.count()

    image_tag.short_description = 'Icon'

    name_code.short_description = 'Name (Code)'

    question_count.short_description = 'Questions'

    list_display = ['name_code','image_tag', 'question_count', 'added']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'is_correct', 'question']
