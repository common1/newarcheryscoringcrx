import abc
from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import gettext_lazy as _

class Worksheet(models.Model):

    name = models.CharField(
        max_length=64,
        null=False,
        unique=True,
        blank=False,
        default="",
        verbose_name=_("Name"),
        help_text=_("format: required, max-64")
    )
    slug = AutoSlugField(
        populate_from='name',
        editable=True
    )
    grid = models.JSONField(default=dict, blank=True)

    def create_grid(self, x, y):
        pass

    def insert_column(self, x):
        pass

    def insert_row(self, y):
        pass

    def delete_column(self):
        pass

    class Meta:
        db_table = 'worksheets'
        ordering = ['name']
        verbose_name = _("Worksheet")
        verbose_name_plural = _("Worksheets")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Workbook(models.Model):

    name = models.CharField(
        max_length=64,
        null=False,
        unique=True,
        blank=False,
        default="",
        verbose_name=_("Name"),
        help_text=_("format: required, max-64")
    )
    slug = AutoSlugField(
        populate_from='name',
        editable=True
    )

    worksheets = models.ManyToManyField(
        Worksheet,
        blank=True,
        help_text=_("format: not required"),
        verbose_name=_("Worksheets")
    )

    class Meta:
        db_table = 'workbooks'
        ordering = ['name']
        verbose_name = _("Workbook")
        verbose_name_plural = _("Workbooks")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
