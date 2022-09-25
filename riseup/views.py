from urllib import response
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from django.contrib import messages
from math import ceil
from riseup.models import *

import io
import json

# Create your views here.

def home(request):
    params={}
    startup_details=Startup.objects.all()
    startup_list=[]
    #?selects the only comapanies whose all details are filled
    for i in startup_details:
        if(i.completion_status==1):
            startup_list.append(i)
    params['startup_details']=startup_list
    return render(request,"home.html",params)



def signup(request):
    flag=0
    if(request.method=='POST'):
        username=request.POST['username']
        name=request.POST['fname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        choice=request.POST['choice']
        currentPath=request.POST['currentPathsignIn']
        
        #?validation part
        flag=0
        if len(username)<3 or len(username)>20:
            messages.warning(request, 'Username is either too long or too short')
            flag=1
        if not username.isalnum():
            messages.warning(request, 'Username should contain either alphabets or numerics')
            flag=1
        if pass1!=pass2:
            messages.warning(request, 'Password is not matching')
            flag=1


        #? if validation fails return imediatly
        if flag==1:
            return redirect(currentPath)


        #?validation for already existing users username and emailid
        if(len(User.objects.filter(username=username))>0):
            messages.warning(request, 'Username already exists')
            return redirect(currentPath)

        if(len(User.objects.filter(email=email))>0):
            messages.warning(request, 'Email already exists')
            return redirect(currentPath)



        choice = int(choice)
        if(choice==1):
            signup = Student(name=name,email=email,user_type=1,username=username )
            signup.save()

        if(choice==2):
            signup = Startup(name=name,email=email,user_type=2,username=username )
            signup.save()

        if(choice==3):
            signup = Investor(name=name,email=email,user_type=3,username=username )
            signup.save()


        newUser=User.objects.create_user(username,email,pass1)
        newUser.first_name=name
        newUser.save()
        messages.success(request, 'Successfully created account')
        login(request,newUser)
        return redirect(currentPath)




def userLogin(request):
    if (request.method=="POST"):
        username=request.POST['loginusername']
        userpass=request.POST['loginpass']
        currentPathlogIn=request.POST['currentPathlogIn']
        choice=request.POST['Choice']

        user=authenticate(request,username=username,password=userpass)

        #if user doesnt exists return
        if user is None:
            messages.error(request, 'Invalid credentials, Please try again')
            return redirect(currentPathlogIn)

        else: 
            #?first do the login directly to get the access of database
            #?and the  check for the correctness of usertype
            login(request,user)

            if(int(choice)==1):
                student_obj=Student.objects.all()
                flag=0
                for i in student_obj:
                    if(username==i.username):#if user is actually a student, like he mentioned
                        flag=1
                        break
                if(flag==0):#?if user is not a student,then logout
                    messages.warning(request, 'Please select valid usertype')
                    logout(request)
                    return redirect(currentPathlogIn)

            elif(int(choice)==2):
                startup_obj=Startup.objects.all()
                flag=0
                for i in startup_obj:
                    if(username==i.username):
                        flag=1
                        break
                if(flag==0):
                    messages.warning(request, 'Please select valid usertype')
                    logout(request)
                    return redirect(currentPathlogIn)

            elif(int(choice)==3):
                investor_obj=Investor.objects.all()
                flag=0
                for i in investor_obj:
                    if(username==i.username):
                        flag=1
                        break
                if(flag==0):
                    messages.warning(request, 'Please select valid usertype')
                    logout(request)
                    return redirect(currentPathlogIn)


            messages.success(request, 'Successfully Logged in')
            return redirect(currentPathlogIn)
    return HttpResponse('404 - Not found')




def userLogout(request):
    if request.method=="POST":
        currentPath=request.POST['currentPath']
    logout(request)
    messages.info(request, 'Successfully Logged out')
    return redirect(currentPath)


def startup(request,myid):
    params={}
    startup_object=Startup.objects.get(startup_id=myid)
    params['startup_object']=startup_object
    return render(request,"startup.html",params)


def request(request):
    if request.method == "POST":
        user_type = request.POST.get('user_type', '')
        startup_name = request.POST.get('startup_name', '')
        request_type = request.POST.get('request_type', '')
        description = request.POST.get('description', '')
        specific_link = request.POST.get('specific_link', '')
        startup_obj=Startup.objects.get(username=startup_name)
        finalreq = Request(user_name=request.user,startup_name=startup_obj,user_type=user_type,request_type=request_type,description=description,specific_link=specific_link)
        finalreq.save()
    return redirect("/")


def tracker(request):
    params={}
    try:
        current_user=request.user.username
        student=Student.objects.values('username')
        investor=Investor.objects.values('username')
        startup=Startup.objects.values('username')
        for i in student:
            if(i['username']==current_user):
                params['request1']=Student.objects.filter(username=i['username'])
                params['user_type']=1
                break
        for i in investor:
            if(i['username']==current_user):
                params['request1']=Student.objects.filter(username=i['username'])
                params['user_type']=1
                break
        for i in startup:
            if(i['username']==current_user):
                params['request1']=Student.objects.filter(username=i['username'])
                params['user_type']=1
                break
    except Exception as e:
        print(e)
    # print(student)
    # if(Startup.objects.get(username=request.user)):
    #     params['request1']=Request.objects.filter(user_type=1)
    #     params['request3']=Request.objects.filter(user_type=3)
    #     params['user_type']=2
    # if(Investor.objects.get(username=request.user)):
    #     params['request1']=Request.objects.filter(user_type=3)
    #     params['user_type']=1
    # if(Student.objects.get(username=request.user)):
    print(params)
    
    return render(request,"tracker.html",params)




def profile(request):
    params={}

    if request.method=='POST':
        user_type=request.POST.get("user_type")
        flag=0
        # for investor 
        if(user_type=='3'):
            name = request.user.username     
            phone=request.POST['phone']
            linkedln=request.POST['linkedln']
            description=request.POST['description']

            #validation
            if(len(description)==0):
                messages.warning(request,"Please fill all sections")
                flag=1

            #saving the data
            if(flag==0):
                upload = Investor.objects.get(username = name)
                upload.phone = phone
                upload.linkedln = linkedln
                upload.description = description
                upload.completion_status=1
                upload.save()
                messages.success(request,"Profile updated sucessfully")


        # for student
        elif (user_type=='1'):
                details = Student.objects.all()
                age = request.POST['age']
                area = request.POST['area']
                state = request.POST['state']
                phone = request.POST['phone']
                college = request.POST['college']
                course = request.POST['course']
                description = request.POST['description']
                name = request.user.username
                
                if(len(description)==0):
                    messages.warning(request,"Please fill all sections")
                    flag=1
                
                if(flag==0):
                    upload = Student.objects.get(username = name)
                    upload.age = age
                    upload.area = area
                    upload.state = state
                    upload.phone = phone
                    upload.college = college
                    upload.course = course
                    upload.description = description
                    upload.completion_status=1
                    upload.save()
                    messages.success(request,"Profile updated sucessfully")
                
               
        # startup 
        elif (user_type=='2'):
            tagname = request.POST['tagname']
            about = request.POST['about']
            comapany_type = request.POST['comapany_type']
            market_cap = request.POST['market_cap']
            netsales = request.POST['netsales']
            revenue = request.POST['revenue']
            profit_after_tax = request.POST['profit_after_tax']
            tagprofit_growthname = request.POST['profit_growth']
            company_mission = request.POST['company_mission']
            fund_to_be_raised = request.POST['fund_to_be_raised']
            hiring_details = request.POST['hiring_details']
            job_vacancy = request.POST['job_vacancy']
            website_link = request.POST['website_link']
            linkedin_link = request.POST['linkedin_link']
            twitter_link = request.POST['twitter_link']
            name = request.user.username


            if(len(about)==0):
                messages.warning(request,"Please fill all sections")
                flag=1
                

            if(flag==0):
                upload = Startup.objects.get(username = name)
                upload.tagname = tagname
                upload.about = about
                upload.comapany_type = comapany_type
                upload.market_cap = market_cap
                upload.netsales = netsales
                upload.revenue = revenue
                upload.profit_after_tax = profit_after_tax
                upload.tagprofit_growthname = tagprofit_growthname
                upload.company_mission = company_mission
                upload.fund_to_be_raised = fund_to_be_raised
                upload.hiring_details = hiring_details
                upload.job_vacancy = job_vacancy
                upload.website_link = website_link
                upload.linkedin_link = linkedin_link
                upload.twitter_link = twitter_link
                upload.completion_status=1
                upload.save()
                messages.success(request,"Profile updated sucessfully")




    username=request.user.username
    user_type=0
    #fetching the usertype
    if(len(Student.objects.filter(username=username))>0):
        user_type=1
    elif(len(Startup.objects.filter(username=username))>0):
        user_type=2
    elif(len(Investor.objects.filter(username=username))>0):
        user_type=3


    #sending the current loggedin user to frontend
    if(user_type==1):
        details = Student.objects.all()
        for i in range(len(details)):
            if(details[i].username==request.user.username):
                params["user_object"]= details[i]
                break

    elif(user_type==2):
        details = Startup.objects.all()
        for i in range(len(details)):
            if(details[i].username==request.user.username):
                params["user_object"]= details[i]
                break
    
    elif(user_type==3):
        details = Investor.objects.all()
        for i in range(len(details)):
            if(details[i].username==request.user.username):
                params["user_object"]= details[i]
                break
    
    return render(request,"profile.html",params)




def tracker(request):
        params={}
        if request.user.is_authenticated:


            if request.method == "POST":
                status =0
                table_id = 0
                reject = request.POST.get('reject', '')
                approve = request.POST.get('approve', '')
                if reject == "2" and approve == "":
                    table_id = request.POST.get('table_id', '')
                    status = 2
                elif reject == "" and approve == "1":
                    table_id = request.POST.get('table_id2', '')
                    status = 1
                ty = Request.objects.get(table_id = table_id)
                ty.status = status 
                ty.save()


            user_typ = 0
            data =0
            reqs_list=[]
            reqi_list=[]
            s_list = []
            i_list = []
            c_list = []
            inc_list = []
            if(len(Student.objects.filter(username=request.user))>0):
                user_typ=1
            elif(len(Startup.objects.filter(username=request.user))>0):
                user_typ=2
            elif(len(Investor.objects.filter(username=request.user))>0):
                user_typ=3

            if user_typ == 2:
                startup_name = Startup.objects.get(username= request.user)
                req =  Request.objects.filter(startup_name=startup_name)  
                
                if len(req) > 0:
                    for i in req:
                        
                        if int(i.user_type) == 1:
                            req_t = "Applying for Job" 
                            if i.status ==1:
                                c_list.append([i.user_name,"Student",req_t,i.description,i.table_id])
                            elif i.status ==2:
                                inc_list.append([i.user_name,"Student",req_t,i.description,i.table_id])
                            else:
                                s_list.append([i.user_name,"Student",req_t,i.description,i.table_id])

                            params['c_list'] = c_list
                            params['inc_list'] = inc_list
                            params['s_list'] = s_list
                            params['data']=1
                        
                        if int(i.user_type) == 3:
                            req_t = "Investing" 
                            if i.status == 1:
                                c_list.append([i.user_name,"Investor",req_t,i.description,i.table_id])
                            elif i.status ==2:
                                inc_list.append([i.user_name,"Investor",req_t,i.description,i.table_id])
                            else:
                                i_list.append([i.user_name,"Investor",req_t,i.description,i.table_id])

                            params['c_list'] = c_list
                            params['inc_list'] = inc_list
                            params['i_list'] = i_list
                            params['data']=1
                else:
                     messages.warning(request, 'No request sent')
                     

            elif user_typ== 1:
                req =  Request.objects.filter(user_name=request.user)     
                if len(req) > 0:
                    for i in req:
                        user_t = "Student"
                        req_t = "Applying for Job"  
                        if i.status ==1:
                            c_list.append([i.user_name,user_t,i.startup_name,req_t,i.description,i.table_id])
                        elif i.status ==2:
                            inc_list.append([i.user_name,user_t,i.startup_name,req_t,i.description,i.table_id])
                        else:
                            reqs_list.append([i.user_name,user_t,i.startup_name,req_t,i.description,i.table_id])
                        params['c_list'] = c_list
                        params['inc_list'] = inc_list
                        params['reqs_list'] = reqs_list 
                        params['data']=1
    
                else:
                    messages.warning(request, 'No request sent')

            elif user_typ== 3:
                req =  Request.objects.filter(user_name=request.user)     
                if len(req) > 0:
                    for i in req:
                        user_t = "Investor"
                        req_t = "Investing"    
                        if i.status ==1:
                            c_list.append([i.user_name,user_t,i.startup_name,req_t,i.description,i.table_id])
                        elif i.status ==2:
                            inc_list.append([i.user_name,"Investor",i.startup_name,req_t,i.description,i.table_id])
                        else:
                            reqi_list.append([i.user_name,user_t,i.startup_name,req_t,i.description,i.table_id])

                        params['c_list'] = c_list
                        params['inc_list'] = inc_list
                        params['reqi_list'] = reqi_list 
                        params['data']=1
                else:
                    messages.warning(request, 'No request sent')

            # if request.method == "POST":
            #     status =0
            #     table_id = 0
            #     reject = request.POST.get('reject', '')
            #     approve = request.POST.get('approve', '')
            #     if reject == "2" and approve == "":
            #         table_id = request.POST.get('table_id', '')
            #         status = 2
            #     elif reject == "" and approve == "1":
            #         table_id = request.POST.get('table_id2', '')
            #         status = 1
            #     ty = Request.objects.get(table_id = table_id)
            #     ty.status = status 
            #     ty.save()
                
        
        return render(request,"tracker.html",params)