from django.db import models
from taggit.managers import TaggableManager


class Paper(models.Model):
    """
    Model of the research paper that will be manipulated in the frontend.
    """
    abstract = models.TextField()
    title = models.CharField(max_length=1000)
    author = models.CharField(max_length=1000)
    paper_url = models.CharField(max_length=1000)
    published_date = models.CharField(max_length=250)
    subject = models.CharField(max_length=250)
    updated = models.CharField(max_length=250)
    pdf_url = models.CharField(max_length=1000)
    tags = TaggableManager()

    class Meta:
        ordering = ['id']


    def __str__(self):
        return self.title

class Comment(models.Model):
    # foreignKey: associate each comment with a single paper - i.e many to one relationship
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.paper}'
