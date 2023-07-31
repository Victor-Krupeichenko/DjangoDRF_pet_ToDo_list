from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .models import Task
from .forms import CreateTaskForm, RegisterUserForm, LoginUserForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST


class ListTaskViews(ListView):
    """List Task"""
    model = Task
    template_name = "todo_list/index.html"
    paginate_by = 1

    def get_queryset(self):
        return Task.objects.filter(execute_status=False, user=self.request.user.pk).select_related("user")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "ToDo"
        return context


class CreateTask(LoginRequiredMixin, CreateView):
    """Create Task"""
    form_class = CreateTaskForm
    template_name = "todo_list/task_create.html"

    def form_valid(self, form):
        try:
            task = form.save(commit=False)
            task.user_id = self.request.user.pk
            task.save()
            messages.success(self.request, message=f"Task: {task.title} created")
            return redirect("home")
        except Exception as ex:
            messages.error(self.request, message=f"Error {ex} task not created")
        context = self.get_context_data(form=form)
        return self.render_to_response(context=context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Task"
        return context


@require_POST
def chenge_status(rquest, task_id):
    """Chenge Status Task"""
    task = Task.objects.filter(pk=task_id).first()
    if task:
        task.execute_status = not task.execute_status
        task.save()
        messages.success(rquest, message=f"{task.title} completed")
    else:
        messages.error(rquest, message=f"Task not found")
    return redirect("home")


class RegisterUser(CreateView):
    """Create User"""
    form_class = RegisterUserForm
    template_name = "todo_list/user_register_or_login.html"

    def form_valid(self, form):
        try:
            user = form.save()
            messages.success(self.request, message=f"{user.username} Successfully created")
            login(self.request, user)
            return redirect("home")
        except Exception as ex:
            messages.error(self.request, message=f"Error {ex}")
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["register_user"] = True
        context["title"] = "Register User"
        return context


class LoginUser(LoginView):
    """Login User"""
    form_class = LoginUserForm
    template_name = "todo_list/user_register_or_login.html"
    success_url = reverse_lazy("home")

    def get_success_url(self):
        return self.success_url

    def form_valid(self, form):
        messages.success(self.request, message=f"{form.cleaned_data.get('username')} Successfully logged in")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, message=f"{form.cleaned_data.get('username')} Error")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Login User"
        context["login"] = True
        return context


def user_logout(requset):
    """Logout User"""
    logout(requset)
    return redirect("login_user")
