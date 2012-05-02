from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext, Context, loader
from polls.models import Poll, Choice
from twilio.twiml import Response
from django_twilio.decorators import twilio_view
from django.conf import settings

def index(request):
    polls = Poll.objects.all()
    return render_to_response('index.html', {
        'polls': polls,
    }, context_instance=RequestContext(request))

def view(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choices = poll.choice_set.all()
    phone_number = settings.TWILIO_DEFAULT_CALLERID
    return render_to_response('view.html', {
        'poll': poll,
        'choices': choices,
        'phone_number': phone_number,
    }, context_instance=RequestContext(request))

def web_vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choices = poll.choice_set.all()
    return render_to_response('web_vote.html', {
        'poll': poll,
        'choices': choices,
    }, context_instance=RequestContext(request))

def vote(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    choice.votes += 1
    choice.save()
    return HttpResponseRedirect(reverse('polls.views.view', args=(choice.poll.id,)))


@twilio_view
def phone_vote(request):
    body = request.POST.get('Body', None)
    r = Response()
    message = ''
    if body and body.isdigit():
        choice_id = int(body)
	choice = Choice.objects.filter(id=choice_id)
	if choice:
            c = choice[0]
            if c.poll.status == 'ONGOING':
                c.votes += 1
                c.save()
                message = 'Thanks for your vote!'
            elif c.poll.status == 'PENDING':
                message = 'Sorry, your vote is invalid. This poll has not yet begun.'
            else:
                message = 'Sorry, your vote is invalid. This poll has already finished.'

    if not message:
        message = 'Please text a vote number correctly to vote.'
    r.sms(message)
    return r
