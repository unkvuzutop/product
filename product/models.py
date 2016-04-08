# -*- coding: utf-8 -*-
from datetime import timedelta
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=220, null=False, blank=True)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(max_digits=16, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(default=timezone.now)

    def last_comments(self):
        return self.comment_set.filter(
            created_at__gte=(timezone.now() - timedelta(hours=24)))

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.slug)])


class Like(models.Model):
    product = models.ForeignKey(Product, default=None)
    user = models.ForeignKey(User)

    class Meta:
        unique_together = ("product", "user", )

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.product.slug)])


class Comment(models.Model):
    user = models.ForeignKey(User, default=None, null=True, blank=True)
    name = models.CharField(
        max_length=16, blank=True, null=False,
        validators=[
            MinLengthValidator(4),
            RegexValidator(
                regex=u'^[a-zA-Z0-9а-я-А-Я]*$',
                message='Username must be Alphanumeric',
                code='invalid_username'
            )
        ])
    product = models.ForeignKey(Product)
    text = models.TextField(
        blank=False, null=False, validators=[MinLengthValidator(20)])
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ['-created_at']

    def __unicode__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.product.slug)])

    def get_author(self):
        if self.user:
            user = self.user.username
        elif self.name:
            user = self.name
        else:
            user = 'Anonym'
        return user
