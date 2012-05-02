from polls.models import Poll, Choice
from django.contrib import admin


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'deadline', 'status')
    inlines = [ChoiceInline]

admin.site.register(Poll, PollAdmin)


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('poll', 'choice', 'votes', 'percentage')

admin.site.register(Choice, ChoiceAdmin)
