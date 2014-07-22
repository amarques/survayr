import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from polls.models import Poll

class PollMethodTests(TestCase):

    # Para criar brakpoins em Python
    #import pdb; pdb.set_trace();

    def test_was_published_recently_with_future_poll(self):
        """
        was_published_recently() deveria retornar False para enquetes com
        pub_date com data futura

        :return: False
        """
        future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(future_poll.was_published_recently(), False)

    def test_was_published_recently_with_old_poll(self):
        """
        was_published_recently() deveria retornar False para enquetes em que
        pub_date é maior que 1 dia

        :return: False
        """
        old_poll = Poll(pub_date=timezone.now() - datetime.timedelta(days=30))
        self.assertEqual(old_poll.was_published_recently(),False)

    def test_was_published_recently_with_recent_poll(self):
        """
        was_published_recently() deve retornar True para enquetes que foram
        publicadas no dia anterior

        :return: True
        """
        recent_poll = Poll(pub_date=timezone.now() - datetime.timedelta(hours=1))
        self.assertEqual(recent_poll.was_published_recently(), True)

def create_poll(question, days):
    """
    Crar uma enquete com a pergunta publicada com um número de dias
    antes de agora (now) [enquetes negativas para enquetes (polls) publicadas
    no passado para enquetes que ainda serão publicadas]
    :param question: Pergunta
    :param days: Número de dias
    :return: Criação da enquete
    """
    return Poll.objects.create(question=question, pub_date=timezone.now() + datetime.timedelta(days=days))


class PollViewTests(TestCase):
    def test_index_view_with_no_polls(self):
        """
        Se a enquete não exisitr, uma mensagem apropriada deve ser exibida
        :return: Mensagem apropriada
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sem enquetes disponíveis")
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_index_view_with_a_past_poll(self):
        """
        Enquetes com a pub_date no passado deveriam ser mostradas no index.
        :return:
        """
        create_poll(question="Enquete antiga.", days=-30)
        create_poll(question="Enquete futura.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Poll: Enquete antiga.>']
        )

    def test_index_view_with_two_past_polls(self):
        """
        Teste com index que devem mostrar múltiplas enquetes
        :return:
        """
        create_poll(question="Enquete antiga 1.", days=-30)
        create_poll(question="Enquete antiga 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        response = self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Poll: Enquete antiga 2.>', '<Poll: Enquete antiga 1.>']
        )

class PollIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_poll(self):
        """
        The detail view of a poll with a pub_date in the future should
        return a 404 not found.
        """
        future_poll = create_poll(question='Future poll.', days=5)
        response = self.client.get(reverse('polls:detail', args=(future_poll.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_poll(self):
        """
        The detail view of a poll with a pub_date in the past should display
        the poll's question.
        """
        past_poll = create_poll(question='Past Poll.', days=-5)
        response = self.client.get(reverse('polls:detail', args=(past_poll.id,)))
        self.assertContains(response, past_poll.question, status_code=200)