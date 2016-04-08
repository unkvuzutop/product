from django.contrib import admin
from product.models import Product, Comment, Like
from product.utils import make_localtime


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'slug', 'description', 'price',
        'created_at_local', 'modified_at_local']

    readonly_fields = ['created_at_local']

    def created_at_local(self, obj):
        return make_localtime(obj.created_at)

    def modified_at_local(self, obj):
        return make_localtime(obj.modified_at)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'product', 'text', 'created_at_local']
    readonly_fields = ['created_at_local']

    def created_at_local(self, obj):
        return make_localtime(obj.created_at)


class LikeAdmin(admin.ModelAdmin):
    list_display = ['product', 'user']

admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
