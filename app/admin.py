from django.contrib import admin
from .models import *
from datetime import date
from django.contrib import auth

admin.site.site_header = "Taffy Dating Admin."
# admin.site.unregister(auth.models.Group)



class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name',
                    'last_name', 'birthday', 'gender', 'testes', 'description', 'is_staff', 'is_active','profile_image')
    list_display_links = ('id', )
    list_filter = ('username', 'birthday', 'testes',
                   'gender', 'is_staff', 'is_active')
    list_editable = ( 'birthday', 'gender', 'testes', 'is_staff', 'is_active','profile_image')
    search_fields = ('testes','username')
    list_per_page = 20


admin.site.register(Member, MemberAdmin)


class ScoreBloodTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'bloodtypeA', 'bloodtypeB', 'scorebloodtype')
    list_display_links = ('id', 'scorebloodtype')
    list_filter = ('bloodtypeA', 'bloodtypeB',)
    list_per_page = 40


admin.site.register(ScoreBloodType, ScoreBloodTypeAdmin)


class ScoreDaysOfWeekAdmin(admin.ModelAdmin):
    list_display = ('id', 'daysofweekA', 'daysofweekB', 'scoredaysofweek')
    list_display_links = ('id', 'scoredaysofweek')
    list_filter = ('daysofweekA', 'daysofweekB',)
    list_per_page = 50


admin.site.register(ScoreDaysOfWeek, ScoreDaysOfWeekAdmin)
# admin.site.register(ScoreDaysOfWeek)


class ScoreNakSusAdmin(admin.ModelAdmin):
    list_display = ('id', 'naksusA', 'naksusB', 'scorenaksus')
    list_display_links = ('id', 'scorenaksus')
    list_filter = ('naksusA', 'naksusB',)
    list_per_page = 150


admin.site.register(ScoreNakSus, ScoreNakSusAdmin)


class ScoreRaSiAdmin(admin.ModelAdmin):
    list_display = ('id', 'rasiA', 'rasiB', 'scorerasi')
    list_display_links = ('id', 'scorerasi')
    list_filter = ('rasiA', 'rasiB',)
    list_per_page = 150


admin.site.register(ScoreRaSi, ScoreRaSiAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'member', 'age', 'daysofweek',
                    'rasi', 'bloodtype', 'naksus', 'profile_score',)
    list_display_links = ('id', 'member')
    list_filter = ('member', 'age', 'bloodtype', 'naksus', 'daysofweek')
    list_editable = ( 'age', 'daysofweek',
                    'rasi', 'bloodtype', 'naksus', 'profile_score','profile_score',)
    search_fields = ('age','member__username',)
    list_per_page = 50


admin.site.register(Profile, ProfileAdmin)


class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'matcher_owner', 'matcher_excluded', 'rating')
    list_display_links = ('id', 'matcher_owner')
    list_filter = ('matcher_owner', 'matcher_excluded', 'rating')
    list_per_page = 50


admin.site.register(Match, MatchAdmin)


class NoMatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'nomatcher_owner', 'nomatcher_excluded', 'rating')
    list_display_links = ('id', 'nomatcher_owner')
    list_filter = ('nomatcher_owner', 'nomatcher_excluded', 'rating')
    list_per_page = 50


admin.site.register(NoMatch, NoMatchAdmin)


class BloodTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'bloodtype')
    list_display_links = ('id',)
    list_per_page = 50


admin.site.register(BloodType, BloodTypeAdmin)


class DaysOfWeekAdmin(admin.ModelAdmin):
    list_display = ('id', 'daysofweek')
    list_display_links = ('id',)
    list_per_page = 50


admin.site.register(DaysOfWeek, DaysOfWeekAdmin)


class NakSusAdmin(admin.ModelAdmin):
    list_display = ('id', 'naksus')
    list_display_links = ('id',)
    list_per_page = 50


admin.site.register(NakSus, NakSusAdmin)


class RaSiAdmin(admin.ModelAdmin):
    list_display = ('id', 'rasi')
    list_display_links = ('id',)
    list_per_page = 50


admin.site.register(RaSi, RaSiAdmin)


class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'member_owner', 'member_excluded', 'ratingPoint')
    list_display_links = ('id', 'member_owner',)
    list_filter = ('member_owner', 'member_excluded', 'member_owner__age','member_excluded__age','ratingPoint')
    search_fields = ('member_owner__member__username','member_excluded__age','ratingPoint')
    list_per_page = 50


admin.site.register(Rating, RatingAdmin)



