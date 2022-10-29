from django.shortcuts import render



def financesview(request):
    return render(request, 'finances.html')
