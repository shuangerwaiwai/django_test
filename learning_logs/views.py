# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    #学习笔记的主页
    return render(request, 'learning_logs/index.html')

def topics(request):
    #show all themes
    topics = Topic.objects.order_by('data_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    #show single theme and all the tips
    topic = Topic.objects.get(id = topic_id)
    entries = topic.entry_set.order_by('-data_added')
    context = {'topic':topic, 'entries':entries}
    return render(request, 'learning_logs/topic.html', context)

def new_topic(request):
    # add new theme
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

def new_entry(request, topic_id):
    #add new tips for one topic
    topic = Topic.objects.get(id = topic_id)
    if request.method!='POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))

    context = {'topic':topic, 'form':form}
    return render(request, 'learning_logs/new_entry.html', context)

def edit_entry(request, entry_id):
    #edit entry
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic

    if request.method != 'POST':
        #first request, use current entry
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)