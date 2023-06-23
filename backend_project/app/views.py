from django.http import JsonResponse

def connectView(request, db_url):
    return JsonResponse({'db_url': db_url});