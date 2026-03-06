from django.contrib.auth import get_user_model

# from django.core.exceptions import PermissionDenied

# def block_admin_google_login(backend, user=None, **kwargs):
#     if user and user.is_staff:
#         raise PermissionDenied("ADMIN_GOOGLE_BLOCK")


User = get_user_model()


def link_to_existing_user(strategy, details, backend, user=None, *args, **kwargs):
    """
    If a Google account email matches an existing user (normal signup),
    then use the existing user instead of creating a new one.
    """
    email = details.get('email')

    # If user already found in pipeline, do nothing
    if user:
        return {'user': user}

    if email:
        try:
            existing_user = User.objects.get(email=email)
            return {'user': existing_user}
        except User.DoesNotExist:
            return {}  # no existing user, allow create_user step to run
