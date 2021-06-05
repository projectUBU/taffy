from django.contrib import admin
from chat.models import Handler, Message
# Register your models here.
# admin.site.register(Message)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver',
                    'message', 'timestamp', 'is_read')
    list_display_links = ('id', 'sender')
    list_filter = ('sender', 'receiver', 'is_read')
    list_per_page = 50


admin.site.register(Message, MessageAdmin)

class HandlerAdmin(admin.ModelAdmin):
    list_display = ('id', 'member', 'rejected_m', 'reviewe_value')
    list_display_links = ('id', 'member',)
    list_filter = ('rejected_m', 'member', )
    search_fields = ('member__username','rejected_m__username','reviewe_value')
    list_per_page = 50


admin.site.register(Handler, HandlerAdmin)