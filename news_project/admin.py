from django.contrib import admin
from .models import Contact,Category,News,Comments

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


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['news','user','created_on','active']
    list_filter = ['created_on','active']
    search_fields = ['body','user__username']
    actions = ['disable_comments','activate_comments']
    
    def disable_comments(self, request, queryset):
        queryset.update(active=False)
        
        
    def activate_comments(self, request, queryset):
        queryset.update(active=True)