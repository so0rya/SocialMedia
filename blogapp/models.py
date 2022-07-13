from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    profile_pic=models.ImageField(upload_to="profilepics",null=True)
    bio=models.CharField(max_length=120)
    phone=models.CharField(max_length=15)
    date_of_birth=models.DateField(null=True)
    options=(
        ("male","male"),
        ("female","female"),
        ("other","other")
    )
    gender=models.CharField(max_length=120,choices=options,default="male")
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="users")
    following=models.ManyToManyField(User,related_name="followings",blank=True)

    @property
    def fetch_followings(self):
        return self.following.all()

    @property
    def fetch_following_count(self):
        return self.fetch_followings.count()

    @property
    def get_invitations(self):
        all_users=UserProfile.objects.all().exclude(user=self.user)
        following_list=[u for u in self.fetch_followings]
        invitations=[user for user in all_users if user not in following_list]
        return invitations

    @property
    def get_followers(self):
        all_users=UserProfile.objects.all()
        followers_list=[]
        for user in all_users:
            if self.user in user.fetch_followings:
                followers_list.append(user)
        return followers_list


class Blogs(models.Model):
    title=models.CharField(max_length=120)
    description=models.CharField(max_length=230)
    image=models.ImageField(upload_to="blogimage",null=True)
    posted_date=models.DateTimeField(auto_now_add=True)
    liked_by=models.ManyToManyField(User)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="author")

    @property
    def get_like_count(self):
        like_count=self.liked_by.all().count()
        return like_count

    @property
    def get_liked_user(self):
        all_likes=self.liked_by.all()
        users = [user.username for user in all_likes]
        return users

    @property
    def get_comments(self):
        all_comments=self.comments_set.all()
        return all_comments

    def __str__(self):
        return self.title

class Comments(models.Model):
    blog=models.ForeignKey(Blogs,on_delete=models.CASCADE)
    comment=models.CharField(max_length=160)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.comment







