from django.shortcuts import render

# Create your views here.
def landing(request):
    return render(
        request,
        'main_pages/landing.html'
    )

def about_me(request):
    return render(
        request,
        'main_pages/about_me.html'
    )