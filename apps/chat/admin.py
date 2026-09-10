from django.contrib import admin
from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('sender', 'content', 'created_at', 'is_read')


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('proposal', 'owner_confirmed_meeting', 'bidder_confirmed_meeting', 'meeting_confirmed_at', 'created_at')
    list_filter = ('owner_confirmed_meeting', 'bidder_confirmed_meeting')
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'created_at', 'is_read')
    search_fields = ('content', 'sender__username')
