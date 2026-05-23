from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View

from cloudinary import uploader as cloudinary_uploader

from .forms import RecipePhotoForm
from .models import RecipePhoto


def user_is_album_admin(user):
    """Album admins: staff or superuser accounts only."""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


class GalleryHomeView(LoginRequiredMixin, View):
    template_name = "gallery/home.html"
    paginate_by = 2

    def get(self, request):
        query = request.GET.get("q", "")
        if query:
            photo_list = RecipePhoto.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            ).order_by("-uploaded_at")
        else:
            photo_list = RecipePhoto.objects.all().order_by("-uploaded_at")

        paginator = Paginator(photo_list, self.paginate_by)
        photos = paginator.get_page(request.GET.get("page"))
        form = RecipePhotoForm()

        return render(request, self.template_name, {
            "form": form,
            "photos": photos,
            "query": query,
            "is_admin": user_is_album_admin(request.user),  # pass role to template
        })

    def post(self, request):
        # Standard users can upload
        form = RecipePhotoForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            messages.success(request, f"'{instance.title}' uploaded successfully!")
            return redirect("gallery_home")

        query = request.GET.get("q", "")
        photo_list = RecipePhoto.objects.all().order_by("-uploaded_at")
        paginator = Paginator(photo_list, self.paginate_by)
        photos = paginator.get_page(request.GET.get("page"))

        return render(request, self.template_name, {
            "form": form,
            "photos": photos,
            "query": query,
            "is_admin": user_is_album_admin(request.user),
        })


class RecipePhotoCreateView(LoginRequiredMixin, View):
    """Any authenticated user can upload."""
    template_name = "gallery/home.html"

    def post(self, request):
        form = RecipePhotoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            messages.success(request, f"'{obj.title}' uploaded successfully!")
            return redirect("gallery_home")

        query = request.GET.get("q", "")
        photo_list = RecipePhoto.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).order_by("-uploaded_at") if query else RecipePhoto.objects.all().order_by("-uploaded_at")

        paginator = Paginator(photo_list, 2)
        photos = paginator.get_page(request.GET.get("page"))

        return render(request, self.template_name, {
            "form": form,
            "photos": photos,
            "query": query,
            "is_admin": user_is_album_admin(request.user),
        })


class RecipePhotoUpdateView(LoginRequiredMixin, View):
    """Only album admins (staff/superuser) can edit."""
    template_name = "gallery/edit.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if not user_is_album_admin(request.user):
            messages.error(request, "Only album administrators can edit photos.")
            return redirect("gallery_home")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, pk):
        return RecipePhoto.objects.get(pk=pk)

    def get(self, request, pk):
        photo = self.get_object(pk)
        form = RecipePhotoForm(instance=photo)
        return render(request, self.template_name, {"form": form, "photo": photo})

    def post(self, request, pk):
        photo = self.get_object(pk)
        form = RecipePhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{photo.title}' updated successfully!")
            return redirect("gallery_home")
        return render(request, self.template_name, {"form": form, "photo": photo})


class RecipePhotoDeleteView(LoginRequiredMixin, View):
    """Only album admins (staff/superuser) can delete."""
    template_name = "gallery/delete.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if not user_is_album_admin(request.user):
            messages.error(request, "Only album administrators can delete photos.")
            return redirect("gallery_home")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, pk):
        return RecipePhoto.objects.get(pk=pk)

    def get(self, request, pk):
        photo = self.get_object(pk)
        return render(request, self.template_name, {"photo": photo})

    def post(self, request, pk):
        photo = self.get_object(pk)
        if photo.image:
            try:
                cloudinary_uploader.destroy(photo.image.public_id)
            except Exception as e:
                print(f"Cloudinary deletion failed: {e}")

        title = photo.title
        photo.delete()
        messages.success(request, f"'{title}' was completely deleted.")
        return redirect("gallery_home")