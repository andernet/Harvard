from django.contrib.auth.models import AbstractUser
from django.db import models

class Listing(models.Model):
	title = models.CharField(max_length=64)
	description = models.TextField()
	dateTime = models.DateTimeField(auto_now_add=True)  # default widget form: DateTimeInput
	start_bid = models.DecimalField(max_digits=10, decimal_places=2)  # default widget form: NumberInput when localize is False
	current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	image = models.URLField()  # validate by URLValidator. Widget form: URLInput
	category = models.ForeignKey("Category", on_delete=models.CASCADE, blank=True, null=True, related_name="listings_by_category", default="")
	user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="listings_by_user")
	watchListings = models.ManyToManyField("WatchList", related_name="listings") 
	active = models.BooleanField(default="True")
    
	class Meta:
		ordering = ['title']

	def __str__(self):
		return f"{self.title}"

class WatchList(models.Model):
	pass

class User(AbstractUser):
    watch_list = models.ForeignKey(WatchList, related_name="watch_list", on_delete=models.CASCADE, blank=True, null=True)


class Category(models.Model):
	name = models.CharField(max_length=32)

	class Meta:
		ordering = ['name'] 
	def __str__(self):
		return f"{self.name}"

class Bid(models.Model):
	value = models.DecimalField(max_digits=10, decimal_places=2)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid", blank=True, null=True, default="")
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid")

	def __str__(self):
		return f"{self.listing.title} , {self.user.username} , {self.value}"

	class Meta:
		ordering = ['value']

class Comment(models.Model):
	text = models.TextField()
	dateTime = models.DateTimeField(auto_now_add=True)
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commentsByListing")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentsByUser")

	def __str__(self):
		return f"{self.listing.title} , {self.user.username} , {self.dateTime}"