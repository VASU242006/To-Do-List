from django.db.models import query
from django.http import request
from django.shortcuts import render, redirect, HttpResponse
from django.utils import html
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from base.models import TODO
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date
from .tables import TODOTable
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import csv
from django.db.models import Q

# pdf generator
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django_tables2 import RequestConfig


def show_mymodels(request):
    table = TODOTable(TODO.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'base/index_django.html', {'table': table})

def index_django(request):
    if request.user.is_authenticated:
        due_date_dict = {}
        user = request.user
        form = TODOForm()
        totos = TODO.objects.filter(user=user).order_by('end_date')
        # for t in totos:
        # due_date_for_task = t.end_date.day - date.today().day
        # print(str(t.pk) + "==== " + str(due_date_for_task))
        # due_date_dict[t.pk] = due_date_for_task
        table = TODOTable(TODO.objects.filter(user=user).order_by('priority','end_date'))


        print('Table ', table)

        return render(request, "base/index_django.html", context={'form': form, 'table': table, 'totos': totos, 'due_date_dict': due_date_dict, })

    else:
        return redirect('/login')

def history(request):
    if request.user.is_authenticated:
        due_date_dict = {}
        user = request.user
        form = TODOForm()
        totos = TODO.objects.filter(user=user).order_by('end_date')
        # for t in totos:
        # due_date_for_task = t.end_date.day - date.today().day
        # print(str(t.pk) + "==== " + str(due_date_for_task))
        # due_date_dict[t.pk] = due_date_for_task
        table = TODOTable(TODO.objects.filter(user=user).order_by('priority','end_date'))


        print('Table ', table)

        return render(request, "base/history.html", context={'form': form, 'table': table, 'totos': totos, 'due_date_dict': due_date_dict, })

    else:
        return redirect('/login')

def pending(request):
    if request.user.is_authenticated:
        due_date_dict = {}
        user = request.user
        form = TODOForm()
        totos = TODO.objects.filter(user=user,status="P").order_by('end_date')
        # for t in totos:
        # due_date_for_task = t.end_date.day - date.today().day
        # print(str(t.pk) + "==== " + str(due_date_for_task))
        # due_date_dict[t.pk] = due_date_for_task
        table = TODOTable(TODO.objects.filter(user=user,status="P").order_by('priority','end_date'))


        print('Table ', table)

        return render(request, "base/pending.html", context={'form': form, 'table': table, 'totos': totos, 'due_date_dict': due_date_dict, })

    else:
        return redirect('/login')

def complete(request):
    if request.user.is_authenticated:
        due_date_dict = {}
        user = request.user
        form = TODOForm()
        totos = TODO.objects.filter(user=user,status="C").order_by('end_date')
        # for t in totos:
        # due_date_for_task = t.end_date.day - date.today().day
        # print(str(t.pk) + "==== " + str(due_date_for_task))
        # due_date_dict[t.pk] = due_date_for_task
        table = TODOTable(TODO.objects.filter(user=user,status="C").order_by('priority','end_date'))


        print('Table ', table)

        return render(request, "base/complete.html", context={'form': form, 'table': table, 'totos': totos, 'due_date_dict': due_date_dict, })

    else:
        return redirect('/login')



def index(request):
    if request.user.is_authenticated:
        due_date_dict = {}
        user = request.user
        form = TODOForm()
        totos = TODO.objects.filter(user=user).order_by('priority')
        for t in totos:
            due_date_for_task = t.end_date.day - date.today().day
            print(str(t.pk) + "==== " + str(due_date_for_task))
            due_date_dict[t.pk] = due_date_for_task

        return render(request, 'base/index.html', context={'form': form, 'totos': totos, 'due_date_dict': due_date_dict, })
    else:
        # form = AuthenticationForm(request)
        # return render(request, 'base/login.html', context={'form': form})
        return redirect('/login')

def sign_up(request):
    if request.method == 'POST':
        fm = SignUpform(request.POST)
        if fm.is_valid():
            messages.success(request, 'Account Created Successfully')
            fm.save()
            # return render(request, 'base/login.html')
            # return render(request, 'base/home.html')
            return redirect('/login')

    else:
        fm = SignUpform()
    return render(request, 'base/signup.html', {'form': fm})

def login_request(request):
    if request.method == "POST":
        fm = AuthenticationForm(request, data=request.POST)
        if fm.is_valid():
            username = fm.cleaned_data.get('username')
            password = fm.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are logged in as {username}")
                return redirect("/home")
                # return render(request, 'base/home.html')

            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        fm = AuthenticationForm()
       
    return render(request, 'base/login.html', {'form': fm})

def home(request):
    return render(request, 'base/home.html')

def add_todo(request):

    if request.user.is_authenticated:
        user = request.user
        print(user)
        form = TODOForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = user
            todo.save()

            return redirect("/home")

        else:
            messages.info(request, 'Plz enter correct details')
            return redirect("/home")

def signout(request):
    logout(request)
    return render(request, 'base/home.html')

def delete_todo(request, id): 
    print(id)
    TODO.objects.get(pk=id).delete()
    return redirect(request.META.get('HTTP_REFERER'))

def change_todo(request, id, status):
    todo = TODO.objects.get(pk=id)
    todo.status = status
    todo.save()
    return redirect("/home")

def edit_task(request, id):
    todo = TODO.objects.get(pk=id)
    form = TODOForm(instance=todo)

    if request.method == "POST":
        form = TODOForm(request.POST, instance=todo)
        title_task = TODO.objects.get(pk=id)
        if form.is_valid():
            form.save()
            messages.info(request, f"{title_task.title} is updated")
            title_task = TODO.objects.get(pk=id)
            # messages.info(request, f"to {title_task.title} ")
            return redirect("/home")

    return render(request, 'base/edit.html', {'form': form})

def profile(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            u_form=UserUpdateForm(request.POST,instance=request.user)
            if u_form.is_valid():
                u_form.save()
                messages.success(request,f'Your account is updated!')
                return redirect('/home')

        else:
            u_form=UserUpdateForm(instance=request.user) 

    
        return render(request,'base/profile.html',{'u_form':u_form})
    else:
        return redirect('/login')

def view_todo(request, id):
    if request.user.is_authenticated:
        view_todos = TODO.objects.get(pk=id)
        print(view_todos)
        date = view_todos.date

        form = TODOForm(instance=view_todos)
        return render(request, 'base/taskViewing.html', {'form': form, "date": date})

def search_query(request):
    if request.user.is_authenticated:
        user = request.user
        query = request.GET['query']
        if len(query)!=0:
            view_todos = TODO.objects.filter( Q(title__icontains=query) | Q(status__icontains=str(query)) | Q(date__icontains=str(query))| Q(end_date__icontains=str(query)) | Q(priority__icontains=str(query)))
            print(view_todos)
            table = TODOTable(TODO.objects.filter(Q(title__icontains=query) | Q(status__icontains=str(query)) | Q(date__icontains=str(query))| Q(end_date__icontains=str(query))| Q(priority__icontains=str(query)), user=user))
            return render(request, 'base/search.html', {'table': table, 'view_todos': view_todos, 'query': query})
        else:
            messages.error(request,"Not searched anything")
            return redirect('/home')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/home')
        else:
            messages.error(request, 'Please write proper details')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'base/change_password.html', {
        'form': form
    })

def task_details(request, task_id):
    if request.session.has_key('username'):
        login_user = request.session["username"]
        login_user_obj = UserRegister.objects.get(username=login_user)
        print(task_id)
        task_obj = get_object_or_404(TaskData, pk=task_id)
        content = {"login_user_obj": login_user_obj, 'tash_obj': task_obj}
        return render(request, 'app/task_details.html', content)
    else:
        return redirect('user-login')

def venue_pdf(request):
    # Create Bytestream buffer
    buf=io.BytesIO()
    # create canvas
    c=canvas.Canvas(buf,pagesize=letter, bottomup=0)
    #create a text objects
    textob=c.beginText()
    textob.setTextOrigin(inch,15)
    textob.setFont("Helvetica",7)

    #Add some lines of text
    # lines=[
    #     "Cool 1",
    #     "Cool 2",
    #     "Cool 3",
    #     "Cool 4",
    #     "Cool 5",
    # ]
    user=request.user
    venues=TODO.objects.filter(user=user)
    
    lines=[]
    a=[]

    for venue in venues:
        # b=venue.date.day
        # print(a)
        lines.append("Title: "+ venue.title)
        lines.append("Status: "+ venue.status)
        lines.append("Priority: "+ venue.priority)
        lines.append("Username: "+ venue.user.username)
        lines.append("Start Date: "+ str(venue.date))
        lines.append("End Date: "+ str(venue.end_date))
        lines.append(" ")
        lines.append(" ")
    # print(lines)
    #loop
    for line in lines:
        textob.textLine(line)
    #fininshing
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    #return Something
    return FileResponse(buf, as_attachment=True, filename='venue.pdf')

def venue_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=venues.csv'

    #create a csv writer
    writer=csv.writer(response)

    #designate the model
    user=request.user
    venues=TODO.objects.filter(user=user)

    #add column headings to the csv file
    writer.writerow(['Title','Status','Priority','Username','Start Date','End Date'])

    for venue in venues:
        writer.writerow([venue.title,venue.status,venue.priority, venue.user.username,venue.date,venue.end_date])

    return response

