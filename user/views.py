from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from shop.forms import UserProfile


def users(request):
    return redirect('product_list')

def account(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'users/404.html', status=404)

    try:
        profile = user.userprofile
    except User.userprofile.RelatedObjectDoesNotExist:
        profile = None

    return render(request, 'users/account_profile.html', {'profile': profile, 'user': user})
