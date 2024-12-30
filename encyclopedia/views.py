import random

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util


#
# Form Classes
#

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
    create_title = forms.CharField(
        label = "Title",
        widget = forms.TextInput(attrs = {
            "class": "search",
            "placeholder": "Entry title",
        })
    )

    create_content = forms.CharField(
        label = "Content",
        widget = forms.Textarea(attrs = {
            "class": "search",
            "placeholder": "Entry content",
        })
    )

class NewEditForm(forms.Form):
    edit_content = forms.CharField(
        label = "Edit Content",
        widget = forms.Textarea(attrs = {
            "class": "search"
        })
    )

def search_form(request):
    form = NewSearchForm(request.POST)

    if form.is_valid():
        query = form.cleaned_data["q"]
    
        # Get entries and convert all items to lowercase
        entries = util.list_entries()
        entires_lower_case = []
    
        for entry in entries:
            entires_lower_case.append(entry.lower())
    
        if query in entires_lower_case:
            return HttpResponseRedirect(f"wiki/{query}")
        else:
            return HttpResponseRedirect(f"results/{query}")
    
    return None

#
# Views Fucntions
#

# HOME page
def index(request):
    # Search form
    if request.method == "POST":
        response = search_form(request)
        if response:
            return response

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
    # Search form
    if request.method == "POST":
        response = search_form(request)
        if response:
            return response
    
    if util.get_entry(entry) == None:
        return render(request, "encyclopedia/error.html", {
            "title": entry,
            "entry": entry,
            "form": NewSearchForm()
        })
    else:
        return render(request, "wiki/index.html", {
            "title": entry,
            "entry": util.get_entry(entry),
            "form": NewSearchForm()
        })

# Get search results.
def results(request, query):
    # Search form
    if request.method == "POST":
        response = search_form(request)
        if response:
            return response
        
    query_lower = query.lower()

    # Get entries and convert all items to lowercase
    entries = util.list_entries()
    entires_lower_case = []

    for entry in entries:
        entires_lower_case.append(entry.lower())

    # Check if query is included in list item, if yes add this item to a new list
    entries_matches = []

    for index, entry in enumerate(entires_lower_case):
        if query_lower in entry:
            entries_matches.append(entries[index])

    return render(request, "results/index.html", {
        "title": query,
        "matches": entries_matches,
        "form": NewSearchForm()
    })

# Redirect from link from results
def reResults(request, query):
    return HttpResponseRedirect(f"/wiki/{query}")

# New Entry
def new_entry(request):
    # Search form
    if request.method == "POST" and "q" in request.POST:
        response = search_form(request)
        if response:
            return response
    
    # Create form
    if request.method == "POST" and "create_title" in request.POST:
        form = NewCreateForm(request.POST)

        if form.is_valid():
            entry_title = form.cleaned_data["create_title"]
            entry_content = form.cleaned_data["create_content"]

            # Check if title already exists
            entries = util.list_entries()

            # Variable that will change to 1 if entry already exists
            entry_exists = 0

            for entry in entries:
                if entry.lower() == entry_title.lower():
                    entry_exists = 1
                    break
                    
            if not entry_exists:
                # Create a new md file using predefined function from util.py
                util.save_entry(entry_title, entry_content)

                # Redirect to a new created entry
                return HttpResponseRedirect(f"/wiki/{entry_title}")
            else:
                return render(request, "new-entry/index.html", {
                    "title": "Create a New Entry",
                    "create_form": NewCreateForm(),
                    "message": "Entry already exists!",
                    "form": NewSearchForm()
                })

    return render(request, "new-entry/index.html", {
        "title": "Create a New Entry",
        "create_form": NewCreateForm(),
        "form": NewSearchForm()
    })

# When no entry is provided in 'editEntry/ENTRY' url,
# redirect to the home page "index".
def edit(request):
    return HttpResponseRedirect(reverse("index"))

# Get entry from the urls path and pass it as "entry" variable
def edit_entry(request, entry):
    # Search form
    if request.method == "POST" and "q" in request.POST:
        response = search_form(request)
        if response:
            return response
    
    # Edit form
    if request.method == "POST" and "edit_content" in request.POST:
        form = NewEditForm(request.POST)

        if form.is_valid():
            entry_content = form.cleaned_data["edit_content"]
            # Save (overwrite) the the md file
            util.save_entry(entry, entry_content)
            # Redirect to the entry with new changes
            return HttpResponseRedirect(f"../wiki/{entry}")

    if util.get_entry(entry) == None:
        return render(request, "encyclopedia/error.html", {
            "title": entry,
            "entry": entry,
            "form": NewSearchForm()
        })
    else:
        # Get entry content
        entry_content = util.get_entry(entry)

        initial_data = {
            "edit_content": entry_content 
        }

        # Pass enrty content to the form as an input value
        form = NewEditForm(initial=initial_data)

        return render(request, "edit-entry/index.html", {
            "title": "Edit an Entry",
            "entry": entry,
            "edit_form": form,
            "form": NewSearchForm()
        })

# Redirect from link from wiki edit
def re_edit_entry(request, query):
    return HttpResponseRedirect(f"/edit-entry/{query}")

# Random entry
def random_entry_page(request):
    random_entry = random.choice(util.list_entries())

    return HttpResponseRedirect(f"wiki/{random_entry}")
