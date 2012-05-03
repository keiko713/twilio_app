"""
run 'python -m unittest polls.tests'
"""

import unittest
import mock
from polls import views
from polls import models
from django.conf import settings


class ViewTest(unittest.TestCase):
    @mock.patch('polls.views.render_to_response')
    @mock.patch('polls.models.Poll.objects.all')
    @mock.patch('polls.views.RequestContext')
    def test_index(self, RequestContext, polls, render_to_response):
        request = mock.Mock()
        polls.return_value = []
        views.index(request)
        render_to_response.assert_called_with(
            'index.html', {'polls': []},
            context_instance=RequestContext(request))

    @mock.patch('polls.views.render_to_response')
    @mock.patch('polls.views.get_object_or_404')
    @mock.patch('polls.views.RequestContext')
    def test_view(self, RequestContext, poll, render_to_response):
        request = mock.Mock()
        p = mock.Mock()
        poll.return_value = p

        def all():
            return []

        p.choice_set.all = all
        number = settings.TWILIO_DEFAULT_CALLERID
        views.view(request, None)
        render_to_response.assert_called_with(
            'view.html', {'poll': p, 'choices': [], 'phone_number': number},
            context_instance=RequestContext(request))

    @mock.patch('polls.views.Response.sms')
    @mock.patch('polls.models.Choice.objects.filter')
    @mock.patch('polls.models.VoterChoice.objects.filter')
    def test_phone_vote_error(self, vc, choice, sms):
        """
        Testcase 1: given invalid choice number (String)
        """
        request = mock.Mock()
        request.POST = {
            'Body': 'aaa',
            'From': '1234567890',
        }
        request.REQUEST = request.POST
        views.phone_vote(request)
        message = 'Please text a vote number correctly to vote.'
        sms.assert_called_with(message)

        """
        Testcase 2: given invalid choice number (Not in Choice)
        """
        request = mock.Mock()
        request.POST = {
            'Body': '999',
            'From': '1234567890',
        }
        request.REQUEST = request.POST
        choice.return_value = []
        views.phone_vote(request)
        message = 'Please text a vote number correctly to vote.'
        sms.assert_called_with(message)

    @mock.patch('polls.views.Response.sms')
    @mock.patch('polls.models.Choice.objects.filter')
    @mock.patch('polls.models.VoterChoice.objects.filter')
    def test_phone_vote_sorry(self, vc, choice, sms):
        """
        Testcase 1: try to vote twice in the same poll
        """
        request = mock.Mock()
        request.POST = {
            'Body': '1',
            'From': '1234567890',
        }
        request.REQUEST = request.POST
        c = mock.Mock()
        choice.return_value = [c]
        vc.return_value = [mock.Mock()]
        views.phone_vote(request)
        message = 'Sorry, you have already voted in this poll.' \
            + ' You cannot vote twice.'
        sms.assert_called_with(message)

        """
        Testcase 2: try to vote before it starts
        """
        request = mock.Mock()
        request.POST = {
            'Body': '1',
            'From': '1234567890',
        }
        request.REQUEST = request.POST
        c = mock.Mock()
        poll = mock.Mock()

        def status():
            return 'PENDING'

        poll.status = status
        c.poll = poll
        c.votes = 0
        choice.return_value = [c]
        vc.return_value = []
        views.phone_vote(request)
        message = 'Sorry, your vote is invalid.' \
            + ' This poll has not yet begun.'
        sms.assert_called_with(message)
        self.assertEqual(c.votes, 0)

        """
        Testcase 3: try to vote after it finishes
        """
        request = mock.Mock()
        request.POST = {
            'Body': '1',
            'From': '1234567890',
        }
        request.REQUEST = request.POST
        c = mock.Mock()
        poll = mock.Mock()

        def status():
            return 'FINISHED'

        poll.status = status
        c.poll = poll
        c.votes = 0
        choice.return_value = [c]
        vc.return_value = []
        views.phone_vote(request)
        message = 'Sorry, your vote is invalid.' \
            + ' This poll has already finished.'

    @mock.patch('polls.views.Response.sms')
    @mock.patch('polls.models.Choice.objects.filter')
    @mock.patch('polls.views.VoterChoice.objects.filter')
    @mock.patch('polls.views.VoterChoice')
    def test_phone_vote_success(self, VoterChoice, vc, choice, sms):
        """
        Testcase 1: vote success
        """
        request = mock.Mock()
        request.POST = {
            'Body': '1',
            'From': '1234567890',
        }
        request.REQUEST = request.POST
        c = mock.Mock(spec=models.Choice)
        poll = mock.Mock()

        def status():
            return 'ONGOING'

        poll.status = status
        c.poll = poll
        c.votes = 0
        c.save = mock.Mock()
        choice.return_value = [c]
        vc.return_value = []
        views.phone_vote(request)
        message = 'Thanks for your vote!'
        sms.assert_called_with(message)
        self.assertEqual(c.votes, 1)
