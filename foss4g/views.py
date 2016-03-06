from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

import markdown
import unicodecsv

from symposion.reviews.views import access_not_permitted

from foss4g.proposals.models import TalkProposal


# From https://raw.githubusercontent.com/djangocon/2015.djangocon.us/develop/djangocon/views.py (2016-03-01)
@login_required
def proposal_export(request):
    if not request.user.is_superuser:
        return access_not_permitted(request)

    # Use text/plain mimetype so that we don't get a download dialog
    content_type = 'text/plain'
    response = HttpResponse(content_type=content_type)

    writer = unicodecsv.writer(response, quoting=unicodecsv.QUOTE_ALL)
    writer.writerow([
        'id',
        'title',
        'description',
        'keywords',
        'links'
    ])

    proposals = TalkProposal.objects.all().order_by('id')
    for proposal in proposals:

        if proposal.foss_is_links:
            description = "{}\n\nLinks: {}".format(
                proposal.abstract, proposal.foss_is_links)
        else:
            description = proposal.abstract

        writer.writerow([
            proposal.id,
            proposal.title,
            markdown.markdown(description, extensions=["linkify"]),
            ", ".join([str(tag) for tag in list(proposal.tags.all())]),
        ])
    return response
