from wallet import views as wv
from user_auth.models import CustomUser 
from wallet.models import Wallet


#def shareCreateWallet(user,currency):
#    try:
#        wallet = wv.Account.Create_Wallet(user,currency)
#        return  True
#    except:
#        return False


def user_query(usernameUser,method_get):
    try:

      user = CustomUser.objects

      match method_get:
        case "get_exits_user":
            get_user = user.filter(username=usernameUser).exists()
          
        case "get_query_username":
            get_user = user.get(username=usernameUser)
        case "get_query_name":
            get_user = user.get(name=usernameUser)
        
      return get_user 
    except:
       raise ""
    

    







