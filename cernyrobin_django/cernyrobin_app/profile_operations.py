from .models import UserProfile, AnonymousUserProfile
from django.contrib.auth.models import User
import json

def get_profile(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        return UserProfile.objects.get_or_create(user=user)
    else:
        session_key = request.session.session_key

        if not session_key:
            request.session.save()
            session_key = request.session.session_key

        return AnonymousUserProfile.objects.get_or_create(session_key=session_key)

def get_all_profiles():
    return UserProfile.objects.all()

def get_data(user_profile, scope):
    if scope:
        try:
            username = ""

            if hasattr(user_profile, "user"):
                username = user_profile.user.username
            else:
                username = "anonymous"
            
            data = {
                "data": json.loads(getattr(user_profile, scope)),
                "username": username,
            }

            return data
        except AttributeError:
            return None
    else:
        if hasattr(user_profile, "user"):
            return  user_profile.user.username
        else:
            return "anonymous"