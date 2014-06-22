from django.http import HttpResponse

def index(request):
    return HttpResponse("Oi Andy, você está no index do Poll")

def detail(request, poll_id):
    return HttpResponse("Você está olhando a enquete %s." % poll_id)

def results(request, poll_id):
    return HttpResponse("Você está olhando os resultados da enquete %s." % poll_id)

def vote(request, poll_id):
    return HttpResponse("Você está votando na enquete %s" % poll_id)