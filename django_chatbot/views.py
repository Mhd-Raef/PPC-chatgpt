from django.shortcuts import render

def index(request):
    return render(request,'index.html')

from django.http import JsonResponse

def get_csrf_token(request):
    return JsonResponse({'csrfToken': request.COOKIES['csrftoken']})
