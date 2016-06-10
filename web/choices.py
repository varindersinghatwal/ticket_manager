from django.utils.translation import ugettext_lazy as _

CATEGORY_CHOICES = (
    ('D', _("Desktop")),
    ('W', _("Web")),
    ('M', _("Mobile"))
)
PRIORITY_CHOICES = (
    ('H', _("High")),
    ('M', _("Medium")),
    ('L', _("Low"))
)
ASSIGNEE_CHOICES = (
    (1, _("Varinder")),
    (2, _("Varun")),
    (3, _("Jugal")),
    (4, _("Kunal"))
)

STATUS_CHOICES = (
    ('OP', _("Open")),
    ('IP', _("In progress")),
    ('RE', _("Reopened")),
    ('RS', _("Resolved")),
    ('CL', _("Close"))
)
