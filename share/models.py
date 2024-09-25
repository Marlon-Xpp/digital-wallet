from wallet import views as wv
from user_auth.models import CustomUser 
from wallet.models import Wallet


#def shareCreateWallet(user,currency):
#    try:
#        wallet = wv.Account.Create_Wallet(user,currency)
#        return  True
#    except:
#        return False


def user_instance(username):
    try:
      user = CustomUser.objects.get(username=username)
      return user 
    except:
       raise ""
    
def first_wallet_create():
   try:

   except:    






