from django.shortcuts import render, redirect
from .models import GeneralUser
from .helper import GENERAL_USER_EMAIL, GENERAL_USER_ID
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
        data = {
            'userInfo' : {
                'id' : generalUserID,
                'email' : generalUserEmail
            }
        }
        return render(req, 'core/index.html', data)
    else:
        return render(req, 'login.html')
    

def logout(req):

    del req.session[GENERAL_USER_EMAIL]
    del req.session[GENERAL_USER_ID]
    return redirect("/")