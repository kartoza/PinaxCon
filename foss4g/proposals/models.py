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

    foss_is = models.BooleanField(
        default=False,
    )
    foss_is_links = models.TextField(
        verbose_name="Link to project",
        help_text="Please add a link to the source code of your open source project",
        blank=True
    )
    foss_contributing = models.BooleanField(
        default=False,
    )
    foss_contributing_links = models.TextField(
        verbose_name="Link to contributions",
        help_text="Please add links some of the contributions you've made",
        blank=True
    )
    foss_using = models.BooleanField(
        default=False,
    )
    foss_using_links = models.TextField(
        verbose_name="Link to projects",
        help_text="Please add links some of the projects you use",
        blank=True
    )

    class Meta:
        verbose_name = "talk proposal"


class WorkshopProposal(Proposal):

    class Meta:
        verbose_name = "workshop proposal"
