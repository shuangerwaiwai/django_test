# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import  HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout

# Create your views he
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))