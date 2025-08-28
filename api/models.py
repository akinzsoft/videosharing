from django.db import models

class TblCreator(models.Model):  # Capitalized class name for convention (PEP8)
    name = models.CharField(max_length=128, null=True, blank=True)
    country = models.CharField(max_length=100)
    gender = models.CharField(max_length=128, null=True, blank=True)
    astatus = models.CharField(max_length=128, null=True, blank=True)
    phoneno = models.CharField(max_length=128, null=True, blank=True)
    email = models.EmailField(max_length=128, null=True, blank=True)  # Better field type
    address = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    state = models.CharField(max_length=128, null=True, blank=True)
    zipcode = models.CharField(max_length=128, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)  # Use DateField for dates
    username = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.name or "Unnamed Creator"
    
    

class TblCreator(models.Model):  # Capitalized class name for convention (PEP8)
    name = models.CharField(max_length=128, null=True, blank=True)
    country = models.CharField(max_length=100)
    gender = models.CharField(max_length=128, null=True, blank=True)
    astatus = models.CharField(max_length=128, null=True, blank=True)
    phoneno = models.CharField(max_length=128, null=True, blank=True)
    email = models.EmailField(max_length=128, null=True, blank=True)  # Better field type
    address = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    state = models.CharField(max_length=128, null=True, blank=True)
    zipcode = models.CharField(max_length=128, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)  # Use DateField for dates
    username = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.name or "Unnamed Creator"
    
class Video(models.Model):
    title = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    producer = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    age_rating = models.CharField(max_length=10)
    movie_type = models.CharField(max_length=50)
    video_file = models.FileField(upload_to="videos/")  # stored in /media/videos/
    username = models.CharField(max_length=128, null=True, blank=True)
    thumbnail =models.FileField(upload_to="images/",default="images/default.jpg")  # stored in /media/images/

    def __str__(self):
        return self.title
    

class tblcomment(models.Model):
    movieid = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    mesg = models.CharField(max_length=255)
    rating = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return self.username
    
 