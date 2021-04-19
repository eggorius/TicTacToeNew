from django.db import models
from django.shortcuts import reverse
from django.utils import timezone


class Game(models.Model):
    name = models.CharField(unique=True, null=False, max_length=20)
    current_players = models.IntegerField(default=1, null=False)
    created_at = models.DateTimeField(default=timezone.now())
    game_creator = models.CharField(max_length=50, default='', null=False)
    tags = models.ManyToManyField('Tag', blank=True, related_name='games')
    is_over = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('game', kwargs={'name': self.name})

    def set_tags(self, tags):
        self.tags = tags


class Tag(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return ''.join(self.title)


