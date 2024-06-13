from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def example_view(request):
    return render(request,'my_app/example.html')
def variable_view(request):
    my_var={"first_name":"roSe","last_name":"derRick",
            "some_list":[5,6,7],"some_dict":{"docker":"conteneurisation","AWS":"Amazon cloud Server"},
            'user_loggedin':True}
    return render(request,'my_app/variable.html',context=my_var)
    # return render(request,'my_app/variable.html')