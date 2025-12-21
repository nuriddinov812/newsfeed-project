from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import ContactForm
from django.views.generic import TemplateView,ListView,UpdateView,DeleteView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Category,News,Comments
from .models import NewsView
from .forms import CommentForm
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.db.models import Q, F
from django.utils import timezone
from datetime import timedelta
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
        news = get_object_or_404(News, pk=news_id)
        # Record view by unique IP
        ip = self._get_client_ip(self.request)
        if ip:
            # create view if not exists; unique_together prevents duplicates
            created = False
            try:
                obj, created = NewsView.objects.get_or_create(news=news, ip_address=ip)
            except Exception:
                # In rare race conditions a duplicate insertion may raise; ignore
                created = False

            if created:
                # increment stored counter atomically
                News.objects.filter(pk=news.pk).update(views_count=F('views_count') + 1)


  

        context['news'] = news
        context['popular_news'] = News.published.all().order_by('-publish_time')[:4]  

        context['comments'] = context['news'].comments.all().order_by('-created_on')

        context['comments_count'] = Comments.objects.filter(news=news, active=True).count()

        context['comment_form'] = CommentForm()
        return context

    def _get_client_ip(self, request):
        """Return the client's IP address, respecting X-Forwarded-For if present."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # X-Forwarded-For can contain multiple IPs, take the first one
            ip = x_forwarded_for.split(',')[0].strip()
            return ip
        return request.META.get('REMOTE_ADDR')
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        news = context['news']
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
            # We calculate comment counts on the fly; do not update a non-existent
            # `comment_count` field on News (avoid FieldDoesNotExist).
            return redirect('single_page', pk=news.pk, slug=news.slug)

        context['comment_form'] = comment_form
        return render(request, self.template_name, context)
    
    
    

# def news_detail(request, pk, slug):
#     news = get_object_or_404(News, pk=pk, slug=slug)  # Yangilikni ID bo'yicha olish
#     comments = news.comments.filter(active=True).order_by('-created_on') 
#     new_comment = None

#     if news.slug != slug:
#         return redirect(
#             reverse('single_page', kwargs={'pk': news.pk, 'slug': news.slug})
#         )    
#     if request.method == 'POST':
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.news = news
#             new_comment.user = request.user
#             new_comment.save()
#     else:
#         comment_form = CommentForm()
        
#     context = {
#         'popular_news': News.published.all().order_by('-publish_time')[:4],
#         'categories': Category.objects.all(),
#         'news': news,
#         'comments': comments,
#         'new_comment': new_comment,
#         'comment_form': comment_form
#     }   

#     return render(request, 'news/single_page.html', context)




def error_page(request):
    return render(request,'news/404.html')


class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ['title', 'title_uz', 'title_en', 'title_ru', 'body_uz', 'body_en', 'body_ru', 'image', 'category','status']
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



class SearchResultsView(ListView):
    model = News
    template_name = 'news/search_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = (self.request.GET.get('q') or '').strip()
        if not query:
            return News.published.none()
        return News.published.filter(Q(title__icontains=query) | Q(body__icontains=query))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context
    
    