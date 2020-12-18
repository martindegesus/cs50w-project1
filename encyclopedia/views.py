from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
import markdown2

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':15}),label="Description")

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title in util.list_entries():
            raise forms.ValidationError("That entry already exists")
        return title

class NewQueryForm(forms.Form):
    query = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

searchform = NewQueryForm()

def search(request):
    if request.method == "GET":
        form = NewQueryForm(request.GET)
        form.is_valid()
        query=form.cleaned_data["query"].lower()
        entries = util.list_entries()
        resultslist = []
        for entry in entries:
            if query in entry.lower():
                resultslist.append(entry)
        print(resultslist)
        if resultslist:
            if len(resultslist)==1 and resultslist[0].lower() == query:
                return HttpResponseRedirect("/"+resultslist[0])
            else:
                return render(request, "encyclopedia/index.html",{
                    "searchform": searchform,
                    "heading": "Search Results",
                    "entries": resultslist,
                    "random": util.random_entry()
                })
        else:
            return render(request, "encyclopedia/search.html",{
                "searchform": searchform,
                "error": "There are no results for the given query",
                "random": util.random_entry()
            })
    return render(request, "encyclopedia/index.html",{
        "searchform": searchform,
        "error": "There are no results for the given query",
        "random": util.random_entry()
    })

def index(request):
    return render(request, "encyclopedia/index.html", {
        "heading": "All Pages",
        "searchform": searchform,
        "entries": util.list_entries(),
        "random": util.random_entry()
    })

def title(request, title):
    return render(request, "encyclopedia/title.html",{
        "searchform": searchform,
        "title":title,
        "entry": markdown2.markdown(util.get_entry(title)),
        "random": util.random_entry()
    })

def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            util.save_entry(title, description)
            return HttpResponseRedirect("/"+title)
        else:
            return render(request, "encyclopedia/create.html", {
                "searchform": searchform,
                "form": form
            })
    return render(request, "encyclopedia/create.html", {
        "searchform": searchform,
        "form": NewEntryForm(),
        "entries": util.list_entries(),
        "random": util.random_entry()
    })


def edit(request,title):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        form.is_valid()
        description = form.cleaned_data["description"]
        util.save_entry(title, description)
        return render(request, "encyclopedia/title.html",{
            "searchform": searchform,
            "title":title,
            "entry": markdown2.markdown(util.get_entry(title)),
            "random": util.random_entry()
        })
    util.get_content(title)
    form= NewEntryForm(initial={
            "searchform": searchform,
            'title': title,
            'description':util.get_content(title)
            })
    print(form['description'])
    form.fields['title'].disabled = True
    return render(request, "encyclopedia/edit.html", {
        "searchform": searchform,
        "entries": util.list_entries(),
        "random": util.random_entry(),
        "title":title,
        "form": form
    })