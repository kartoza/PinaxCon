from django.db import models

from symposion.proposals.models import ProposalBase


class Proposal(ProposalBase):

    recording_release = models.BooleanField(
        default=True,
        help_text="By submitting your proposal, you agree to give permission to the conference organizers to record, edit, and release audio and/or video of your presentation. If you do not agree to this, please uncheck this box."
    )

    class Meta:
        abstract = True


class TalkProposal(Proposal):

    class Meta:
        verbose_name = "talk proposal"
