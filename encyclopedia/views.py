import markdown

from django.core.files.storage import default_storage

from django import forms

from random import randint

from django.urls import reverse

from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import render

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, title):
    article = util.get_entry(title)
    html = markdown.markdown(article)
    return render(request, "encyclopedia/article.html", {
        "content": html,
        "title": title,
    })

def search(request):
    if request.method == 'POST':
        filename = f"entries/{request.POST['q']}.md"
        if default_storage.exists(filename):
            return HttpResponseRedirect(f"/wiki/{request.POST['q']}")
        else:
            names = util.list_entries()
            entries = [i for i in names if request.POST['q'] in i]
            return render(request, "encyclopedia/search.html", {
                "entries": entries
            })
    else:
        return HttpResponseRedirect(reverse("index"))

def random(request):
    entries = util.list_entries()
    title = entries[ randint(0, len(entries)-1) ]
    return HttpResponseRedirect(f"/wiki/{title}")

def add(request):
    if request.method == 'POST':
        title = request.POST['title'].strip()
        content = request.POST['content'].strip()
        filename = f"entries/{title}.md"
        if default_storage.exists(filename):
            return render(request, "encyclopedia/error.html", {
                "message": "Not saved - word exists"
            })
        else:
            util.add_entry(title, f"# {title}\n\n{content}")
            return HttpResponseRedirect(f"/wiki/{title}")
    else:
        return render(request, "encyclopedia/add.html")

def edit(request, title):
    article = util.get_entry(title)
    content = article.split("\n", 1)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content[1],
    })

def save(request):
    title = request.POST['title'].strip()
    content = request.POST['content'].strip()
    util.add_entry(title, f"# {title}\n\n{content}")
    return HttpResponseRedirect(f"/wiki/{title}")
