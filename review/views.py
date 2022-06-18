from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Review, Category, Tag
from .forms import CommentForm

class ReviewUpate(LoginRequiredMixin, UpdateView):
    model = Review
    fields = ['title',  'content', 'attached_file', 'category', 'tags']

    template_name = 'review/review_form_update.html'

    def dispatch(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.is_authenticated and current_user == self.get_object().author: #or current_user== superuser:
            return super(ReviewUpate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

class ReviewCreate(LoginRequiredMixin, UserPassesTestMixin,CreateView):
    model = Review
    fields = ['title', 'content', 'attached_file', 'category', 'tags']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(ReviewCreate, self).form_valid(form)
        else:
            return redirect('/review/')

class ReviewList(ListView):
    model = Review
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ReviewList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['count_reviews_without_category'] = Review.objects.filter(category=None).count()

        return context


class ReviewDetail(DetailView):
    model = Review

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ReviewDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['count_reviews_without_category'] = Review.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
        return context


def show_category_reviews(request, slug):
    if slug == 'no-category': #미분류 글 요청
        category = '미분류'
        review_list = Review.objects.filter(category=None)
    else:
        category = Category.objects.get(slug = slug)
        review_list = Review.objects.filter(category=category)
    context = {
        'categories' : Category.objects.all(),
        'count_reviews_without_category' : Review.objects.filter(category=None).count(),
        'category' : category,
        'review_list' : review_list
    }
    return render(request, 'review/review_list.html', context)


def show_tag_reviews(request, slug):
    tag = Tag.objects.get(slug=slug)
    review_list = tag.review_set.all()
    context = {
        'categories' : Category.objects.all(),
        'count_reviews_without_category' : Review.objects.filter(category=None).count(),
        'tag' : tag,
        'review_list' : review_list
    }

    return render(request, 'review/review_list.html', context)


def add_comment(request, pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=pk) #만약 pk에 해당되는 애가 없으면 404 error #post = Post.object.get(pk=pk) -> 505 error

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            # if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.review = review
            comment.author = request.user
            comment.save()
            return redirect(comment.get_absolute_url())
        else:
            return redirect(review.get_absolute_url())
    else:
        raise PermissionDenied