from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import urlencode
from random import randint

from . import util


def index(request):
    return render(
        request, "encyclopedia/index.html", {"entries": util.list_entries()}
    )


def page(request, title):
    entry = util.convert_to_html(util.get_entry(title))
    if not entry:
        return redirect(error)

    return render(
        request,
        "encyclopedia/page.html",
        {
            "entry": entry,
            "title": title.capitalize(),
        },
    )


def error(request):
    code = request.GET.get("code", "not_found")
    goto = request.GET.get("goto", "")
    return render(
        request,
        "encyclopedia/error.html",
        {"code": code, "goto": goto.capitalize()},
    )


def search(request):
    query = request.GET.get("q", "")
    entries = util.list_entries()

    if any(query.lower() == entry.lower() for entry in entries):
        return redirect(page, query)

    results = list(
        entry for entry in entries if query.lower() in entry.lower()
    )
    return render(request, "encyclopedia/search.html", {"entries": results})


def new_page(request):
    context = {
        "pageName": "New Page",
        "type": "text",
        "initialTitle": "",
        "initialContent": "",
        "action": "save",
    }
    return render(request, "encyclopedia/form.html", context)


def edit_page(request, title):
    title = title
    content = util.get_entry(title)
    context = {
        "pageName": "Edit Page",
        "type": "hidden",
        "initialTitle": title,
        "initialContent": content,
        "action": "save-edit",
    }
    return render(request, "encyclopedia/form.html", context)


def save(request):
    title = request.POST.get("title", "No Title")
    content = request.POST.get("content", "No Content")
    if util.get_entry(title):
        params = urlencode({"code": "exists", "goto": title})
        url = reverse(error)
        return redirect(f"{url}?{params}")
    util.save_entry(title, content)
    return redirect(page, title)


def save_edit(request):
    title = request.POST.get("title", "No Title")
    content = request.POST.get("content", "No Content")
    util.save_entry(title, content)
    return redirect(page, title)


def random_page(request):
    entries = util.list_entries()
    randomEntry = randint(0, len(entries) - 1)
    return redirect(page, entries[randomEntry])
