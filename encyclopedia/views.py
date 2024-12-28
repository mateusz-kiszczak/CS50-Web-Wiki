from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util

# Create a form class
class NewSearchForm(forms.Form):
    q = forms.CharField(
        label = "",
        required = False,
        widget = forms.TextInput(attrs = {
            "class": "search",
            "placeholder": "Search Encyclopedia",
        })
    )

def index(request):
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

        

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm()
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
    return render(request, "encyclopedia/newEntry.html", {
        "title": "Create a New Entry"
    })

# USE GIT AND COMMIT BEFORE MAKE BELOW CHANGES !!!!!!!!!!!!!!

# find a way to make a working layout form in all html files
# alternativly REMOVE layout or search form from other pages
# BEST OPTION - create a separate apps for every functionality: wiki, results, new entry etc.

# Remove all folders from "templates" and put files directly to "encyclopedia"

# Check and manage dynamic titles and variable names (results)

# One "layout" for all html files

