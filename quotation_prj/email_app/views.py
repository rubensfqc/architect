from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import UserMessageForm
from quotation_app.models import Client
from django.utils.translation import gettext_lazy as _

def email_page(request):
    if request.method == 'POST':
        form = UserMessageForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            user_message = form.save()

            # Send a custom email
            subject = _('Thank you for contacting us!')
            #message = f'Hello {user_message.name},\n\nThank you for reaching out. We will get back to you soon.\n\nBest regards,\nMy Team'
            message = _('Hello {name},\n\nThank you for reaching out. We will get back to you soon.\n\nBest regards,\nMy Team').format(name=user_message.name)
            from_email = 'contact.plat4u@gmail.com'  # Replace with your email
            recipient_list = [user_message.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return redirect('email_success')
    else:
        form = UserMessageForm()

    return render(request, 'email_app/email_page.html', {'form': form})

def email_success(request):
    return render(request, 'email_app/email_success.html')
