from django.contrib import admin
from quickstart.models import State, Question, Answer, QuestionImage, StateIcon
from django.utils.html import format_html

# Register your models here.

class AnswerInline(admin.StackedInline):
    model = Answer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        if obj.image and hasattr(obj.image, 'data_base64_string'):
            html_string = f'<img src="data: image/png; base64, {obj.image.data_base64_string}" width="30" height="30" />'
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

    inlines = [AnswerInline]


class QuestionInline(admin.StackedInline):
    model = Question


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    
    def name_code(self, obj):
        return f'{obj.name} ({obj.code})'

    def image_tag(self, obj):
        html_string = f'<img src="data: image/png; base64, {obj.icon.data_base64_string}" width="30" height="30" />'
        return format_html(html_string)

    def question_count(self, obj):
        return obj.question_set.count()

    image_tag.short_description = 'Icon'

    name_code.short_description = 'Name (Code)'

    question_count.short_description = 'Questions'

    list_display = ['name_code','image_tag', 'question_count', 'added']

    inlines = [QuestionInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'is_correct', 'question']
    
@admin.register(StateIcon)
class StateIconAdmin(admin.ModelAdmin):
    def scheme_image_tag(self, obj):
        img = obj.data_base64_string
        html_string = f'<img src = "data: image/png; base64, {img}" width="30" height="30" />'
        return format_html(html_string)

    scheme_image_tag.short_description = 'Image'
    scheme_image_tag.allow_tags = True
    
    def img_name(self, obj):
        return obj.path.name
    
    img_name.short_description = 'Name'
    
    list_display = ['img_name', 'scheme_image_tag']
    
    
@admin.register(QuestionImage)
class QuestionImageAdmin(admin.ModelAdmin):
    def scheme_image_tag(self, obj):
        img = obj.data_base64_string
        html_string = f'<img src = "data: image/png; base64, {img}" width="30" height="30" />'
        return format_html(html_string)

    scheme_image_tag.short_description = 'Image'
    scheme_image_tag.allow_tags = True
    
    def img_name(self, obj):
        return obj.path.name
    
    img_name.short_description = 'Name'
    
    list_display = ['img_name', 'scheme_image_tag']
    
