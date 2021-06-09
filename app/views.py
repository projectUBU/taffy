from re import M
from typing import ContextManager
from django import views
from django.http import request
from django.http.response import HttpResponseRedirect
from app.models import *
from chat.models import Handler
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User, AnonymousUser
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView
from django.contrib.auth.hashers import make_password
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView
)
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views import View
from django.db.models import Avg, Max, Min

def wellcome(request):
    return render(request, 'app/wellcome.html')


def logout_views(req):
    auth_logout(req)
    return redirect('/login/')


class LoginView(View):
    models_class = Member
    form_class = MemberLoginForm
    initial = {'key': 'value'}
    template_name = 'app/wellcome.html'

    def render(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('member_all')
        self.form = self.form_class(initial=self.initial)
        self.context = {'form': self.form}
        return self.render(request)

    def post(self, request, *args, **kwargs):
        next = self.request.GET.get('next')
        self.form = self.form_class(request.POST)
        self.username = request.POST.get('username', '')
        self.password = request.POST.get('password', '')
        self.user = authenticate(username=self.username, password=self.password)
        # if request.method == 'POST':
        if self.request.user.is_authenticated:
            return redirect('member_all')
        if self.user is not None:

            if self.user.is_active:
                auth_login(request, self.user)
                messages.success(request, "You have logged in!")
                if next == None:
                    return HttpResponseRedirect('/')
                return redirect(self.request.GET.get('next'))

            else:
                messages.warning(request, "Your account is disabled!")
                return redirect('/login/')
        else:
            messages.warning(
                request, "Warning!The username or password are not valid!")
            # return redirect('/login/')
        self.context ={'form':self.form}
        return self.render(request)


class RegisterView(View):
    # pass
    models_class = Member
    form_class = MemberRegisterForm
    initial = {'key': 'value'}
    template_name = 'app/register.html'

    def render(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('member_all')

        self.form = self.form_class(initial=self.initial)
        print(self.form)
        self.context = {'form': self.form}
        return self.render(request)

    def post(self, request, *args, **kwargs):
        self.form = self.form_class(request.POST, request.FILES,)
        if self.request.user.is_authenticated:
            return redirect('member_all')

        if self.form.is_valid():
            
            self.form.save()
            self.profile_image = self.form.cleaned_data.get('profile_image')
            self.username = self.form.cleaned_data.get('username')
            messages.success(
                request, f'Your account:{self.username} has been created! Your ar now able to login.')
            return redirect('login')
        else:
            self.form = self.form_class(initial=self.initial)
            print(self.form)
        self.context = {'form': self.form}
        return self.render(request)

class ProfileView(LoginRequiredMixin,View):
    success_url = '/profile/'
    template_name = 'app/profile.html'
    models_class = Profile
    models_member_class = Member
    initial = {'key': 'value'}
    form_class = MemberProfileUpdateForm

    def redirect(self, request, *args, **kwargs):
        return redirect(self.success_url)

    
    def render(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

   
   
    def get(self, request, *args, **kwargs):
       
        self.member = self.models_class.objects.filter(id=self.request.user.id)
        self.form = self.form_class(instance=self.request.user)
        # print(self.form)
        self.context = {'form': self.form,'member':self.member}
        return self.render(request)

    def post(self, request, *args, **kwargs):
        
        self.form = self.form_class(self.request.POST,self.request.FILES,instance=self.request.user)
        if self.form.is_valid():
            self.form.save()
            messages.success(request, "Your account has been updated!")
            return self.redirect(request)
        else:
            self.form = self.form_class(instance=self.request.user)
        context = {'form':self.form}
        return self.render(request)

class SettingsUpdateView(LoginRequiredMixin,View):
    template_name = 'app/setting.html'
    success_url = '/setting/'
    form_class = MemberSettingUpdateForm
    delete_form_class = AccountDeleteForm
    models_profile_class =Profile

    def redirect(self, request, *args, **kwargs):
        return redirect(self.success_url)

    
    def render(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

   
    def get(self, request, *args, **kwargs):
       
        self.member = self.models_profile_class.objects.filter(id=self.request.user.id)
        self.form = self.form_class(instance=self.request.user)
        # print(self.form)
        self.context = {'form': self.form,'member':self.member}
        return self.render(request)

    def post(self, request, *args, **kwargs):
        
        self.delete_form =self.delete_form_class(request.POST, instance=request.user)
        self.form = self.form_class(self.request.POST,self.request.FILES,instance=self.request.user)
        if self.form.is_valid():
            self.form.save()
            messages.success(request, "Setting updated!")
            return self.redirect(request)
        elif self.delete_form.is_valid():
            self.user = self.request.user
            self.user.delete()
            messages.info(request, 'Your account has been deleted.')
            return redirect('login')
        else:
            self.form = self.MemberSettingUpdateForm(instance=request.user)
            self.delete_form = AccountDeleteForm(instance=request.user)

        context = {'form':self.form,'delete_form': self.delete_form}
        return self.render(request)


class GetRatingView(LoginRequiredMixin, View):
    models_class = Profile
    member_class_handle = Handler
    models_class_member = Member
    models_class_bloodtype = BloodType
    models_class_dayofweek = DaysOfWeek
    models_class_naksus = NakSus
    models_class_rasi = RaSi
    models_class_scorebloodtype = ScoreBloodType
    models_class_scoredayofweek = ScoreDaysOfWeek
    models_class_scorenaksus = ScoreNakSus
    models_class_scorerasi = ScoreRaSi
    models_class_match = Match
    models_class_nomatch = NoMatch
    models_class_rating = Rating
    form_class = MatchForm
    initial = {'key': 'value'}
    template_name = 'app/member_all.html'
    
   
    
    def get(self, request, * args, **kwargs):
        
      

        bloodtype = self.models_class_bloodtype.objects.all()
        daysofweek = self.models_class_dayofweek.objects.all()
        naksus = self.models_class_naksus.objects.all()
        rasi = self.models_class_rasi.objects.all()

        scorebloodtype = self.models_class_scorebloodtype.objects.all()
        scoredaysofweek = self.models_class_scoredayofweek.objects.all()
        scorenaksus = self.models_class_scorenaksus.objects.all()
        scorerasi = self.models_class_scorerasi.objects.all()
        
        
        matcher_excluded = self.models_class_match.objects.exclude(matcher_excluded__id=request.user.id)

        
        
        lenbloodtype = int(len(bloodtype))
        lendaysofweek = int(len(daysofweek))
        lennaksus = int(len(naksus))
        lenrasi = int(len(rasi))

        lenscorebloodtype = int(len(scorebloodtype))
        lenscoredaysofweek = int(len(scoredaysofweek))
        lenscorenaksus = int(len(scorenaksus))
        lenscorerasi = int(len(scorerasi))


        bloodtypelist = []
        daysofweeklist = []
        naksuslist = []
        rasilist = []
        allMember = []
        allrating = []

        bloodtypewhile = 0

        while bloodtypewhile <= lenscorebloodtype:
            k = lenbloodtype + bloodtypewhile
            # print("k: ",k)
            if k <= lenscorebloodtype:
                bloodtypelist.append([scorebloodtype[j].scorebloodtype for j in range(
                    bloodtypewhile, k)])
            bloodtypewhile += lenbloodtype
            

        daysofweekwhile = 0
        while daysofweekwhile <= lenscoredaysofweek:
            k = lendaysofweek + daysofweekwhile
            if k <= lenscoredaysofweek:
                daysofweeklist.append([scoredaysofweek[j].scoredaysofweek for j in range(
                    daysofweekwhile, k)])

            daysofweekwhile += lendaysofweek

        naksuswhile = 0
        while naksuswhile <= lenscorenaksus:
            k = lennaksus + naksuswhile
            if k <= lenscorenaksus:
                naksuslist.append([scorenaksus[j].scorenaksus for j in range(
                    naksuswhile, k)])

            naksuswhile += lennaksus

        rasiwhile = 0
        while rasiwhile <= lenscorerasi:
            k = lenrasi + rasiwhile
            if k <= lenscorerasi:
                rasilist.append([scorerasi[j].scorerasi for j in range(
                    rasiwhile, k)])

            rasiwhile += lenrasi
        # print(matcher_excluded)
  
        
        own_id =[]
        member_ex_id = []
        match_id = []
        rating_id = []

        own = list(self.models_class.objects.filter(id=request.user.id))
        member_excluded = self.models_class.objects.exclude(id=request.user.id)

        own_id = list(self.models_class.objects.filter(member__id=request.user.id).values_list('member__id', flat=True))
        member_excluded_id = sorted(list(self.models_class.objects.exclude(member__id=request.user.id).values_list('member__id', flat=True)))
        nomatch_id = sorted(list(self.models_class_nomatch.objects.filter(nomatcher_owner=request.user.id).values_list('nomatcher_excluded_id', flat=True)))
        match_id = sorted(list(self.models_class_match.objects.filter(matcher_owner=request.user.id).values_list('matcher_excluded_id', flat=True)))
        rating = self.models_class_rating.objects.filter(member_owner=request.user.id)


        # print(lll.index(42))

        equal = [x for x in match_id + nomatch_id + member_excluded_id  if x  in match_id and x not in nomatch_id and x not in member_excluded_id]
        
        
        not_equal=[x for x in match_id + nomatch_id + member_excluded_id if x not in match_id and x not in nomatch_id or x not in member_excluded_id]
        print(not_equal)
        

        for i in range(len(not_equal)):
            
            owner_class=self.models_class.objects.get(member__id=request.user.id)
            member_class=self.models_class.objects.get(member__id=not_equal[i])
            print(member_class)
            if own_id[0] != member_class.member.id and owner_class.member.testes == member_class.member.gender and owner_class.member.gender ==  member_class.member.testes :
                # print(f'_______{member_class}______')
                rating_score =  (rasilist[owner_class.rasi.id-1][member_class.rasi.id-1] + bloodtypelist[owner_class.bloodtype.id-1][member_class.bloodtype.id-1] +
                                daysofweeklist[owner_class.daysofweek.id-1][member_class.daysofweek.id -
                                                                    1] + naksuslist[owner_class.naksus.id-1][member_class.naksus.id-1])*member_class.profile_score
               
                member_excluded_id = member_class.member.id
                try:
                
                  
                    Rating(member_owner=owner_class, member_excluded=member_class,
                                    ratingPoint=rating_score).save()
                   
                    
                    
                except :
            
                    # print("____________________________")
                    
                    
                    old = self.models_class_rating.objects.filter(member_owner_id=request.user.id).order_by("-ratingPoint")
                    rating_all_get = self.models_class_rating.objects.filter(member_owner_id=request.user.id,member_excluded__member__testes=request.user.gender,member_excluded__member__gender=request.user.testes).order_by("-ratingPoint")
                    # print(f'_____rating all is {rating_all_get}')

                    for i in range(len(old)):
                        if old[i]  in rating_all_get:
                            self.models_class_rating.objects.filter(member_excluded_id=member_class.member.id).update(ratingPoint=rating_score)
                            # print(f'__________{old[i].member_excluded.member.username}____')
                            
                        else:
                            print(old[i].member_excluded.member.username)
                            excluded_id = old[i].id
                 
            
            # else:
            #     old = self.models_class_rating.objects.filter(member_owner_id=request.user.id).order_by("-ratingPoint")
            #     print(f'__________{old}___________')       

     
       
        rating_alls = self.models_class_rating.objects.filter(member_owner_id=request.user.id,member_excluded__member__testes=request.user.gender,member_excluded__member__gender=request.user.testes).order_by("-ratingPoint")
        print(f'_____{len(rating_alls)}________')
        age_min = self.models_class.objects.all().aggregate(Min('age'))['age__min']
        age_max = self.models_class.objects.all().aggregate(Max('age'))['age__max']
        
        page = request.GET.get('page', 1)
        paginator = Paginator(rating_alls, 1)
        try:
            rating_all = paginator.page(page)
        except PageNotAnInteger:
            rating_all = paginator.page(1)
        except EmptyPage:
            rating_all = paginator.page(paginator.num_pages)
        
        if 'min_age' in request.GET:
            filter_age1 = request.GET.get('min_age')
            filter_age2 = request.GET.get('max_age')
            anode = request.GET.get('anode')
            cathode = request.GET.get('cathode')
            
            
            if filter_age1 == "":
                filter_age1 = self.models_class.objects.all().aggregate(Min('age'))[
                    'age__min']
                print(filter_age1)
            if filter_age2 == '':
                filter_age2 = self.models_class.objects.all().aggregate(Max('age'))[
                    'age__max']

            if anode is None and cathode is not None:
                cathode = -1
                filter_ages = self.models_class_rating.objects.filter(
                    member_excluded__age__range=(filter_age1, filter_age2)) & self.models_class_rating.objects.filter(member_owner_id=request.user.id,member_excluded__member__testes=request.user.gender,member_excluded__member__gender=request.user.testes) & self.models_class_rating.objects.filter(ratingPoint__lte=cathode).order_by("ratingPoint")
                # print(f'__________{anode}________/{cathode}_______')

            elif anode is not None and cathode is None:
                anode = 1
                filter_ages = self.models_class_rating.objects.filter(
                    member_excluded__age__range=(filter_age1, filter_age2)) & self.models_class_rating.objects.filter(member_owner_id=request.user.id,member_excluded__member__testes=request.user.gender,member_excluded__member__gender=request.user.testes) & self.models_class_rating.objects.filter(ratingPoint__gte=anode).order_by("-ratingPoint")
                # print(f'__________{anode}________/{cathode}_______')
            else:
                filter_ages = self.models_class_rating.objects.filter(
                    member_excluded__age__range=(filter_age1, filter_age2)).order_by("-ratingPoint") & self.models_class_rating.objects.filter(member_owner_id=request.user.id,member_excluded__member__testes=request.user.gender,member_excluded__member__gender=request.user.testes)
    
            context = {
            "filter_ages": filter_ages,
            "filter_age1":filter_age1 ,
            "filter_age2":filter_age2 ,
            }
            return render(request, self.template_name, context)
            
        context = {  
            'rating_all': rating_all,
            'rating_alls':rating_alls,
            "age_min":age_min,
            "age_max":age_max,
    
        }

        return render(request, self.template_name, context)

class LikeView(LoginRequiredMixin,View):
    models_class = Match
    models_member_class = Member
    models_rating_class = Rating
    success_url = 'member_all'
    
    
    def post(self, request,pk, *args, **kwargs):
        try:
            get_owner = get_object_or_404(self.models_member_class,id=request.user.id)
            get_member = get_object_or_404(self.models_member_class,pk=pk)
            rating_point = request.POST.get('point')
            print(pk)
            self.models_class(matcher_owner=get_owner,matcher_excluded=get_member,rating=rating_point).save()
            self.models_rating_class.objects.filter(member_excluded__member_id=pk).delete()
            return redirect(self.success_url)
            
        except:
            print("ERROR")
            return redirect(self.success_url)
        
        

class NopeView(LoginRequiredMixin,View):
    models_class = NoMatch
    models_member_class = Member
    models_rating_class = Rating
    success_url = '/'
    
        
    def post(self, request,pk, *args, **kwargs):
        try:
            get_owner = get_object_or_404(self.models_member_class,id=request.user.id)
            get_member = get_object_or_404(self.models_member_class,pk=pk)
            rating_point = request.POST.get('point')
            print(get_owner,get_member,rating_point)
            self.models_class(nomatcher_owner=get_owner,nomatcher_excluded=get_member,rating=rating_point).save()
            self.models_rating_class.objects.filter(member_excluded__member_id=pk).delete()
            return redirect(self.success_url)
            
        except:
            print("ERROR")
            return redirect(self.success_url)




@login_required
def memberprofile(request, username):
    return render(request, 'app/memberprofile.html', {'user': User.objects.all().get(username=username)})


@login_required
def test_view(request):
    return render(request, 'app/test.html')


@login_required
def match(req):
    print(f'bornborn to match')
    return render(req, 'taffy/matchedtest.html')


@login_required
def rating(req):
    #  pass
    # คะแนนจาก ตารางที่หามาทำเป็น Matrix ลิงก์ จำลอง Data
    # https://colab.research.google.com/drive/1Rnk7lSw1qkbOmp79J9w3yDdXtOe94Op7?usp=sharing

    pass