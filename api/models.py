from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from api.utils import sendTransaction
import hashlib

class Post(models.Model):  #create a classic Post model for the blog
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default=None)
    content = models.TextField()
    hash = models.CharField(max_length=32, default=None, null=True, blank=True)
    txId = models.CharField(max_length=66, default=None, null=True, blank=True)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def writeOnChain(self):  #in case we can create transactions also for blog
        self.hash = hashlib.sha256(self.content.encode('utf-8')).hexdigest()
        self.txId = sendTransaction(self.hash)
        self.save()

class Lot(models.Model):   #Lot model
    lot = models.CharField(max_length = 20, default=None, null=True)
    id_code = models.CharField(max_length = 30, default=None, null=True)
    description = models.TextField()
    published_date = models.DateTimeField(blank=True, null=True)
    hash = models.CharField(max_length=32, default=None, null=True, blank=True)
    txId = models.CharField(max_length=66, default=None, null=True, blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.lot

class Ip(models.Model):  #Ip model to memorize them
    pub_date = models.DateTimeField('date published')
    ip_address = models.GenericIPAddressField()

class Wal(models.Model):  #Wal model to memorize them
    ropsten = models.TextField(max_length=80, default=None, null=True)
    address = models.TextField(max_length=80, default=None, null=True, blank=True)
    private_key = models.TextField(max_length=80, default=None, null=True, blank=True)
    new_wallet = models.BooleanField(default=False)
    author = models.TextField(max_length=50, default=None, null=True, blank=True)