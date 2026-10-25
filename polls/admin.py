from django.contrib import admin

from .models import Poll, PollOption, Vote


class PollOptionInline(admin.TabularInline):
    model = PollOption
    extra = 0
    min_num = 2
    max_num = 5


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ("question", "author", "created_at", "is_published")
    list_filter = ("is_published", "created_at")
    search_fields = ("question", "author__username")
    readonly_fields = ("id", "created_at")
    inlines = (PollOptionInline,)


@admin.register(PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    list_display = ("text", "poll", "position")
    list_select_related = ("poll",)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("poll", "option", "user", "guest_id", "created_at")
    list_filter = ("created_at",)
    readonly_fields = ("poll", "option", "user", "guest_id", "created_at")
    list_select_related = ("poll", "option", "user")

    def has_add_permission(self, request):
        return False
