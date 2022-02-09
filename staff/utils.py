from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def check_for_admin(user):
    if user.role == "admin":
        return True
    else:
        return False    

def check_for_employee(user):
    if user.role == "employee":
        return True
    else:
        return False


def check_for_doctor(user):
    if user.role == "doctor":
        return True
    else:
        return False



def  paginatorutils(request,object_list,num_of_items):
    page = request.GET.get('page', 1)
    paginator = Paginator(object_list, num_of_items)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return posts                
