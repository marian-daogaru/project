from .models import User
import re


def validateForInjections(inputDict):
    """this function will make a string, a nickname, name of group, about me
    valid by removing the special characters {} so we dont have injections. """
    newDict = {}
    for key, value in inputDict.items():
        if type(value) == str:
            newDict[key] =  re.sub('[\{\};]', '', value)
        else:
            newDict[key] = value
    return newDict


class LoginForm(object):
    def __init__(self, inputDict, *args, **kwargs):
        newDict = validateForInjections(inputDict)
        self.email = newDict['email']
        self.password = newDict['password']
        self.rememberMe = newDict['rememberMe']
        self.errors = []

    def validate(self):
        """email check for @ is done by bootstrap.
        length is also checked, but not an issue if we double check"""
        if len(self.email) ==  0 or len(self.password) == 0:
            print("rosu")
            self.errors.append("Missing field.")
            return False
        user = User.query.filter_by(email = self.email).first()
        if user is None:
            self.errors.append("Invalid username / password.")
            print("galben")
            return False
        if user.password != self.password:
            self.errors.append("Invalid username / password.")
            print("portocaliu")
            return False
        print('albastru')
        return True


class SignUpForm():
    def __init__(self, inputDict, *args, **kwargs):
        newDict = validateForInjections(inputDict)
        self.email = newDict['email']
        self.password = newDict['password']
        self.confpwd = newDict['confpwd']
        self.rememberMe = newDict['rememberMe']
        self.errors = []

    def validate(self):
        """email check for @ is done by bootstrap.
        length is also checked, but not an issue if we double check"""
        if len(self.email) ==  0 or len(self.password) == 0 or len(self.confpwd) == 0:
            print("rosu")
            self.errors.append("Missing field.")
            return False
        if User.query.filter_by(email = self.email).first():
            print("galben")
            self.errors.append('Email already registered')
            return False
        if len(self.email) > 30:
            print("beige 22")
            self.errors.append("Email too long.")
            return False
        if len(self.password) > 20 or len(self.password) < 8:
            print("beige")
            self.errors.append("Password not the right dimension. It must be between 8 and 20 chracters long.")
            return False
        if self.password != self.confpwd:
            print("portocaliu")
            self.errors.append('Password not matching')
            return False
        if User.isValidPassword(self.password):
            print("maro")
            self.errors.append('Invalid Passwword.')
            return False
        return True

class EditForm():
    def __init__(self, inputDict, *args, **kwargs):
        newDict = validateForInjections(inputDict)
        self.nickname = newDict['nickname']
        self.aboutMe = newDict['aboutMe']
        self.password = newDict['password']
        self.confpwd =  newDict['confpwd']
        self.avatar = newDict['avatar']
        self.errors = []

    def validate(self):
        if len(self.nickname) ==  0:
            print("rosu")
            self.errors.append("Nickname must be present.")
            return False
        if len(self.nickname) > 30:
            print("rosu 2")
            self.errors.append("Nickname too large.")
            return False
        if self.nickname != User.make_valid_nickname(self.nickname):
            print("mov")
            self.errors.append('This nickname has invalid characters. Please use letters, numbers, dots and underscores only.')
            return False
        if len(self.password) > 0:
            if self.password != self.confpwd:
                self.errors.append('Password not matching')
                return False
            if len(self.password) > 20 or len(self.password) < 8:
                print("beige")
                self.errors.append("Password not the right dimension. It must be between 8 and 20 chracters long.")
                return False
            if self.password != self.confpwd:
                print("portocaliu")
                self.errors.append('Password not matching')
                return False
            if User.isValidPassword(self.password):
                print("maro")
                self.errors.append('Invalid Passwword.')
                return False
        # must do something about the aboutMe, to check it is not injecting stuff
        return True


# ##############################################################################
# GROUP Forms
# ##############################################################################
class GroupCreateForm():
    def __init__(self, inputDict, *args, **kwargs):
        newDict = validateForInjections(inputDict)
        self.name = newDict['name']
        self.aboutGroup = newDict['aboutGroup']
        self.errors = []
    def validate(self):
        if len(self.name) == 0:
            # this is already checked by browser
            self.errors.append("Name must be present!")
            return False
        if len(self.name) > 30:
            self.errors.append("Name too long.")
            return False
        if len(self.aboutGroup) > 200:
            self.errors.append("""The about section is too long.
                                  Max 200 characters.
                                  Currently {} long.""".format(len(self.aboutGroup)))
            return False
        return True

class EditGroupForm():
    def __init__(self, inputDict, *args, **kwargs):
        newDict = validateForInjections(inputDict)
        self.name = newDict['name']
        self.aboutGroup = newDict['aboutGroup']
        self.errors = []

    def validate(self):
        if len(self.name) == 0:
            # this is already checked by browser
            self.errors.append("Name must be present!")
            return False
        if len(self.name) > 30:
            self.errors.append("Name too long.")
            return False
        if len(self.aboutGroup) > 200:
            self.errors.append("""The about section is too long.
                                  Max 200 characters.
                                  Currently {} long.""".format(len(self.aboutGroup)))
            return False
        return True


class PeopleGroupForm():
    def __init__(self, inputDict, *args, **kwargs):
        newDict = validateForInjections(inputDict)
        self.emails = str(newDict['emails'])
        self.errors = []

    def validate(self):
        comp = re.compile(r"^[-A-Za-z0-9_\s\.,@]*$")
        if not bool(comp.match(self.emails)):
            self.errors.append("The field contains characters that are not permitted. \n ")
            self.errors.append("The only permitted characters are Letters, Numbers, '@', Space, '_', '-', '.', ','.")
            return False
        isValid, self.emails = self.validateCorrectEmails()
        if not isValid:
            self.errors.append("This email is not correct: {}".format(self.emails[0]))
            return False
        return True

    def validateCorrectEmails(self):
        text = self.emails
        text = text.replace(",", " ")
        emails = text.split()
        if len(emails) == 0:
            return True, []

        for email in emails:
            if "@" not in email:
                return False, [email]
            parts = email.split("@")
            if "." not in parts[1]:
                return False, [email]
            if len(parts[1].split('.')[0]) == 0:
                return False, [email]

        return True, emails


class RestaurantAddForm():
    def __init__(self, inputDict, *args, **kwargs):
        newDict = validateForInjections(inputDict)
        self.url = newDict['restaurantURL']
        self.originalURL = inputDict['restaurantURL']
        self.errors = []

    def validate(self):
        if self.url != self.originalURL:
            self.errors.append('Invalid URL.')
            return False
        return True
