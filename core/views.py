from django.shortcuts import render, redirect, get_object_or_404
from .models import GeneralUser, Item, Bid
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
            return redirect('/')
        
    
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
    
    currentUser = GeneralUser.objects.get(id = generalUserID)
    currentDateTime = datetime.now()
    items = Item.objects.filter(created_by = currentUser).order_by('-id')
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
    
    generalUserEmail = req.session.get(GENERAL_USER_EMAIL, None)
    generalUserID = req.session.get(GENERAL_USER_ID, None)
    if generalUserEmail == None :
        return render(req, 'login.html')
    

    if req.method == 'POST':
        bidItem = Item.objects.get(id = id)
        bidUser = GeneralUser.objects.get(id = generalUserID)
        bidAmount = req.POST['bidAmount']
        
        bid = Bid()
        bid.item = bidItem
        bid.bid_by = bidUser
        bid.bid_amount = bidAmount
        bid.save()

        return redirect('item-details', id=id)

    currentDateTime = datetime.now()
    item = get_object_or_404(Item, id=id)
    bids = Bid.objects.filter(item = item).order_by('-bid_amount')
    userAlreadyBid = False
    bidWinner = Bid.objects.filter(item = item).order_by('-bid_amount').first()

    for b in bids:
        if b.bid_by.id == generalUserID:
            userAlreadyBid = True
            break
    
    # item = Item.objects.get(id = id)
    data = {
        'userInfo' : {
            'id' : generalUserID,
            'email' : generalUserEmail
        },
        'item' : item,
        'currentDateTime' : currentDateTime,
        'userAlreadyBid' : userAlreadyBid,
        'bids' : bids,
        'bidWinner' : bidWinner
    }
    return render(req, 'core/item-details.html', data)


def itemBidEdit(req, id):
    generalUserEmail = req.session.get(GENERAL_USER_EMAIL, None)
    generalUserID = req.session.get(GENERAL_USER_ID, None)
    if generalUserEmail == None :
        return render(req, 'login.html')
    

    if req.method == 'POST':
        bidID = req.POST['bidID']
        bidAmount = req.POST['bidAmount']
        
        bid = Bid.objects.get(id = bidID)
        bid.bid_amount = bidAmount
        bid.save()

        return redirect('item-details', id=id)
    

def itemDelete(req, id):
    item = get_object_or_404(Item, id=id)
    item.delete()

    return redirect('/my-posted-items')