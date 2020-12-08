import re
import random

from markdown2 import markdown
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def get_entries(string):
    """
    Retrieves encyclopedia entries that match to the string
    """
    entries = list_entries()
    matched_entries = []
    for entry in entries:
        if string.lower() in entry.lower():
            matched_entries += [entry]
    return matched_entries

def get_random():
    """
    Retrieves a random encyclopedia entry
    """
    return random.choice(list_entries())

def mark2html(marktext):
    """
    Convert markdown text to html
    """
    return markdown(marktext)