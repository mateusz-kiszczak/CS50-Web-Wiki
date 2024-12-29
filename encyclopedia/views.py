import random

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util

# Create a form classes
class NewSearchForm(forms.Form):
    q = forms.CharField(
        label = "",
        required = False,
        widget = forms.TextInput(attrs = {
            "class": "search",
            "placeholder": "Search Encyclopedia",
        })
    )

class NewCreateForm(forms.Form):
    createTitle = forms.CharField(
        label = "Title",
        widget = forms.TextInput(attrs = {
            "class": "search",
            "placeholder": "Entry title",
        })
    )

    createContent = forms.CharField(
        label = "Content",
        widget = forms.Textarea(attrs = {
            "class": "search",
            "placeholder": "Entry content",
        })
    )

class NewEditForm(forms.Form):
    editContent = forms.CharField(
        label = "Edit Content",
        widget = forms.Textarea(attrs = {
            "class": "search"
        })
    )


def index(request):
    # Search form
    if request.method == "POST":
        form = NewSearchForm(request.POST)

        if form.is_valid():
            query = form.cleaned_data["q"]

            # Get entries and convert all items to lowercase
            entries = util.list_entries()
            entiresLowerCase = []

            for entry in entries:
                entiresLowerCase.append(entry.lower())

            if query in entiresLowerCase:
                return HttpResponseRedirect(f"wiki/{query}")
            else:
                return HttpResponseRedirect(f"results/{query}")

    # Random entry
    random_entry = random.choice(util.list_entries())

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm(),
        "random": random_entry
    })

# When no entry is provided in 'wiki/ENTRY' url,
# redirect to the home page "index".
def wiki(request):
    return HttpResponseRedirect(reverse("index"))

# Get entry from the urls path and pass it as "entry" variable
def entry(request, entry):   
    if util.get_entry(entry) == None:
        return render(request, "wiki/error.html", {
            "title": entry,
            "entry": entry
        })
    else:
        return render(request, "wiki/index.html", {
            "title": entry,
            "entry": util.get_entry(entry)
        })
    
def results(request, query):
    queryLower = query.lower()

    # Get entries and convert all items to lowercase
    entries = util.list_entries()
    entiresLowerCase = []

    for entry in entries:
        entiresLowerCase.append(entry.lower())

    # Check if query is included in list item, if yes add this item to a new list
    entriesMatches = []

    for index, entry in enumerate(entiresLowerCase):
        if queryLower in entry:
            entriesMatches.append(entries[index])

    return render(request, "results/index.html", {
        "title": query,
        "matches": entriesMatches
    })

# Redirect from link from results
def reResults(request, query):
    return HttpResponseRedirect(f"/wiki/{query}")

def newEntry(request):
    if request.method == "POST":
        form = NewCreateForm(request.POST)

        if form.is_valid():
            entryTitle = form.cleaned_data["createTitle"]
            entryContent = form.cleaned_data["createContent"]

            # Check if title already exists
            entries = util.list_entries()

            # Variable that will change to 1 if entry already exists
            entryExists = 0

            for entry in entries:
                if entry.lower() == entryTitle.lower():
                    entryExists = 1
                    break
                    
            if not entryExists:
                # Create a new md file using predefined function from util.py
                util.save_entry(entryTitle, entryContent)

                # Redirect to a new created entry
                return HttpResponseRedirect(f"/wiki/{entryTitle}")
            else:
                return render(request, "newEntry/index.html", {
                    "title": "Create a New Entry",
                    "createForm": NewCreateForm(),
                    "message": "Entry already exists!"
                })

    return render(request, "newEntry/index.html", {
        "title": "Create a New Entry",
        "createForm": NewCreateForm()
    })

# When no entry is provided in 'editEntry/ENTRY' url,
# redirect to the home page "index".
def edit(request):
    return HttpResponseRedirect(reverse("index"))

# Get entry from the urls path and pass it as "entry" variable
def editEntry(request, entry):
    if request.method == "POST":
        form = NewEditForm(request.POST)

        if form.is_valid():
            entry_content = form.cleaned_data["editContent"]
            # Save (overwrite) the the md file
            util.save_entry(entry, entry_content)
            # Redirect to the entry with new changes
            return HttpResponseRedirect(f"../wiki/{entry}")

    # Get entry content
    entry_content = util.get_entry(entry)

    initial_data = {
        "editContent": entry_content 
    }

    # Pass enrty content to the form as an input value
    form = NewEditForm(initial=initial_data)

    return render(request, "editEntry/index.html", {
        "title": "Edit an Entry",
        "entry": entry,
        "editForm": form
    })

# Redirect from link from wiki edit
def reEditEntry(request, query):
    return HttpResponseRedirect(f"/editEntry/{query}")



# USE GIT AND COMMIT BEFORE MAKE BELOW CHANGES !!!!!!!!!!!!!!

# find a way to make a working layout form in all html files
# alternativly REMOVE layout or search form from other pages
# BEST OPTION - create a separate apps for every functionality: wiki, results, new entry etc.

# Remove all folders from "templates" and put files directly to "encyclopedia"

# Check and manage dynamic titles and variable names (results)

# One "layout" for all html files

