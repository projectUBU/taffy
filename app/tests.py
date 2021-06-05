from django.test import TestCase
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import Avg, Max, Min
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView,  View
)



class MatchTest(View):
    template_name = 'app/match_test.html'
    models_class = Match
    models_profile_class = Profile
    models_rating_class = Rating
    success_url = '/match-test/'

    def render(self, request ,*args, **kwargs):
        return render(request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
        self.members = self.models_profile_class.objects.all()
        
        self.rating = self.models_rating_class.objects.filter(member_owner__member__id=self.request.user.id).order_by('-ratingPoint')
        # print(self.rating)
        self.context = {"ratings": self.rating}
        return self.render(request)

    def post(self, request, *args, **kwargs):
        get_owner = get_object_or_404(self.models_profile_class,id=request.user.id)
        return redirect(self.success_url)
        # get_profile = get_object_or_404(self.models_profile_class,pk=pk)
        # rating_point = get_object_or_404(self.models_rating_class,member_excluded__id=pk)



class LikeTest(View):
    models_class = Match
    models_profile_class = Profile
    models_rating_class = Rating
    success_url = '/match-test/'
    

    def get(self, request, pk,*args, **kwargs):
        get_owner = get_object_or_404(self.models_profile_class,id=request.user.id)
        get_profile = get_object_or_404(self.models_profile_class,pk=pk)
        rating_point = get_object_or_404(self.models_rating_class,member_excluded__id=pk)

       
        print({f'____{get_owner}____{get_profile}____{rating_point.ratingPoint}'})
        
        
        '''
        Match call profile field id (matcher_owner=profile_id)
        '''

        # try:
        #     match = self.models_class.objects.create(matcher_owner__id=request.user.id,matcher_excluded__id=get_profile.id,rating=rating_point)
        #     print(match)
        # except:
        #     match = self.models_class.objects.create(matcher_owner__id=request.user.id,matcher_excluded__id=get_profile.id,rating=rating_point)
        #     # pass


        return redirect(self.success_url)
    
    def post(self, request,pk, *args, **kwargs):
        try:
            get_owner = get_object_or_404(self.models_profile_class,id=request.user.id)
            get_profile = get_object_or_404(self.models_profile_class,pk=pk)
            rating_point = request.POST.get('point')
            print(get_owner,get_profile,rating_point)
            self.models_class(matcher_owner=get_owner,matcher_excluded=get_profile,rating=rating_point).save()
            oo=self.models_rating_class.objects.filter(member_excluded__member_id=pk)
            oo.delete()
            print(oo)
            return redirect(self.success_url)
            
        except:
            print("ERROR")
            return redirect(self.success_url)
        
        

class NopeTest(View):
    models_class = NoMatch
    models_profile_class = Profile
    success_url = '/match-test/'
    

    def get(self, request, pk,*args, **kwargs):
        get_profile = get_object_or_404(self.models_profile_class,pk=pk)
        # tt = self.models_class.objects.create(member_owner=request.user,member_excluded=member_excluded__member.id)
        print(get_profile)
        
        return redirect(self.success_url)
        
    def post(self, request,pk, *args, **kwargs):
        get_owner = get_object_or_404(self.models_profile_class,id=request.user.id)
        get_profile = get_object_or_404(self.models_profile_class,pk=pk)
        print(get_owner,get_profile)
        return redirect(self.success_url)



def tests(request):
    if 'min_age' in request.GET:
        filter_age1 = request.GET.get('min_age')
        filter_age2 = request.GET.get('max_age')
        rating = request.GET.get('rating')
        gender = request.GET.get('gender')
        anode = request.GET.get('anode')
        cathode = request.GET.get('cathode')

        if gender is None:
            gender = "M"
        if filter_age1 == "":
            filter_age1 = 0
        if filter_age2 == '':
            filter_age2 = Profile.objects.all().aggregate(Max('age'))[
                'age__max']

        if anode is None and cathode is not None:
            cathode = -1
            ages = Rating.objects.filter(
                member_excluded__age__range=(filter_age1, filter_age2)) & Rating.objects.filter(member_excluded__member__gender=gender) & Rating.objects.filter(ratingPoint__lte=cathode).order_by("ratingPoint")
            print(f'__________{anode}________/{cathode}_______')

        elif anode is not None and cathode is None:
            anode = 1
            ages = Rating.objects.filter(
                member_excluded__age__range=(filter_age1, filter_age2)) & Rating.objects.filter(member_excluded__member__gender=gender) & Rating.objects.filter(ratingPoint__gte=anode).order_by("-ratingPoint")
            print(f'__________{anode}________/{cathode}_______')
        else:
            ages = Rating.objects.filter(
                member_excluded__age__range=(filter_age1, filter_age2)).order_by("-ratingPoint") & Rating.objects.filter(member_excluded__member__gender=gender)
    
        
        # print(f'_________________{ages}________________')
        context = {"ages": ages}
        return render(request, 'members/test.html', context)
    profile = Rating.objects.filter(member_owner_id=request.user.id).order_by("-ratingPoint")
    print(profile)
    
    print(f'__________{profile}________')
    context = {"profile": profile}
    return render(request, 'members/test.html', context)


# class Conversation(LoginRequiredMixin, View):
#     initial = {'key': 'value'}
#     template_name = 'members/conversation.html'

#     def __init__(self,  *args, **kwargs):
#         self.models_class = Profile
#         self.models_class_scorebloodtype = ScoreBloodType
#         self.models_class_scoredayofweek = ScoreDaysOfWeek
#         self.models_class_scorenaksus = ScoreNakSus
#         self.models_class_scorerasi = ScoreRaSi
#         self.models_class_match = Match
#         self.form_class = MatchForm

#     @ login_required
#     def message(request, username):
#         currentProfile = request.user.profile
#         otherProfile = User.objects.get(username=username).profile

#         qr = Message.objects \
#             .raw('SELECT id, sender_id, text, sentDate \
#                 FROM taffy_message \
#                 WHERE sender_id = {0} AND recipient_id = {1} \
#                 UNION \
#                 SELECT id, sender_id, text, sentDate \
#                 FROM taffy_message \
#                 WHERE sender_id = {1} AND recipient_id = {0} \
#                 ORDER BY sentDate'.format(currentProfile.id, otherProfile.id))

#         messages = [(Profile.objects.get(id=m.sender_id), m.text) for m in qr]

#         if request.method == 'POST':
#             form = MessageForm(request.POST)
#             if form.is_valid():
#                 message = Message(
#                     sender=currentProfile, recipient=otherProfile, text=form.cleaned_data['text'])
#                 message.save()
#                 return redirect(request.path)
#         else:
#             form = MessageForm()

#         return render(request, 'taffy/message.html', {'messages': messages, 'form': form})
#     pass