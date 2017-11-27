from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.db.models import F
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Post, Comment, PostView, Subscribers
from .forms import PostForm, CommentForm
import nbconvert


def posts_with_tag(request, tag):
    posts = Post.objects.filter(tags__name=tag)
    return render(request, 'blog/post_list.html', {'posts': posts, 'sub_scribe': True})


def post_list(request):
    posts = Post.objects.order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts, 'sub_scribe': True})


def subscribe(request):
    if not request.is_ajax():
        raise Http404
    email = request.POST.get('email')
    subscriber_model = Subscribers()
    subscriber_model.email = email
    subscriber_model.subscribe_date = timezone.now()
    subscriber_model.save()
    return HttpResponse("{}", content_type="application/json")


def record_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    session_id = request.session.session_key
    if not session_id:
        request.session.save()
    session_id = request.session.session_key

    if not PostView.objects.filter(post=post,
                                   session=session_id):
        view = PostView(post=post,
                        ip=request.META['REMOTE_ADDR'],
                        created=timezone.now(),
                        session=session_id)
        view.save()
        Post.objects.filter(pk=post_id).update(view_count=F('view_count') + 1)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    record_view(request, pk)
    return render(request, 'blog/post_detail.html', {'post': post, 'sub_scribe': False})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(request.user, commit=False)
            post.published_date = timezone.now()
            try:
                data = request.FILES['docfile']
                htx = nbconvert.HTMLExporter()
                html = htx.from_file(data)
                post.docfile = html[0]
            except:
                print("no docfile")
                pass
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(request.user, commit=False)
            # post.author = request.user
            post.published_date = timezone.now()
            try:
                data = request.FILES['docfile']
                htx = nbconvert.HTMLExporter()
                html = htx.from_file(data)
                post.docfile = html[0]
            except:
                print("no docfile")
                pass
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
