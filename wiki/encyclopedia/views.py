from markdown2 import Markdown
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import secrets

from . import util

mark = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    
    page = util.get_entry(entry)
     
    if page is None:
        return render(request, "encyclopedia/error_page.html",{
            "tittle" : entry
        })
    else:
        return render (request, "encyclopedia/entry.html",{
        "entry": mark.convert(page),
        "tittle" : entry
        })


def search_entry(request):

    search = request.GET.get("q")
    search_clean =  search.strip()
    entries = util.list_entries()
    list_entries = []
    
    if util.get_entry(search_clean.upper()) is None:

        for entry in entries:

            if search_clean.upper() in entry.upper():
                list_entries.append(entry)
            
        
        return render (request, "encyclopedia/index.html",{
        "entries" : list_entries
        })
    else: 
        return HttpResponseRedirect(reverse( "encyclopedia:entry",
        kwargs = {'entry' : search_clean} ) ) 


class newEntry(forms.Form):

    entry = forms.CharField(label="Tittle", widget=forms.TextInput(attrs={'class':"form-control mb-2 col-md-3"}))
    textarea = forms.CharField( label="Description", widget=forms.Textarea (attrs={'class': "form-control mb-2 col-md-9 sm-7" }))
    edited  = forms.BooleanField(initial=False, required=False, widget=forms.HiddenInput())
    

def new_entry(request):

    if request.method == "POST":
        
        form = newEntry(request.POST)

        if form.is_valid():

            entry = form.cleaned_data["entry"]
            info = form.cleaned_data["textarea"]
            edit = form.cleaned_data["edited"]

            # if entry not exist, create a new entry
            if util.get_entry(entry) is None or edit == True:

                util.save_entry(entry, info)

                return HttpResponseRedirect(reverse ("encyclopedia:entry", 
                kwargs={"entry" : entry}))

            else:
                exists = True
                
                return render (request, "encyclopedia/new_entry.html",{
                    "exist" : exists,
                    "tittle" : "This page already exists",
                    "entry" : entry,
                    "btn" :"OK"
                })

    return render (request, "encyclopedia/new_entry.html",{
        "form" : newEntry(request.POST),
        "btn" :"Save"
    })


def edit(request, entry):
    
    textarea = util.get_entry(entry)
    entry
     
    form  = newEntry()
    form.fields["entry"].initial = entry 
    form.fields["entry"].widget = forms.HiddenInput()
    form.fields["textarea"].initial = textarea
    form.fields["edited"].initial = True

    return render (request, "encyclopedia/new_entry.html",{
        "form": form,
        "tittle" : "Editing    " + entry,
        "textarea" : textarea,
        "btn" : "Done",
        "edited" : form.fields["edited"].initial

    })

def random (request):
    lista = util.list_entries()
    random_items = secrets.choice(lista)

    return HttpResponseRedirect(reverse ("encyclopedia:entry",
    kwargs={"entry" :random_items }))

    

     

        
        


        
    