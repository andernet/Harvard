from django.contrib import admin
from .models import User, Bid, Listing, Comment, Category, WatchList

# Register your models here.

admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(WatchList)