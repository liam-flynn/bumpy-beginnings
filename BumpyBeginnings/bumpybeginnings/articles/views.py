from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm
from django.contrib.auth.decorators import user_passes_test,  login_required
from .models import Article
from django.db.models import Q
from django.views.generic import ListView
from django.utils.timezone import now
from users.models import SiteUser
from bumpybeginnings.breadcrumbs import get_breadcrumbs
from django.contrib.auth.mixins import LoginRequiredMixin


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'articles.html'
    login_url = '/login/'

    # Help from https://stackoverflow.com/questions/44357028/how-to-use-redirect-at-listview-on-django
    def get(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return redirect('homepage')
        return super(ArticleListView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = get_breadcrumbs(self.request)
        return context

    def get_queryset(self):
        return Article.objects.all()


@user_passes_test(lambda user: user.is_staff, login_url='/login/')
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST,  request.FILES)
        if form.is_valid():
            form.save()
            return redirect('articles')
    else:
        form = ArticleForm()

    return render(request, 'create_article.html', {'form': form, "breadcrumbs": get_breadcrumbs(request)})


def view_article(request, article_id):
    # get the article by its id and make a note of the text
    article = get_object_or_404(Article, id=article_id)
    article_text = article.text

    # depending on the type of user, replace the pronouns of the article text
    if request.user.is_authenticated and not request.user.is_staff:
        site_user = SiteUser.objects.get(user=request.user)
        if site_user.isMother:
            replacements = {
                '{{ you }}': 'you',
                '{{ your }}': 'your',
            }
        else:
            partner_name = site_user.partnerName
            replacements = {
                '{{ you }}': partner_name,
                '{{ your }}': f"{partner_name}'s",
            }
        for placeholder, replacement in replacements.items():
            article_text = article_text.replace(placeholder, replacement)
    else:
        # for staff or unauthenticated users, placeholders remain unchanged
        pass

    return render(request, 'view_article.html', {
        'article': article,
        'article_text': article_text,
        "breadcrumbs": get_breadcrumbs(request)
    })


@user_passes_test(lambda user: user.is_staff, login_url='/login/')
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.delete()
    return redirect('articles')


@user_passes_test(lambda user: user.is_staff, login_url='/login/')
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles')
    else:
        form = ArticleForm(instance=article)

    return render(request, 'edit_article.html', {'form': form, 'article': article, "breadcrumbs": get_breadcrumbs(request)})


@login_required(login_url='/login')
def user_articles(request):
    try:
        # get the SiteUser profile for the logged-in user
        site_user = SiteUser.objects.get(user=request.user)
    except SiteUser.DoesNotExist:
        # Redirect users without a profile to a profile setup page
        return redirect('get_details')

    # Calculate the current pregnancy week
    today = now().date()
    conception_date = site_user.dueDate - timedelta(weeks=40)
    pregnancy_week = max((today - conception_date).days // 7, 0)

    # Fetch relevant articles (order by week, then by newest)
    articles = Article.objects.filter(
        Q(related_week__lte=pregnancy_week) | Q(related_week__isnull=True)
        # Order by week, then by newest
    ).order_by('-related_week', '-creation_date')

    return render(request, 'user_articles.html', {'articles': articles, 'pregnancy_week': pregnancy_week})
