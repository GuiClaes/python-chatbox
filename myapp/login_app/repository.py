from .models import User

class UserRepository():
    def find_user(start):
        return [q.get_username() for q in User.objects.filter(username__startswith=start).all()]