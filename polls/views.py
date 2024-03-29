from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from polls.models import Poll, Choice, VoterChoice
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


@twilio_view
def phone_vote(request):
    body = request.POST.get('Body', None)
    from_number = request.POST.get('From', None)
    r = Response()
    message = ''
    if body and body.isdigit():
        choice_id = int(body)
        choice = Choice.objects.filter(id=choice_id)
        if choice:
            c = choice[0]
            vc = VoterChoice.objects.filter(choice__poll=c.poll, phone_number=from_number)
            if vc:
                message = 'Sorry, you have already voted in this poll.' \
                    + ' You cannot vote twice.'
            elif c.poll.status() == 'ONGOING':
                c.votes += 1
                c.save()
                vc_obj = VoterChoice(choice=c, phone_number=from_number)
                vc_obj.save()
                message = 'Thanks for your vote!'
            elif c.poll.status() == 'PENDING':
                message = 'Sorry, your vote is invalid.' \
                    + ' This poll has not yet begun.'
            else:
                message = 'Sorry, your vote is invalid.' \
                    + ' This poll has already finished.'

    if not message:
        message = 'Please text a vote number correctly to vote.'
    r.sms(message)
    return r
