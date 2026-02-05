import base64, string, random, json
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password

from accounts.jwt_tools import generate as generate_jwt, verify as verify_jwt 
from portal.gmail import send_gmail

from .models import Profile, SocialAccount

class Avatar:
    def __init__(self, username = None):
        pass

    def signup(self, request):
        obj_user = None
        # Check user exist
        if User.objects.using("default").filter(username = request["username"]).exists():
            return False, "User already exist"
        if User.objects.using("default").filter(email = request["email"]).exists():
            return False, "User already exist"

        # Create user
        obj_user = User.objects.create(username = request["username"], \
                password = make_password(request["password"]), email = request["email"])
        obj_user.save()

        return True, generate_jwt(obj_user)

    # TODO: OAuth
    def signin(self, request):
        obj_user = None

        # Auth from multiple DB
        if User.objects.using("default").filter(email = request["email"]).exists():
            obj_user = User.objects.using("default").get(email = request["email"])
        # elif User.objects.using("auth_db").filter(username = username).exists():
        #    obj_user = User.objects.using("auth_db").get(username = username)
        else:
            return False, obj_user.username, 403

       # Auth
        obj_user = authenticate(request, username = obj_user.username, password = request["password"])
        if obj_user is not None:
            return True, obj_user.username, generate_jwt(obj_user)
        else:
            return False, "", 403

        # return True, obj_user
        return True, obj_user.username, generate_jwt(obj_user)

    def verify_jwt(self, username, jwt_token):
        # Verify JWT
        jwt_token = jwt_token.replace("Bearer ","")
        result, message = verify_jwt(jwt_token)
        
        return result, message

    def forgot_password(self, request):
        obj_user = None

        # Auth from multiple DB
        if User.objects.using("default").filter(email = request["email"]).exists():
            obj_user = User.objects.using("default").get(email = request["email"])
        else:
            return False, "User does not exist"

        # Make random password
        n = 8
        random_password = ''.join(random.sample(string.ascii_letters + string.digits, n))

        # Set random password to user
        password = make_password(random_password)
        User.objects.filter(email = request["email"]).update(password = password)

        # Send mail
        send_gmail("[小鎮智能] 您的密碼已經變更完成", request["email"], "您好！這是您的新密碼，請儘速登入更改密碼： " + random_password)

        result = True
        content = "OK"

        return result, content

    def get_group(self, request):
        if not User.objects.filter(email = request["email"]).exists():
            return False, "User not exist"

        obj_user = User.objects.get(email = request["email"])

        # Get group list
        query_set_query = Group.objects.all()
        for obj in query_set_query:
            if obj_user.groups.filter(name = obj.name):
                return obj.name

        return "300"

    def set_group(self, request):
        if not User.objects.filter(email = request["email"]).exists():
            return False, "User not exist"

        obj_user = User.objects.get(email = request["email"])

        # Get group list
        if (request["group"] != ""):
            obj_group = Group.objects.get(name = request["group"])
            obj_group.user_set.add(obj_user)
        else:
            obj_user.groups.clear()

        if obj_user.groups.filter(name = request["group"]):
            return obj_group.name
        else:
            return "300"

    def oauth_google(self, request):
        # Verify Google token
        # FIXME: 因為 IT issue ... 暫時關閉 token 驗證
        #result, idinfo = verify_google_token(request["token"])
        ## Workaround
        result = True
        idinfo = ""
        ## Workaround

        if result == False:
            return False, idinfo, ""

        # Signin or create user
        if User.objects.using("default").filter(email = request["email"]).exists():
            obj_user = User.objects.using("default").get(email = request["email"])
        else:
            # Create user
            obj_user = User.objects.create(username = request["username"], email = request["email"])
            obj_user.save()

        # Create SocialAccount forgien key
        if not SocialAccount.objects.filter(obj_users = obj_user, provider = "google").exists():
            obj_social = SocialAccount()
            obj_social.provider = "google"
            obj_social.unique_id = ""
            obj_social.obj_users = obj_user
            obj_social.save()

        return True, obj_user.username, generate_jwt(obj_user)

    def list_accounts(self, request):
        if not User.objects.filter(email = request["email"]).exists():
            return False, "User not exist"

        list_accounts = []
        qs_accounts = list(User.objects.filter(groups__name__in=[request["group"]]))
        for obj in qs_accounts:
            list_accounts.append(obj.email)

        return True, list_accounts

    def delete(self, request):
        if not User.objects.using("default").filter(email = request["email"]).exists():
            return False, "User does not exist"

        obj_user = User.objects.using("default").get(email = request["email"])
        obj_user.delete()

        return True, "OK"

    def oauth_google(self, request):
        # Verify Google token
        # FIXME: 因為 IT issue ... 暫時關閉 token 驗證
        #result, idinfo = verify_google_token(request["token"])
        ## Workaround
        result = True
        idinfo = ""
        ## Workaround

        if result == False:
            return False, idinfo, ""

        # Signin or create user
        if User.objects.using("default").filter(email = request["email"]).exists():
            obj_user = User.objects.using("default").get(email = request["email"])
        else:
            # Create user
            obj_user = User.objects.create(username = request["username"], email = request["email"])
            obj_user.save()

        # Create SocialAccount forgien key
        if not SocialAccount.objects.filter(obj_users = obj_user, provider = "google").exists():
            obj_social = SocialAccount()
            obj_social.provider = "google"
            obj_social.unique_id = ""
            obj_social.obj_users = obj_user
            obj_social.save()

        return True, obj_user.username, generate_jwt(obj_user)
