from django.contrib import admin
from .models import Contact,Category,News

# Register your models here.
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title','publish_time','category','status']
    list_filter = ['publish_time']
    search_fields = ['title']
    prepopulated_fields = {'slug':('title',)}
    
     
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    list_filter = ['id']     
     
admin.site.register(Contact)