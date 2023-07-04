from django.shortcuts import render, redirect
from .models import GeneralUser, Item
from .helper import GENERAL_USER_EMAIL, GENERAL_USER_ID
from .forms import NewItemForm
from datetime import datetime
import copy
# Create your views here.

def index(req):

    generalUserEmail = req.session.get(GENERAL_USER_EMAIL, None)
    generalUserID = req.session.get(GENERAL_USER_ID, None)
    if req.method == 'POST':
        email = req.POST['email']
        # print(email)
        userInfo = GeneralUser.objects.filter(email = email)
        
        if len(userInfo) == 0:
            newGeneralUser = GeneralUser(email = email)
            newGeneralUser.save()
            req.session[GENERAL_USER_EMAIL] = email
            req.session[GENERAL_USER_ID] = newGeneralUser.id
            return redirect("/")

        req.session[GENERAL_USER_EMAIL] = email
        req.session[GENERAL_USER_ID] = userInfo[0].id
        return redirect("/")

    elif generalUserEmail != None :
        
        currentDateTime = datetime.now()
        items = Item.objects.all().order_by('-id')
        data = {
            'userInfo' : {
                'id' : generalUserID,
                'email' : generalUserEmail
            },
            'items' : items,
            'currentDateTime' : currentDateTime
        }
        return render(req, 'core/index.html', data)
    else:
        return render(req, 'login.html')
    


def logout(req):

    del req.session[GENERAL_USER_EMAIL]
    del req.session[GENERAL_USER_ID]
    return redirect("/")



def create(req):
    if req.method == 'POST':
        form = NewItemForm(req.POST, req.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            generalUser = GeneralUser.objects.get(id = req.session.get(GENERAL_USER_ID, None))
            item.created_by = generalUser
            item.save()
            return redirect('/', pk=item.id)
        
    
    form = NewItemForm()
    generalUserEmail = req.session.get(GENERAL_USER_EMAIL, None)
    generalUserID = req.session.get(GENERAL_USER_ID, None)
    if generalUserEmail == None : 
        return render(req, 'login.html')
    
    data = {
            'userInfo' : {
                'id' : generalUserID,
                'email' : generalUserEmail
            },

            'form': form
        }
    return render(req, 'core/create-item.html', data)


def showMyItems(req):
    generalUserEmail = req.session.get(GENERAL_USER_EMAIL, None)
    generalUserID = req.session.get(GENERAL_USER_ID, None)

    if generalUserEmail == None : 
        return render(req, 'login.html')
    
    currentDateTime = datetime.now()
    currentUser = GeneralUser.objects.get(id = generalUserID)
    currentDateTime = datetime.now()
    items = Item.objects.filter(created_by = currentUser)
    data = {
        'userInfo' : {
            'id' : generalUserID,
            'email' : generalUserEmail
        },
        'items' : items,
        'currentDateTime' : currentDateTime
    }
    return render(req, 'core/my-items.html', data)

        
    

def itemDetails(req, id):
    print(id)
    generalUserEmail = req.session.get(GENERAL_USER_EMAIL, None)
    generalUserID = req.session.get(GENERAL_USER_ID, None)
    if generalUserEmail == None :
        return render(req, 'login.html')
    
    currentDateTime = datetime.now()
    currentUser = GeneralUser.objects.get(id = generalUserID)
    currentDateTime = datetime.now()
    items = Item.objects.filter(created_by = currentUser)
    data = {
        'userInfo' : {
            'id' : generalUserID,
            'email' : generalUserEmail
        },
        'items' : items,
        'currentDateTime' : currentDateTime
    }
    return render(req, 'core/item-details.html', data)
