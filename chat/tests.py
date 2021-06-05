from django.test import TestCase
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import Avg, Max, Min
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView,  View
)

class Test(View):
    template_name = 'chat/test2.html'


    def get(self, request,*args, **kwargs):
        return render(request, self.template_name)