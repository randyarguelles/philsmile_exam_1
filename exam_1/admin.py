from django.contrib import admin

# Register your models here.
from .models import Choice, Question, Quiz


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3
    readonly_fields = ('link',)

    def link(self, obj):
        return '<a href="/admin/exam_1/question/%s/"\
         target="_blank">Edit</a>' % obj.id

    link.allow_tags = True


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['quiz', 'question_text']}),
        # ('Date Information',
        #     {'fields': ['quiz'], 'classes':['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_filter = ['question_text']
    search_fields = ['question_text']
    list_display = ('question_text',)


class QuizAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['quiz_title']}),
        ('Date Information',
            {'fields': ['created_date'], 'classes':['collapse']}),
    ]
    inlines = [QuestionInline]
    list_filter = ['created_date']
    search_fields = ['quiz_title']
    list_display = ('quiz_title', 'created_date')

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
