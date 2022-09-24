from riseup.models import Investor,Startup,Student

def extras(request):
    username=request.user.username
    user_type=0 #for those user who doesnt have account

    params={}

    if(len(Student.objects.filter(username=username))>0):
        user_type=1
    elif(len(Startup.objects.filter(username=username))>0):
        user_type=2
    elif(len(Investor.objects.filter(username=username))>0):
        user_type=3
    
    params={"user_type":user_type}

    return params