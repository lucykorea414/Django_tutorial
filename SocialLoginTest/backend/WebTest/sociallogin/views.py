from django.shortcuts import render

def sociallogin(request):
    return render(request, 'sociallogin/sociallogin.html')