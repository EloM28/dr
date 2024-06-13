from django.shortcuts import render
from django.http.response import HttpResponse,HttpResponseNotFound,Http404,HttpResponseRedirect
from django.urls import reverse
# Create your views here.

# articles={
#     'sports':'Sports Page',
#     'finance':'Finance Page',
#     'politics':'Politics Page',
# }
# def sports_view(request):
#     return HttpResponse(articles['sports'])
# def finance_view(request):
#     return HttpResponse(articles['finance'])
# def news_view(request,topic):
#     try:
#         result=articles[topic]
#         return HttpResponse(articles[topic])
#     except:
#         result='No Page for that topic'
#         raise Http404('404 GENERIC ERROR')  # 404.html
# def add_view(request,num1,num2):
#     add_result=num1+num2
#     result=f'{num1} + {num2}={add_result}'
#     return HttpResponse(str(result))

# domain.com/first_app/0 --->domain.com/first_app/sports   
# def num_page_view(request,num_page):
#     topics_list=list(articles.keys()) # ['sports','finance','politics']
#     topic=topics_list[num_page]
#     webpage=reverse('topic-page', args=[topic])
#     return HttpResponseRedirect(webpage )

def simple_view(request):
    return render(request,'first_app/example.html')