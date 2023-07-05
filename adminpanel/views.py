from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from core.models import Item, Bid
from datetime import datetime
from django.db.models import Count, Max, Sum
# Create your views here.


def loginView(req):
    if req.user.is_authenticated:
        return redirect('dashboard')
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']

        userInfo = User.objects.filter(username = username)
        if not userInfo.exists:
            return render(req, 'admin-login.html')
        
        userInfo = authenticate(username = username, password = password)
        if userInfo :
            login(req, userInfo)
            return redirect('dashboard')
    return render(req, 'admin-login.html')


@login_required
def logoutUser(req):
    logout(req)
    return redirect('/admin')

@login_required
def dashboard(req):

    currentDateTime = datetime.now()
    runningAuctionItemCount = Item.objects.filter(auction_end_datetime__gt=currentDateTime).aggregate(count=Count('id'))
    
    runningAuctions = Item.objects.filter(auction_end_datetime__gt=currentDateTime)
    highestBid = Bid.objects.filter(item__in=runningAuctions).values('item').annotate(max_bid=Max('bid_amount'))

    totalValue = highestBid.aggregate(total_value=Sum('max_bid'))
    print(totalValue)
    data = {
        'runningAuctionItemCount' : runningAuctionItemCount['count'],
        'totalBidValue' : totalValue['total_value']
    }

    return render(req, 'adminpanel/dashboard.html', data)


@login_required
def showGallery(req):

    currentDateTime = datetime.now()
    items = Item.objects.all().order_by('-id')
    data = {
        'items' : items,
        'currentDateTime' : currentDateTime
    }
    return render(req, 'adminpanel/auction-gallery.html', data)


@login_required
def itemDetails(req, id):

    currentDateTime = datetime.now()
    item = get_object_or_404(Item, id=id)
    bids = Bid.objects.filter(item = item).order_by('-bid_amount')
    bidWinner = Bid.objects.filter(item = item).order_by('-bid_amount').first()

    
    # item = Item.objects.get(id = id)
    data = {
        
        'item' : item,
        'currentDateTime' : currentDateTime,
        'bids' : bids,
        'bidWinner' : bidWinner
    }
    return render(req, 'adminpanel/item-details.html', data)
