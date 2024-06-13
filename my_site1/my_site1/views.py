from django.shortcuts import render

def error_view_func(request,exception):
    return render(request,'404.html',status=404)