from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse

from . import util


def index(request):
	if request.GET.get('q') is not None:
		a_entry = util.get_entry(request.GET.get('q'))
		if a_entry is not None:
			return HttpResponse(entry(request, request.GET.get('q')))
		else:
			entries = util.get_entries(request.GET.get('q'))
			return render(request, "encyclopedia/index.html", {
				"entries": entries,
				"h1": "Search Result",
			})
	else:
	    return render(request, "encyclopedia/index.html", {
	        "entries": util.list_entries(),
	        "h1": "All Pages"
    })

def new_entry(request):
	if request.method == "POST":
		form = NewEntryForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data["title"]
			content = form.cleaned_data["content"]
			if util.get_entry(title) is None:
				util.save_entry(title, content)
				return entry(request, title)
			else:
				return render(request, "encyclopedia/error.html", {
					"msg": f"Entry {title} already exist"
				})
		else:
			return render(request, "encyclopedia/new_entry", {
				"form": form
			})
	else:
		return render(request, "encyclopedia/new_entry.html", {
			"form": NewEntryForm()
		})

def entry(request, title):
	content = util.get_entry(title)
	if content is not None:
		return render(request, "encyclopedia/entry.html", {
			"title": title,
			"content": util.mark2html(content)
		})
	else:
		return render(request, "encyclopedia/error.html", {
			"msg": f"Entry {title} Not Found"
		})

def edit(request):
	if request.method == "POST":
		title = request.POST.get('title')
		content = request.POST.get('content')
		util.save_entry(title, content)
		return entry(request, title)
	else:
		title = request.GET.get('title')
		content = util.get_entry(title)
		return render(request, "encyclopedia/edit.html", {
			"title": title,
			"content": content,
		})

def random_entry(request):
	title = util.get_random()
	return entry(request, title)

def error(request):
	return HttpResponse("Entry No Found")

class NewEntryForm(forms.Form):
	title = forms.CharField(label="Type the Title ")
	content = forms.CharField(widget=forms.Textarea(attrs={'cols': '60', 'rows': '15'}), label="Type the Content ")