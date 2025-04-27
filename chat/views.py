from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Message

@login_required
def chat_view(request):
    user = request.user
    if request.method == 'POST':
        user_name = request.user.username
        message_text = request.POST.get('message_text')
        if message_text:
            message = Message(user_name=user_name, message_text=message_text)
            if user_name == 'admin':
                message.is_admin = True
            message.save()
            return redirect('chat:chat')

    messages = Message.objects.all().order_by('created_at')
    return render(request, 'chat/chat.html', {'messages': messages, "user": user})