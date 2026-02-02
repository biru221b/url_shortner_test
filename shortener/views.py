from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DeleteView, ListView, UpdateView

from .forms import ShortURLForm
from .models import ShortURL


class DashboardView(LoginRequiredMixin, ListView):
    model = ShortURL
    template_name = "shortener/dashboard.html"
    context_object_name = "links"

    def get_queryset(self):
        return ShortURL.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = kwargs.get("form") or ShortURLForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ShortURLForm(request.POST)
        if form.is_valid():
            short_url = form.save(commit=False)
            short_url.user = request.user
            short_url.save()
            messages.success(request, "Short URL created.")
            return redirect("dashboard")
        messages.error(request, "Please correct the errors below.")
        return self.render_to_response(self.get_context_data(form=form))


class ShortURLEditView(LoginRequiredMixin, UpdateView):
    model = ShortURL
    form_class = ShortURLForm
    template_name = "shortener/edit.html"

    def get_queryset(self):
        return ShortURL.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Short URL updated.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("dashboard")


class ShortURLDeleteView(LoginRequiredMixin, DeleteView):
    model = ShortURL
    template_name = "shortener/delete.html"

    def get_queryset(self):
        return ShortURL.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Short URL deleted.")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("dashboard")


def redirect_short(request, short_key: str):
    short_url = get_object_or_404(ShortURL, short_key=short_key)
    if not short_url.is_active or short_url.is_expired:
        raise Http404("Short URL inactive or expired")
    ShortURL.objects.filter(pk=short_url.pk).update(click_count=F("click_count") + 1)
    return redirect(short_url.long_url)
