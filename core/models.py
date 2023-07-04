from django.db import models

# Create your models here.
class GeneralUser(models.Model):
    email = models.CharField(max_length=255)
    def __str__(self):
        return self.email


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    min_bid_price = models.FloatField()
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    auction_end_datetime = models.DateTimeField(null=True)
    created_by = models.ForeignKey(GeneralUser, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

class Bid(models.Model):
    item = models.ForeignKey(Item, related_name='bids', on_delete=models.CASCADE)
    bid_by = models.ForeignKey(GeneralUser, related_name='bids', on_delete=models.CASCADE)
    bid_amount = models.FloatField()
