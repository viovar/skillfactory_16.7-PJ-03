from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, UserResponse
from .filters import PostFilter, ResponseFilter
from .forms import PostForm, ResponsesForm, EditForm

class PostList(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    # paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] =self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'Post'

class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    success_url = '/posts/'
    context_object_name = 'post_create'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = EditForm
    model = Post
    template_name = 'post_create.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

class ResponseList(LoginRequiredMixin, ListView):
    form_class = ResponsesForm
    model = UserResponse
    template_name = 'response_list.html'
    context_object_name = 'response_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(post__author=self.request.user)
        self.filterset = ResponseFilter(self.request.GET, queryset, request=self.request.user.id)
        return self.filterset.qs

class ResponseCreate(LoginRequiredMixin, CreateView):
    form_class = ResponsesForm
    model = UserResponse
    template_name = 'response_create.html'
    success_url = reverse_lazy('post_list')


    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)



    def get_context_data(self, *args, **kwargs):
        cat_menu = Post.get_categories()
        context = super(CreateView, self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        return context

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})

class ResponseDelete(DeleteView):
    model = UserResponse
    template_name = 'response_delete.html'
    success_url = reverse_lazy('response_list')

def response_status(request, pk):
    response_objects = UserResponse.objects.get(pk=pk)
    response_objects.status = True
    response_objects.save()
    return HttpResponseRedirect(reverse_lazy('response_list'))
