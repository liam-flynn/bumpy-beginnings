from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Forum, Post, Comment, Vote
from django.contrib.auth.decorators import user_passes_test
from .forms import ForumForm, PostForm, CommentForm
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.safestring import mark_safe
from bumpybeginnings.breadcrumbs import get_breadcrumbs
from django.contrib import messages
import json

# lists all forums on forums page
class ForumListView(ListView):
    model = Forum
    template_name = 'forum_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = get_breadcrumbs(self.request)
        return context

    def get_queryset(self):
        # if you are a staff member, show all forums.
        if self.request.user.is_staff:
            return Forum.objects.all()
        # otherwise, just return the live forums
        return Forum.objects.filter(isLive=True)
    
# only staff members can create new forums
@user_passes_test(lambda user: user.is_staff, login_url='/login/')
def create_forum(request):
    if request.method == 'POST':
        form = ForumForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('forum_list')
    else:
        form = ForumForm()

    context = {'form': form, 'breadcrumbs': get_breadcrumbs(request)}
    return render(request, 'create_forum.html', context)

# only staff can delete forums
@user_passes_test(lambda user: user.is_staff, login_url='/login/')
def delete_forum(request, forum_id):
    # find the forum using the forum id and delete it
    forum = get_object_or_404(Forum, id=forum_id)
    forum.delete()
    return redirect('forum_list')


@user_passes_test(lambda user: user.is_staff, login_url='/login/')
def deactivate_forum(request, forum_id):
    # find the forum using the forum id and swap the status to inactive
    forum = get_object_or_404(Forum, id=forum_id)
    forum.isLive = False
    forum.save()
    return redirect('forum_list')

@user_passes_test(lambda user: user.is_staff, login_url='/login/')
def reactivate_forum(request, forum_id):
    # find the forum using the forum id and swap the status to inactive
    forum = get_object_or_404(Forum, id=forum_id)
    forum.isLive = True
    forum.save()
    return redirect('forum_list')

# used for forum detail page (lists all posts within a forum)
class ForumDetailView(DetailView):
    model = Forum
    template_name = 'forum_detail.html'
    context_object_name = 'forum'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get all posts for this forum
        context['posts'] = self.object.posts.all()  
        # add the post form to the context
        context['form'] = PostForm()
        context['breadcrumbs'] = get_breadcrumbs(self.request)
        return context
    

    # Handle the submission of a new post
    def post(self, request, *args, **kwargs):
        forum = self.get_object()
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.forum = forum
            post.poster = request.user
            post.save()
            return redirect('forum_detail', pk=forum.pk)
        return self.render_to_response(self.get_context_data(form=form))


# used for the post detail page (lists all the comments in that post)
# help with expanding generic view from https://docs.djangoproject.com/en/5.1/topics/class-based-views/generic-display/
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


    def get_object(self):
        # get the forum and post id from the URL
        forum_id = self.kwargs['forum_id']
        post_id = self.kwargs['pk']
        # get the post using those id's
        return get_object_or_404(Post, pk=post_id, forum_id=forum_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get all the comments linked to the post
        comments = self.object.comments.all().order_by('createdOn')
        # get all the votes the user had performed on those comments
        user_votes = {}
        if self.request.user.is_authenticated:
            user_votes = {
                vote.comment.id: vote.vote_type
                for vote in Vote.objects.filter(user=self.request.user, comment__in=comments)
            }

        # pass the cooments, votes, comment form and breadcrumbs to the page
        context['comments'] = comments
        context['user_votes_json'] = json.dumps(user_votes)
        context['form'] = CommentForm()  
        context['breadcrumbs'] = get_breadcrumbs(self.request)
        return context

    # handle submitting a new comment
    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.commenter = request.user
            comment.save()
            return redirect('post_detail', forum_id=post.forum_id, pk=post.pk)
        return self.render_to_response(self.get_context_data(form=form))


# helper function to prevent 'D.R.Y'
def can_manage_post_or_comment(user, obj):
    if user.is_staff or user.siteuser.isForumMod:
        return True
    # Allow creators to manage their own posts or comments
    if isinstance(obj, Post) and obj.poster == user:
        return True
    if isinstance(obj, Comment) and obj.commenter == user:
        return True
    return False


def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if not can_manage_post_or_comment(request.user, post):
        raise PermissionDenied

    # Store the forum id to redirect back to the forum page
    forum_pk = post.forum.pk  
    post.delete()
    return redirect('forum_detail', pk=forum_pk)


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if not can_manage_post_or_comment(request.user, comment):
        raise PermissionDenied

    # Store the post ID to redirect back to the post page
    comment.delete(request)
    messages.success(request, "Comment has been deleted successfully.")
    # help from https://stackoverflow.com/questions/39560175/redirect-to-same-page-after-post-method-using-class-based-views
    referer_url = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(referer_url)


def upvote_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    vote, created = Vote.objects.get_or_create(user=request.user, comment=comment)

    if vote.vote_type == 'upvote':
        # User has already upvoted; remove the vote
        vote.delete()
        comment.score -= 1
    elif vote.vote_type == 'downvote':
        # User switches from downvote to upvote
        vote.vote_type = 'upvote'
        vote.save()
        # Neutralize the downvote and add the upvote
        comment.score += 2  
    else:
        # user upvotes for the first time
        vote.vote_type = 'upvote'
        vote.save()
        comment.score += 1

    comment.save()
    return JsonResponse({"score": comment.score})


def downvote_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    vote, created = Vote.objects.get_or_create(user=request.user, comment=comment)

    if vote.vote_type == 'downvote':
        # User has already downvoted; remove the vote
        vote.delete()
        comment.score += 1
    elif vote.vote_type == 'upvote':
        # User switches from upvote to downvote
        vote.vote_type = 'downvote'
        vote.save()
        # Neutralize the upvote and add the downvote
        comment.score -= 2  
    else:
        # User downvotes for the first time
        vote.vote_type = 'downvote'
        vote.save()
        comment.score -= 1

    comment.save()
    return JsonResponse({"score": comment.score})



@user_passes_test(lambda user: user.is_staff, login_url='/login/')
def low_score_comments(request):

    # get the threshold from the page but if not provided or on the first GET use -2
    threshold = int(request.POST.get('threshold', -2)) if request.method == "POST" else -2

    # get a list of comments and their related details
    comments = Comment.objects.filter(score__lt=threshold).select_related('post', 'commenter')

    context = {
        'comments': comments,
        'threshold': threshold,
    }

    return render(request, 'low_score_comments.html', context)