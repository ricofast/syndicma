from opencourse.institut.models import Classe, Center, Schoolgroup, Academicyear, City, Notification, ParentNotification
from opencourse.profiles.models import Student, LoggedInUser, Professor


def schoolgroupname(request):
    return {'groupename': Schoolgroup.objects.all().first()}


def centername(request):
    return {'center': Center.objects.all().first()}


def academicyearname(request):
    term = request.session.get('term')
    # print(kid)
    if not term:
        acayear = Academicyear.objects.last()
        request.session['term'] = acayear.pk
    else:
        acayear = Academicyear.objects.get(pk=term)

    return {'acayear': acayear}


def academicyearnames(request):
    return {'acayears': Academicyear.objects.all()}


def cityname(request):
    return {'city_name': City.objects.all().first()}


def notificates(request):
    return {'notices': Notification.objects.all()}


def loggedins(request):
    if request.user.is_authenticated:
        if request.user.is_regadmin or request.user.is_superadmin:
            return {'loggedin': LoggedInUser.objects.all()}
        elif request.user.is_parent:
            return {'loggedin': Student.objects.filter(parent=request.user.parent)}
        else:
            return {'loggedin': {}}
    else:
        return {'loggedin': {}}


def notifyStudent(request):
    if request.user.is_authenticated:
        if request.user.is_student:
            return {'pa_notify': ParentNotification.objects.filter(student=request.user.student, studentread=False)}
        elif request.user.is_parent:
            #student = Student.objects.filter(parent=request.user.parent).first()
            notie = ParentNotification.objects.filter(student__parent=request.user.parent, parentread=False)
            print(notie)
            return {'pa_notify': ParentNotification.objects.filter(student__parent=request.user.parent, parentread=False)}
        else:
            return {'pa_notify': {}}
    else:
        return {'pa_notify': {}}


def activestudent(request):
    kid = request.session.get('kid')
    # print(kid)
    if request.user.is_authenticated:
        if request.user.is_parent:
            if not kid:
                kids = Student.objects.filter(parent=request.user.parent).first()
                if kids:
                    kid = kids.pk
                    request.session['kid'] = kid
                    kido = Student.objects.get(pk=kid)
                else:
                    kido = {}
            else:
                kido = Student.objects.get(pk=kid)
        else:
            kido = {}
    else:
        kido = {}


    return {'kid': kido}

# def parentstudents(request):
#     if request.user.is_authenticated:
#         if request.user.is_parent:
#             return {'parentkids': Student.objects.filter(parent=request.user.parent)}
