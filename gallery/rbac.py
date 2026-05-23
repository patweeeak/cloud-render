from django.contrib.auth.models import Group


def user_is_album_admin(user) -> bool:
    """Album admins can edit/delete any photo.

    This is implemented using Django's native Groups.
    Create a group named `album_admin` and add users to it.
    """
    if not user or not user.is_authenticated:
        return False
    return user.groups.filter(name=Group.objects.filter(name="album_admin").first()).exists() if Group.objects.filter(name="album_admin").exists() else False

