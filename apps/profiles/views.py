from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from apps.profiles.models import Profile
from core.views import SuperuserRequiredMixin


class IndexView(SuperuserRequiredMixin, ListView):
    model = Profile
    template_name = "user_list.html"
    context_object_name = "profiles"
    paginate_by = 20

    def get_queryset(self):
        queryset = Profile.objects.all()

        query = self.request.GET.get("q", "")
        sort = self.request.GET.get("sort", "-created_on")

        if query:
            queryset = queryset.filter(Q(name__icontains=query))

        if sort == "email_asc":
            queryset = queryset.order_by("actor__email")
        elif sort == "email_desc":
            queryset = queryset.order_by("-actor__email")
        elif sort == "name_asc":
            queryset = queryset.order_by("name")
        elif sort == "name_desc":
            queryset = queryset.order_by("-name")
        elif sort == "newest":
            queryset = queryset.order_by("-created_on")
        elif sort == "oldest":
            queryset = queryset.order_by("created_on")

        return queryset


class DetailView(SuperuserRequiredMixin, DetailView):
    template_name = "user_detail.html"

    def get(self, request, id):
        profile = get_object_or_404(Profile, uid=id)
        return render(request, self.template_name, {"profile": profile})

    def post(self, request, id):
        profile = get_object_or_404(Profile, uid=id)
        profile.name = request.POST.get("name")
        profile.phone_number = request.POST.get("phone_number")
        profile.address = request.POST.get("address")
        profile.save()
        return redirect("user_list")
