# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.core.paginator import Paginator
# from django.db.models import Q
# from django.http import HttpResponseForbidden
# from django.urls import reverse_lazy
# from django.shortcuts import redirect
# from django.contrib import messages
# from django.views.generic import View

# from cloudinary import uploader as cloudinary_uploader

# from .forms import RecipePhotoForm
# from .models import RecipePhoto

# def user_is_album_admin(user):
#     return user.is_authenticated and (user.is_staff or user.is_superuser)

# class GalleryHomeView(LoginRequiredMixin, View):
#     template_name = "gallery/home.html"
#     paginate_by = 2

#     def get(self, request):
#         query = request.GET.get("q", "")

#         if query:
#             photo_list = (
#                 RecipePhoto.objects.filter(
#                     Q(title__icontains=query) | Q(description__icontains=query)
#                 ).order_by("-uploaded_at")
#             )
#         else:
#             photo_list = RecipePhoto.objects.all().order_by("-uploaded_at")

#         paginator = Paginator(photo_list, self.paginate_by)
#         page_number = request.GET.get("page")
#         photos = paginator.get_page(page_number)

#         form = RecipePhotoForm()
#         return self.render_to_response(request, form=form, photos=photos, query=query)

#     def render_to_response(self, request, **context):
#         from django.shortcuts import render

#         return render(request, self.template_name, context)

#     def post(self, request):
#         form = RecipePhotoForm(request.POST, request.FILES)
#         if form.is_valid():
#             instance = form.save()
#             messages.success(request, f"'{instance.title}' uploaded successfully!")
#             return redirect("gallery_home")

#         # If invalid, re-render with errors
#         query = request.GET.get("q", "")
#         photos = RecipePhoto.objects.all().order_by("-uploaded_at")
#         paginator = Paginator(photos, self.paginate_by)
#         page_number = request.GET.get("page")
#         paged_photos = paginator.get_page(page_number)
#         return self.render_to_response(
#             request,
#             form=form,
#             photos=paged_photos,
#             query=query,
#         )


# class RecipePhotoCreateView(LoginRequiredMixin, View):
#     template_name = "gallery/home.html"

#     def post(self, request):
#         form = RecipePhotoForm(request.POST, request.FILES)
#         if form.is_valid():
#             obj = form.save()
#             messages.success(request, f"'{obj.title}' uploaded successfully!")
#             return redirect("gallery_home")
#         # If invalid, fall back to home context (keeps the same search query/page if present)
#         query = request.GET.get("q", "")
#         if query:
#             photo_list = RecipePhoto.objects.filter(
#                 Q(title__icontains=query) | Q(description__icontains=query)
#             ).order_by("-uploaded_at")
#         else:
#             photo_list = RecipePhoto.objects.all().order_by("-uploaded_at")

#         paginator = Paginator(photo_list, 2)
#         page_number = request.GET.get("page")
#         photos = paginator.get_page(page_number)

#         return render(
#             request,
#             self.template_name,
#             {"form": form, "photos": photos, "query": query},
#         )


# class RecipePhotoUpdateView(LoginRequiredMixin, View):
#     template_name = "gallery/edit.html"

#     def dispatch(self, request, *args, **kwargs):
#         # RBAC: album_admin can edit any photo.
#         # Current model doesn't track per-user ownership, so only admins can edit.
#         if not user_is_album_admin(request.user):
#             return HttpResponseForbidden("You do not have permission to edit this photo.")
#         return super().dispatch(request, *args, **kwargs)

#     def get_object(self, pk):
#         return RecipePhoto.objects.get(pk=pk)

#     def get(self, request, pk):
#         photo = self.get_object(pk)
#         form = RecipePhotoForm(instance=photo)
#         return self.render_to_response(request, form=form, photo=photo)

#     def post(self, request, pk):
#         photo = self.get_object(pk)
#         form = RecipePhotoForm(request.POST, request.FILES, instance=photo)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f"'{photo.title}' updated successfully!")
#             return redirect("gallery_home")
#         return self.render_to_response(request, form=form, photo=photo)

#     def render_to_response(self, request, **context):
#         from django.shortcuts import render

#         return render(request, self.template_name, context)


# class RecipePhotoDeleteView(LoginRequiredMixin, View):
#     template_name = "gallery/delete.html"

#     def dispatch(self, request, *args, **kwargs):
#         # RBAC: album_admin can delete any photo.
#         if not user_is_album_admin(request.user):
#             return HttpResponseForbidden("You do not have permission to delete this photo.")
#         return super().dispatch(request, *args, **kwargs)

#     def get_object(self, pk):
#         return RecipePhoto.objects.get(pk=pk)

#     def get(self, request, pk):
#         photo = self.get_object(pk)
#         return self.render_to_response(request, photo=photo)

#     def post(self, request, pk):
#         photo = self.get_object(pk)

#         # Permanent delete from Cloudinary + DB row.
#         if photo.image:
#             try:
#                 cloudinary_uploader.destroy(photo.image.public_id)
#             except Exception as e:
#                 # Best-effort: still delete DB record.
#                 print(f"Cloudinary deletion failed: {e}")

#         title = photo.title
#         photo.delete()
#         messages.success(request, f"'{title}' was completely deleted.")
#         return redirect("gallery_home")

#     def render_to_response(self, request, **context):
#         from django.shortcuts import render

#         return render(request, self.template_name, context)



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