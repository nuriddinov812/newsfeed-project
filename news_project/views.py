from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import ContactForm
from django.views.generic import TemplateView,ListView
from .models import Category,News

# Create your views here.

# def home(pageviewrequest):
#     categories = Category.objects.all()
#     news_list = News.published.exclude(category__name='Mahalliy').order_by('-publish_time')[:15]
#     local_one = News.published.filter(category__name='Mahalliy').order_by('-publish_time')[:1]
#     local_news = News.published.all().filter(category__name='Mahalliy').order_by('-publish_time')[1:6]

#     context = {
#         'news_list':news_list,
#         'categories':categories,
#         'local_news':local_news,
#         'local_one':local_one
#     }
    
#     return render(request, 'index.html', context)

# Home Page View
class HomePageView(ListView):
    model = News
    template_name = 'index.html'
    context_object_name = 'news_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['popular_news'] = News.published.all().order_by('-publish_time')[:4]
        context['photos'] = News.published.all().order_by('-publish_time')[:6]
        context['latest_post'] = News.published.exclude(category__name__in=['Mahalliy', 'Foreign','Technology']).order_by('-publish_time')[:5]
        context['news_list'] = News.published.exclude(category__name__in=['Mahalliy', 'Foreign','Technology']).order_by('-publish_time')       
        context['local_one'] = News.published.filter(category__name='Mahalliy').order_by('-publish_time')[:1]
        context['local_news'] = News.published.filter(category__name='Mahalliy').order_by('-publish_time')[1:6]
        context['foreign_one'] = News.published.filter(category__name='Foreign').order_by('-publish_time')[:1]        
        context['foreign_news'] = News.published.filter(category__name='Foreign').order_by('-publish_time')[1:6]
        context['technology_one'] = News.published.filter(category__name='Technology').order_by('-publish_time')[:1]        
        context['technology_news'] = News.published.filter(category__name='Technology').order_by('-publish_time')[1:6]        
        return context




# def contact(request):
#     form = ContactForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return HttpResponse('<h2>Thanks for your message</h2>')``
    
#     context = {
#         'form':form
#     }
#     return render(request,'contact.html',context=context)

class ContactPageView(TemplateView):
    template_name = 'contact.html'

            
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        
        return render(request, "contact.html", {"form": form})
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        
        if form.is_valid():
            form.save()
            return HttpResponse('<h2>Thanks for your message</h2>')
        
        return render(request, "contact.html", {"form": form})

    
    


class SinglePageView(TemplateView):
    template_name = 'single_page.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        

        news_id = kwargs.get('pk')  
        context['news'] = get_object_or_404(News, pk=news_id)  
        

        context['categories'] = Category.objects.all()
        context['popular_news'] = News.published.all().order_by('-publish_time')[:4]  
        
        return context
    

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)  # Yangilikni ID bo'yicha olish
    return render(request, 'single_page.html', {'news': news})


def news_detail(request,pk):
    news = News.objects.get(pk=pk)
    return render(request,'single_page.html',{'news':news})
    


def single_page(request):
    return render(request,'single_page.html')



def error_page(request):
    return render(request,'404.html')


def news_detail(request,pk):
    news = News.objects.get(pk=pk)
    return render(request,'single_page.html',{'news':news})