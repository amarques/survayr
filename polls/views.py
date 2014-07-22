from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from polls.models import Choice, Poll


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        """Return the last five published polls.
        (não incluindo os casos que estão com data futura).
        """
        #return Poll.objects.order_by('-pub_date')[:5]
        return Poll.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any polls that aren't published yet.
        """
        return Poll.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'

"""
def index(request):

    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    context = {'latest_poll_list': latest_poll_list}
    return render(request, 'polls/index.html', context)

    #Segundo Exemplo
    #latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
    #template = loader.get_template('polls/index.html')
    #context = RequestContext(request, {
    #    'latest_poll_list': latest_poll_list,
    #})
    #return HttpResponse(template.render(context))

    #Primeiro Exemplo
    #latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
    #output = ', '.join([p.question for p in latest_poll_list])
    #return HttpResponse(output)


def detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/detail.html', {'poll': poll})

    #Segundo Exemplo
    #try:
    #    poll = Poll.objects.get(pk=poll_id)
    #except Poll.DoesNotExist:
    #    raise Http404
    #return render(request, 'polls/detail.html', {'poll':poll})

    #Primeiro Exemplo
    #return HttpResponse("Você está olhando a enquete %s." % poll_id)


def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/results.html', {'poll': poll})

    #Primeiro exemplo
    #return HttpResponse("Você está olhando os resultados da enquete %s." % poll_id)
"""

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        #Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "Você não escolheu nenhuma resposta",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Sempre retorna um HttpResponseRedirect depois de registrar
        # com sucesso um dado do POST. Isto prevê que o dado de origem possa ser postado
        # várias vezes se o usuário clicar no Back.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

    #Primeiro Exemplo
    #return HttpResponse("Você está votando na enquete %s" % poll_id)