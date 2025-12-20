from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import ContactForm
from django.views.generic import TemplateView,ListView,UpdateView,DeleteView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Category,News,Comments
from .forms import CommentForm
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from news_project.custom_permissions import OnlyLoggedSuperUser

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
    template_name = 'news/index.html'
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
    template_name = 'news/contact.html'

            
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        
        return render(request, "news/contact.html", {"form": form})
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        
        if form.is_valid():
            form.save()
            return HttpResponse('<h2>Thanks for your message</h2>')
        
        return render(request, "news/contact.html", {"form": form})

    
    


class SinglePageView(TemplateView):
    template_name = 'news/single_page.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        

        news_id = kwargs.get('pk')  
        context['news'] = get_object_or_404(News, pk=news_id)  
        

        context['categories'] = Category.objects.all()
        context['popular_news'] = News.published.all().order_by('-publish_time')[:4]  

        context['comments'] = context['news'].comments.all().order_by('-created_on')

        context['comment_form'] = CommentForm()
        
        return context

    def post(self, request, *args, **kwargs):

        form = CommentForm(request.POST)
        news_id = kwargs.get('pk')
        news = get_object_or_404(News, pk=news_id)
        if form.is_valid():
            Comments.objects.create(news=news, body=form.cleaned_data['body'])
            # Redirect to same page to avoid form resubmission
            return redirect(reverse('single_page', kwargs={'pk': news.pk, 'slug': news.slug}))
        # If invalid, render template with form errors
        context = self.get_context_data(**kwargs)
        context['comment_form'] = form
        return self.render_to_response(context)
    

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)  # Yangilikni ID bo'yicha olish
    return render(request, 'news/single_page.html', {'news': news})



def error_page(request):
    return render(request,'news/404.html')


class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ['title', 'body', 'image', 'category','status']
    template_name = 'crud/news_update.html'
    success_url = reverse_lazy('home')


class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'    
    success_url = reverse_lazy('home')
    
    


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    fields = '__all__'
    template_name = 'crud/news_create.html'
    success_url = reverse_lazy('home')

@login_required
@user_passes_test(lambda user: user.is_superuser)
def admin_page(request):

    admin_users = User.objects.select_related('profile').all()
    context = {
        'admin_users': admin_users
    }
    return render(request, 'pages/admin_page.html', context)