from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models.expressions import Expression
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from rest_framework.parsers import JSONParser
from chat.models import Handler, Message
from chat.serializers import  MessageSerializer, UserSerializer
from app.models import Match, Member, Profile
from django.contrib.auth.decorators import login_required

def index(request):
    if request.user.is_authenticated:
        return redirect('chats')
    if request.method == 'GET':
        return render(request, 'chat/index.html', {})
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
        else:
            return HttpResponse('{"error": "User does not exist"}')
        return redirect('chats')


@csrf_exempt 
def user_list(request, pk=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        u = []

        if pk:
            u = Member.objects.filter(id=pk)
            print(u)
        else:
            
            matcher = list(Match.objects.filter(matcher_owner=request.user.id).values_list('matcher_excluded__id', flat=True))
            find_qual =  list(Match.objects.filter(matcher_excluded=request.user.id).values_list('matcher_owner__id', flat=True))
            
            qual = [x for x in matcher if x  in  find_qual and  x  in matcher]
            not_equal=[x for x in matcher + find_qual if x not in matcher or x not in find_qual ]
            b = [x for x in qual + not_equal if x  in qual or x  in not_equal]
            print(qual,not_equal,b)
            for i in range(0, len(b)):
                user = Member.objects.get(id = b[i])
                u.append(user)
        
        
        serializer = UserSerializer(u, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            user = Match.objects.create_user(username=data['username'], password=data['password'])
            Member.objects.create(user=user)
            return JsonResponse(data, status=201)
        except Exception:
            return JsonResponse({'error': "Something went wrong"}, status=400)


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def register_view(request):
    """
    Render registration template
    """
    if request.user.is_authenticated:
        return redirect('chats')
    return render(request, 'chat/register.html', {})

@login_required
def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        users = []
        p=list(Match.objects.filter(matcher_owner=request.user.id).values_list('matcher_excluded_id', flat=True))
        for i in range(len(p)):
            users.append(Profile.objects.get(member__id = p[i]))
        print(users)
        p = Profile.objects.filter(id=request.user.id)
        
        return render(request, 'chat/chat.html',{'users':users,'profile':p})

@login_required
def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, "chat/messages.html",
                      {'users': Match.objects.filter(matcher_owner__username=request.user.username),
                       'receiver':  Member.objects.get(id=receiver),
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=sender)})

@login_required
def review_view(request,pk):
    try:
        score = Match.objects.get(matcher_owner__id=request.user.id,matcher_excluded__id=pk)
        obj = Profile.objects.get(member__id=pk)
        context ={
        'object': obj,
        'score':score,
        }
    except:
        texts = "คุณยังไม่ได้กด LIKE ยังรีวิวไม่ได้และปฏิเสทไม่ได้"
        obj = Profile.objects.get(member__id=pk)
        
        context ={
            'object': obj,
            'text':texts
        }
    return render(request, 'chat/rejected.html', context)

@login_required
def rate_view(request):
    if request.method == 'POST':
        m = request.user.id
        mx_id = request.POST.get('mx_id')
        print(m,mx_id)
        owner = get_object_or_404(Member,id=m)
        rejecter = get_object_or_404(Member,id=mx_id)
        val = request.POST.get('val')

        try:
            k = Handler(member=owner,rejected_m=rejecter,reviewe_value=val)
            k.save()
            get_score = Profile.objects.filter(member__id=mx_id).first()
            result = list(Handler.objects.filter(rejected_m__id=mx_id).values_list('reviewe_value', flat=True))
            new_s = (get_score.profile_score + sum(result)*len(result))/(len(result))
            print(result,new_s)
            score_new_profile = Profile.objects.filter(member__id=mx_id).update(profile_score=new_s)
         
        except:
            Handler.objects.filter(member__id=m ,rejected_m__id=mx_id).update(reviewe_value=val)
           
        return JsonResponse({'success':'true', 'score': val}, safe=False)
    return JsonResponse({'success':'false'})





class RejectedView(LoginRequiredMixin,View):
    models_class = Match
    models_member_class = Member
    models_profile_class = Profile
    success_url = '/'
   
    
    def post(self, request,pk, *args, **kwargs):
 

        get_owner = get_object_or_404(self.models_member_class,id=request.user.id)
        get_member = get_object_or_404(self.models_member_class,pk=pk)
        self.models_class.objects.filter(matcher_owner__id=get_owner.id,matcher_excluded__id=pk).delete()
        self.models_class.objects.filter(matcher_owner__id=pk,matcher_excluded__id=get_owner.id).delete()
        return redirect(self.success_url)
            
      
        