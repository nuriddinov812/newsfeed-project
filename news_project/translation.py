from modeltranslation.translator import register, TranslationOptions
from .models import News, Category, Comments

@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'body',)

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Comments)
class CommentsTranslationOptions(TranslationOptions):
    fields = ('body',)

