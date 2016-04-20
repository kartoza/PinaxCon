from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

import markdown
import unicodecsv

from symposion.reviews.views import access_not_permitted

from foss4g.proposals.models import TalkProposal
from symposion.reviews.models import Review


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
    ])

    proposals = TalkProposal.objects.all().filter(cancelled=0).order_by('id')
    for proposal in proposals:
        description = proposal.abstract
        if proposal.foss_is_links:
            description += "\n\nLinks: " + proposal.foss_is_links

        writer.writerow([
            proposal.id,
            proposal.title,
            markdown.markdown(description, extensions=["linkify"]),
            ", ".join([str(tag) for tag in list(proposal.tags.all())]),
        ])
    return response


def calc_score(result):
    '''Returns the score

    The score is weighted equally. It's 4 points for +1, 3 points for +0,
    2 points for -0 and 1 point for -1. Then it's devided by the number
    of votes.
    '''
    if result.vote_count:
        return ((4 * result.plus_one + 3 * result.plus_zero +
                2 * result.minus_zero + 1 * result.minus_one) /
                float(result.vote_count))
    else:
        return 0


@login_required
def review_export(request):
    if not request.user.is_superuser:
        return access_not_permitted(request)

    # Use text/plain mimetype so that we don't get a download dialog
    content_type = 'text/plain'
    response = HttpResponse(content_type=content_type)

    writer = unicodecsv.DictWriter(
        response, quoting=unicodecsv.QUOTE_ALL,
        fieldnames=['rank', 'score', 'id', 'title', 'abstract', 'tags', 'comments',
                    'speaker', 'companies', 'additional', 'project', 'using',
                    'contributing', 'additional_notes'])
    writer.writeheader()

    queryset = TalkProposal.objects.all().filter(cancelled=0).select_related(
        "result", "speaker")
    results = []
    for proposal in queryset:
        reviews = Review.objects.filter(proposal=proposal)
        comments = [review.comment for review in reviews if review.comment]
        additional_speakers = []
        companies = set([proposal.speaker.company])
        for speaker in proposal.additional_speakers.all():
            additional_speakers.append(speaker.name)
            companies.add(speaker.company)
        results.append({
                'score': calc_score(proposal.result),
                'id': proposal.id,
                'title': proposal.title,
                'abstract': proposal.abstract,
                'tags': ", ".join([
                        str(tag) for tag in list(proposal.tags.all())]),
                'comments': '\n'.join(comments),
                'speaker': proposal.speaker,
                'companies':  ', '.join(companies),
                'additional': ', '.join(additional_speakers),
                'project': proposal.foss_is_links,
                'using': proposal.foss_using_links,
                'contributing': proposal.foss_contributing_links,
                'additional_notes': proposal.additional_notes})

    results.sort(key=lambda k: k['score'], reverse=True)
    for rank, result in enumerate(results):
        result['rank'] = rank + 1
        writer.writerow(result)

    return response
