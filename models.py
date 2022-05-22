from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    author_User = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_Author = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.author_User.comment.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.rating_Author = pRat * 3 + cRat
        self.save()


# update_rating модели Author, который обновляет рейтинг пользователя, переданный в аргумент этого метода.
# Он состоит из следующего:
# суммарный рейтинг каждой статьи автора умножается на 3;
# суммарный рейтинг всех комментариев автора;
# суммарный рейтинг всех комментариев к статьям автора

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = "AR"
    CATEGORY_CHOICE = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    category_Type = models.CharField(max_length=2, choices=CATEGORY_CHOICE, default=ARTICLE)
    date_Creation = models.DateTimeField(auto_now_add=True)
    post_Category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating += 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'


class PostCategory(models.Model):
    post_Thorough = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_Through = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_Post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_User = models.ForeignKey(User, on_delete=models.CASCADE)
    texst = models.TextField()
    dete_Creation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating += 1
        self.save()
