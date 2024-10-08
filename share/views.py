from wallet.views import Account


#from user_auth.views import

def first_wallet_created(user):
    bool = Account.first_wallet(user)

    return bool

