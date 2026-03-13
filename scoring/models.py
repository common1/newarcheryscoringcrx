import uuid
from django import forms
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from django.core.validators import MaxValueValidator, MinValueValidator

from custom_user.models import User

from modelcluster.models import ClusterableModel

from django.contrib.contenttypes.fields import GenericRelation
from wagtail.admin.panels import PublishingPanel
from wagtail.models import (
    DraftStateMixin, 
    RevisionMixin, 
    LockableMixin,
    PreviewableMixin,
)
from wagtail.snippets.models import register_snippet
from wagtail.admin.ui.tables import BooleanColumn
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from wagtail.images import get_image_model_string

from wagtail.admin.panels import (
    FieldPanel,
    HelpPanel,
    MultiFieldPanel,
    InlinePanel,
    PageChooserPanel,
    FieldRowPanel,
    MultipleChooserPanel,
    TitleFieldPanel,
)
from wagtail.fields import RichTextField

from coderedcms.models import (
    CoderedArticlePage,
    CoderedArticleIndexPage,
    CoderedEmail,
    CoderedFormPage,
    CoderedWebPage,
    CoderedEventIndexPage,
    CoderedEventOccurrence,
    CoderedLocationIndexPage,
    CoderedLocationPage,
)

from website.models import FormPage

class BaseScoringModel(ClusterableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

# TODO: models - Begin

class Archer(BaseScoringModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    last_name = models.CharField(
        max_length=64,
        null=False,
        unique=False,
        blank=False,
        verbose_name=_("Last name"),
        help_text=_("format: required, max-64")
    )
    first_name = models.CharField(
        max_length=32,
        null=False,
        unique=False,
        blank=False,
        verbose_name=_("First name"),
        help_text=_("format: required, max-32")
    )
    middle_name = models.CharField(
        max_length=6,
        null=True,
        unique=False,
        blank=True,
        verbose_name=_("Middle name"),
        help_text=_("format: not required, max-6")
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        editable=True,
        unique=False,
        verbose_name=_("Birth date"),
        help_text=_("format: Y-m-d, not required"),
    )
    image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Archer Image"),
    )
    slug = AutoSlugField(populate_from='last_name',editable=True)
    union_number = models.PositiveIntegerField(
        unique=True,
        null=True,
        blank=False,
        verbose_name=_("Union number"),
        help_text=_("format: not required")
    )
    info = models.TextField(
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Info"),
        help_text=_("format: not required"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        default=1,
        verbose_name=_("Author"),
        related_name='archer_author',
        help_text=_("format: not required, default=1 (superuser)"),
    )
    email = models.EmailField(
        max_length=254,
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Email"),
        help_text=_("format: not required, max-254")
    )
    phone = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Phone number"),
        help_text=_("format: not required, max-15")
    )
    address = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Address"),
        help_text=_("format: not required, max-128")
    )
    city = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("City"),
        help_text=_("format: not required, max-64")
    )
    zip_code = models.CharField(
        max_length=6,
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Zip code"),
        help_text=_("format: not required, max-6")
    )
    province = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Province"),
        help_text=_("format: not required, max-64")
    )
       
    class Meta:
        db_table = 'archers'
        ordering = ['last_name']
        verbose_name = _("Archer")
        verbose_name_plural = _("Archers")

    def __str__(self):
        s_middle_name = ""
        if self.middle_name:
            s_middle_name = self.middle_name
        return f"{self.last_name} {self.first_name} {s_middle_name}"

    def __unicode__(self):
        s_middle_name = ""
        if self.middle_name:
            s_middle_name = self.middle_name
        return f"{self.last_name} {self.first_name} {s_middle_name}"   

class Discipline(BaseScoringModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    name = models.CharField(
        max_length=64,
        null=False,
        unique=True,
        blank=False,
        verbose_name=_("Name"),
        help_text=_("format: required, max-64")
    )
    slug = AutoSlugField(
        populate_from='name',
        editable=True
    )
    archers = models.ManyToManyField(
        Archer,
        through='DisciplineMembership',
        blank=True,
        help_text=_("format: not required"),
        related_name='discipline_archers',
        verbose_name=_("Archers"),
    )
    info = models.TextField(
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Info"),
        help_text=_("format: not required"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        default=1,
        related_name='discipline_author',
        verbose_name=_("Author"),
        help_text=_("format: required, default=1 (superuser)"),
    )

    class Meta:
        db_table = 'disciplines'
        ordering = ['name']
        verbose_name = _("Discipline")
        verbose_name_plural = _("Disciplines")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class DisciplineMembership(BaseScoringModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
        unique=False,
        verbose_name=_("Discipline"),
        help_text=_("format: required"),
        related_name='disciplinememberships'
    )
    archer = models.ForeignKey(
        Archer,
        on_delete=models.PROTECT,
        unique=False,
        verbose_name=_("Archer"),
        help_text=_("format: required"),
        related_name='archer_disciplinemembership'
    )
    slug = AutoSlugField(populate_from=('archer__last_name', 'discipline__name'), editable=True)
    info = models.TextField(
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Info"),
        help_text=_("format: not required"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        default=1,
        related_name='discipline_membership_author',
        verbose_name=_("Author"),
        help_text=_("format: required, default=1 (superuser)"),
    )

    class Meta:
        db_table = 'disciplinememberships'
        ordering = ['discipline__name']
        verbose_name = _("Discipline Membership")
        verbose_name_plural = _("Discipline Memberships")

    def __str__(self):
        return f"{str(self.archer)} - {str(self.discipline)}"

    def __unicode__(self):
        return f"{str(self.archer)} - {str(self.discipline)}"

class Club(BaseScoringModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self._meta.get_field('slug').populate_from = 'name'

    name = models.CharField(
        max_length=64,
        null=False,
        unique=False,
        blank=False,
        verbose_name=_("Name"),
        help_text=_("format: required, max-64")
    )
    slug = AutoSlugField(populate_from='name',editable=True)
    address = models.CharField(
        max_length=128,
        null=True,
        unique=False,
        blank=True,
        verbose_name=_("Address"),
        help_text=_("format: not required, max-128")
    )
    zip_code = models.CharField(
        max_length=6,
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Zip code"),
        help_text=_("format: not required, max-6")
    )
    town = models.CharField(
        max_length=64,
        null=True,
        unique=False,
        blank=True,
        verbose_name=_("Town"),
        help_text=_("format: not required, max-64")
    )
    archers = models.ManyToManyField(
        Archer,
        through='ClubMembership',
        blank=True,
        help_text=_("format: not required"),
        related_name='clubs',
        verbose_name=_("Archers"),
    )
    info = models.TextField(
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Info"),
        help_text=_("format: not required"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        default=1,
        related_name='author_club',
        verbose_name=_("Author"),
        help_text=_("format: not required, default=1 (superuser)"),
    )
    email = models.EmailField(
        max_length=254,
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Email"),
        help_text=_("format: not required, max-254")
    )
    phone = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Phone number"),
        help_text=_("format: not required, max-15")
    )
    website = models.URLField(
        max_length=200,
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Website"),
        help_text=_("format: not required, max-200")
    )
    social_media = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Social media"),
        help_text=_("format: not required, max-128")
    )

    class Meta:
        db_table = 'clubs'
        ordering = ['name']
        verbose_name = _("Club")
        verbose_name_plural = _("Clubs")

    def __str__(self):
        return self.name

    def __unicode__(self):       
        return self.name

class ClubMembership(BaseScoringModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        unique=False,
        verbose_name=_("Club"),
        help_text=_("format: required"),
        related_name='memberships'
    )
    archer = models.ForeignKey(
        Archer,
        on_delete=models.PROTECT,
        unique=False,
        verbose_name=_("Archer"),
        help_text=_("format: required"),
        related_name='clubmember_archer'
    )
    slug = AutoSlugField(populate_from=('archer__last_name', 'club__name'), editable=True)
    start_date = models.DateField(
        null=True,
        blank=True,
        editable=True,
        unique=False,
        verbose_name=_("Start date"),
        help_text=_("format: Y-m-d, not required"),
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        editable=True,
        unique=False,
        verbose_name=_("End date"),
        help_text=_("format: Y-m-d, not required"),
    )
    info = models.TextField(
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Info"),
        help_text=_("format: not required"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        default=1,
        related_name='membership_author',
        verbose_name=_("Author"),
        help_text=_("format: required, default=1 (superuser)"),
    )

    # Extra fields for membership information end

    class Meta:
        db_table = 'clubmemberships'
        ordering = ['start_date']
        verbose_name = _("Club Membership")
        verbose_name_plural = _("Club Memberships")

    def __str__(self):
        return f"{str(self.archer)} - {str(self.club)} {self.club.town}"

    def __unicode__(self):
        return f"{str(self.archer)} - {str(self.club)} {self.club.town}"

class Category(BaseScoringModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    name = models.CharField(
        max_length=64,
        null=False,
        unique=False,
        blank=False,
        verbose_name=_("Name"),
        help_text=_("format: required, max-64")
    )
    slug = AutoSlugField(populate_from='name',editable=True)
    archers = models.ManyToManyField(
        Archer,
        through='CategoryMembership',
        blank=True,
        help_text=_("format: not required"),
        related_name='category_archers',
        verbose_name=_("Archers"),
    )
    info = models.TextField(
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Info"),
        help_text=_("format: not required"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        default=1,
        verbose_name=_("Author"),
        related_name='category_author',
        help_text=_("format: required, default=1 (superuser)"),
    )
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class AgeGroup(BaseScoringModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    name = models.CharField(
        max_length=32,
        null=False,
        unique=True,
        blank=False,
        verbose_name=_("Name"),
        help_text=_("format: required, max-32")
    )
    from_year = models.PositiveIntegerField(
        unique=False,
        null=True,
        blank=True,
        verbose_name=_("From year"),
        help_text=_("format: not required")
    )
    until_year = models.PositiveIntegerField(
        unique=False,
        null=True,
        blank=True,
        verbose_name=_("Until year"),
        help_text=_("format: not required")
    )
    agegroups = models.ManyToManyField(
        "self",
        blank=True,
        help_text=_("format: not required"),
        verbose_name=_("Other allowed AgeGroups"),
    )

    slug = AutoSlugField(populate_from='name',editable=True)
    info = models.TextField(
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Info"),
        help_text=_("format: not required"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        default=1,
        related_name='agegroup_author',
        verbose_name=_("Author"),
        help_text=_("format: required, default=1 (superuser)"),
    )

    class Meta:
        db_table = 'agegroups'
        ordering = ['name']
        verbose_name = _("Age Group")
        verbose_name_plural = _("Age Groups")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class CategoryMembership(BaseScoringModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        unique=False,
        verbose_name=_("Category"),
        help_text=_("format: required"),
        related_name='categorymembership_category_items'
    )
    archer = models.ForeignKey(
        Archer,
        on_delete=models.PROTECT,
        unique=False,
        verbose_name=_("Archer"),        
        related_name='categorymembership_archer_items',
        help_text=_("format: required"),
    )
    agegroup = models.ForeignKey(
        AgeGroup,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Age Group"),
        related_name='categorymembership_agegroup',
        help_text=_("format: required"),
    )

    # Extra fields for membership information

    slug = AutoSlugField(populate_from=('category__name', 'archer__last_name',), editable=True)
    info = models.TextField(
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Info"),
        help_text=_("format: not required"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        default=1,
        related_name='categorymembership_author',
        verbose_name=_("Author"),
        help_text=_("format: required, default=1 (superuser)"),
    )

    class Meta:
        db_table = 'categorymemberships'
        ordering = ['category__name']
        verbose_name = _("Category Membership")
        verbose_name_plural = _("Category Memberships")

    def __str__(self):
        return f"{str(self.archer)} - {str(self.category)}"

    def __unicode__(self):
        return f"{str(self.archer)} - {str(self.category)}"

class Team(BaseScoringModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self._meta.get_field('slug').populate_from = 'name'

    name = models.CharField(
        max_length=64,
        null=False,
        blank=False,
        unique=False,
        verbose_name=_("Name"),
        help_text=_("format: required, max-64")
    )
    slug = AutoSlugField(populate_from='name', editable=True)
    archers = models.ManyToManyField(
        Archer,
        through='TeamMembership',
        blank=True,
        help_text=_("format: not required"),
        related_name='team_archers',
        verbose_name=_("Archers"),
    )
    info = models.TextField(
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Info"),
        help_text=_("format: not required"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        default=1,
        related_name='team_author',
        verbose_name=_("Author"),
        help_text=_("format: required, default=1 (superuser)"),
    )

    class Meta:
        db_table = 'teams'
        ordering = ['name']
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class TeamMembership(BaseScoringModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        unique=False,
        verbose_name=_("Team"),
        help_text=_("format: required"),
        related_name='teammembership_team'
    )
    archer = models.ForeignKey(
        Archer,
        on_delete=models.PROTECT,
        unique=False,
        verbose_name=_("Archer"),
        help_text=_("format: required"),
        related_name='teammembership_archer'
    )
    slug = AutoSlugField(
        populate_from=('team__name', 'archer__last_name',), 
        editable=True,
    )
    info = models.TextField(
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Info"),
        help_text=_("format: not required"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        default=1,
        related_name='teammembership_author',
        verbose_name=_("Author"),
        help_text=_("format: required, default=1 (superuser)"),
    )

    class Meta:
        db_table = 'teammemberships'
        ordering = ['team__name']
        verbose_name = _("Team Membership")
        verbose_name_plural = _("Team Memberships")

    def __str__(self):
        return f"{str(self.archer)} - {str(self.team)}"

    def __unicode__(self):
        return f"{str(self.archer)} - {str(self.team)}"

class ScoringSheet(BaseScoringModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    name = models.CharField(
        max_length=64,
        null=False,
        unique=False,
        blank=False,
        verbose_name=_("Name"),
        help_text=_("format: required, max-64")
    )
    slug = AutoSlugField(populate_from='name',editable=True)
    columns = models.PositiveIntegerField(
        unique=False,
        null=False,
        blank=False,
        default=3,
        validators=[MinValueValidator(3), MaxValueValidator(20)],
        verbose_name=_("Columns"),
        help_text=_("format: required min-3, max-20")
    )
    rows = models.PositiveIntegerField(
        unique=False,
        null=False,
        blank=False,
        default=10,
        validators=[MinValueValidator(3), MaxValueValidator(20)],
        verbose_name=_("Rows"),
        help_text=_("format: required min-3, max-20")
    )
        
    info = models.TextField(
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Info"),
        help_text=_("format: not required"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        default=1,
        related_name='scoringsheet_author',
        verbose_name=_("Author"),
        help_text=_("format: required, default=1 (superuser)"),
    )
    
    class Meta:
        db_table = 'scoringsheets'
        ordering = ['name']
        verbose_name = _("Scoring Sheet")
        verbose_name_plural = _("Scoring Sheets")

    def __str__(self):
        return f"{self.name} ( rows : {self.rows}, columns : {self.columns} )"

    def __unicode__(self):
        return f"{self.name} ( rows : {self.rows}, columns : {self.columns} )"

class TargetFaceNameChoice(BaseScoringModel):
    ENVIRONMENTS = [
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
    ]
    
    DISCIPLINES = [
        ('Target Archery', 'Target Archery'),
        ('Field Archery', 'Field Archery'),
    ]
    
    TARGETSIZES = [
        ('122 cm', '122 cm'),
        ('80 cm', '80 cm'),
        ('65 cm', '65 cm'),
        ('60 cm', '60 cm'),
        ('50 cm', '50 cm'),
        ('40 cm', '40 cm'),
        ('35 cm', '30 cm'),
        ('30 cm', '30 cm'),
        ('20 cm', '20 cm'),
    ]
    
    KEYFEATURES = [
        ('5-Zone', '5-Zone'),
        ('6-Zone', '6-Zone'),
        ('10-Zone', '10-Zone'),
    ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    name = models.CharField(
        max_length=128,
        null=False,
        unique=True,
        blank=False,
        verbose_name=_("Name"),
        help_text=_("format: required, max-128")
    )
    slug = AutoSlugField(populate_from='name',editable=True)
    environment = models.CharField(
        max_length=32,
        null=False,
        unique=False,
        blank=False,
        choices=ENVIRONMENTS,
        verbose_name=_("Environment"),
        help_text=_("format: required, max-32")
    )
    discipline = models.CharField(
        max_length=32,
        null=False,
        unique=False,
        blank=False,
        choices=DISCIPLINES,
        verbose_name=_("Discipline"),
        help_text=_("format: required, max-32")
    )
    targetsize = models.CharField(
        max_length=32,
        null=False,
        unique=False,
        blank=False,
        choices=TARGETSIZES,
        verbose_name=_("Target size"),
        help_text=_("format: required, max-32")
    )
    keyfeature = models.CharField(
        max_length=32,
        null=False,
        unique=False,
        blank=False,
        choices=KEYFEATURES,
        verbose_name=_("Key feature"),
        help_text=_("format: required, max-32")
    )
    
    info = models.TextField(
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Info"),
        help_text=_("format: not required"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        default=1,
        related_name='targetfacenamechoice_author',
        verbose_name=_("Author"),
        help_text=_("format: required, default=1 (superuser)"),
    )
    
    class Meta:
        db_table = 'targetfacenamechoices'
        ordering = ['name']
        verbose_name = _("Target Face Name Choice")
        verbose_name_plural = _("Target Faces Name Choices")
                   
    def __str__(self):
        return f"{self.name} )"

    def __unicode__(self):
        return f"{self.name} )"  

class TargetFace(BaseScoringModel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
            
    name = models.CharField(
        max_length=64,
        null=False,
        unique=True,
        blank=False,
        verbose_name=_("Name"),
        help_text=_("format: required, max-64")
    )
    slug = AutoSlugField(populate_from='name',editable=True)
    # TODO: Insert image field
    info = models.TextField(
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Info"),
        help_text=_("format: not required"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        default=1,
        related_name='targetface_author',
        verbose_name=_("Author"),
        help_text=_("format: required, default=1 (superuser)"),
    )

    class Meta:
        db_table = 'targetfaces'
        ordering = ['name']
        verbose_name = _("Target Face")
        verbose_name_plural = _("Target Faces")

    def __str__(self):
        return f"{self.name} )"

    def __unicode__(self):
        return f"{self.name} )"

class Round(BaseScoringModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    name = models.CharField(
        max_length=64,
        null=False,
        unique=True,
        blank=False,
        default='',
        verbose_name=_("Name"),
        help_text=_("format: required, max-64")
    )
    slug = AutoSlugField(
        populate_from='name',
        editable=True
    )
    start_date = models.DateField(
        null=True,
        blank=True,
        editable=True,
        unique=False,
        verbose_name=_("Start date"),
        help_text=_("format: Y-m-d, not required"),
    )
    start_time = models.TimeField(
        null=True,
        blank=True,
        editable=True,
        unique=False,
        verbose_name=_("Start time"),
        help_text=_("format: H:M, not required"),
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        editable=True,
        unique=False,
        verbose_name=_("End date"),
        help_text=_("format: Y-m-d, not required"),
    )
    end_time = models.TimeField(
        null=True,
        blank=True,
        editable=True,
        unique=False,
        verbose_name=_("End time"),
        help_text=_("format: H:M, not required"),
    )
    # TODO: Insert location
    archers = models.ManyToManyField(
        Archer,
        through='RoundMembership',
        blank=True,
        help_text=_("format: not required"),
        related_name='round_archers',
        verbose_name=_("Archers"),
    )
    info = models.TextField(
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Info"),
        help_text=_("format: not required"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        default=1,
        related_name='round_author',
        verbose_name=_("Author"),
        help_text=_("format: not required, default=1 (superuser)"),
    )

    class Meta:
        db_table = 'rounds'
        ordering = ['start_date']
        verbose_name = _("Round")
        verbose_name_plural = _("Rounds")

    def __str__(self):
        return self.name

    def __unicode__(self):       
        return self.name

class RoundMembership(BaseScoringModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    round = models.ForeignKey(
        Round,
        on_delete=models.CASCADE,
        unique=False,
        default=1,
        verbose_name=_("Round"),
        help_text=_("format: required"),
        related_name='roundmembership_round'
    )
    archer = models.ForeignKey(
        Archer,
        on_delete=models.CASCADE,
        unique=False,
        verbose_name=_("Archer"),
        help_text=_("format: required"),
        related_name='roundmembership_archer'
    )
    slug = AutoSlugField(
        populate_from=('archer__last_name', 'round__name'), 
        editable=True
    )
    info = models.TextField(
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Info"),
        help_text=_("format: not required"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        default=1,
        related_name='roundmembership_author',
        verbose_name=_("Author"),
        help_text=_("format: required, default=1 (superuser)"),
    )

    class Meta:
        db_table = 'roundmemberships'
        ordering = ['round__name']
        verbose_name = _("Round Membership")
        verbose_name_plural = _("Round Memberships")

    def __str__(self):
        return f"{str(self.archer)} - {str(self.round)}"

    def __unicode__(self):
        return f"{str(self.archer)} - {str(self.round)}"

class Score(BaseScoringModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    round_archer = models.ForeignKey(
        RoundMembership,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        unique=False,
        related_name='score_round_archer',
        verbose_name="Round & Archer,",
        help_text=_("format: required"),
    )
    score = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Score"),
        help_text=_("format: not required")
    )
    number_of_arrows = models.PositiveIntegerField(
        null=False,
        blank=False,
        default=0,
        verbose_name=_("Number of arrows")  ,      
        help_text=_("format: not required"),
    )
    info = models.TextField(
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Info"),
        help_text=_("format: not required"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        default=1,
        related_name='score_author',
        verbose_name=_("Author"),
        help_text=_("format: required, default=1 (superuser)"),
    )

    class Meta:
        db_table = 'scores'
        verbose_name = _("Score")
        verbose_name_plural = _("Scores")

    def __str__(self):
        if self.round_archer:
            return f"{str(self.score)} - {str(self.round_archer.archer)}"
        else:
            return f"{str(self.score)} - No Archer"

    def __unicode__(self):
        if self.round_archer:
            return f"{str(self.score)} - {str(self.round_archer.archer)}"
        else:
            return f"{str(self.score)} - No Archer"

class Competition(BaseScoringModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    name = models.CharField(
        max_length=64,
        null=False,
        unique=True,
        blank=False,
        default='',
        verbose_name=_("Name"),
        help_text=_("format: required, max-64")
    )
    slug = AutoSlugField(
        populate_from='name',
        editable=True
    )
    rounds = models.ManyToManyField(
        Round,
        through='CompetitionMembership',
        blank=True,
        help_text=_("format: not required"),
        related_name='competition_rounds',
        verbose_name=_("Competition rounds"),
    )
    start_date = models.DateField(
        null=True,
        blank=True,
        editable=True,
        unique=False,
        verbose_name=_("Start date"),
        help_text=_("format: Y-m-d, not required"),
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        editable=True,
        unique=False,
        verbose_name=_("End date"),
        help_text=_("format: Y-m-d, not required"),
    )
    info = models.TextField(
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Info"),
        help_text=_("format: not required"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        default=1,
        related_name='competition_author',
        verbose_name=_("Author"),
        help_text=_("format: not required, default=1 (superuser)"),
    )

    class Meta:
        db_table = 'competitions'
        ordering = ['name']
        verbose_name = _("Competitions")
        verbose_name_plural = _("Competitions")

    def __str__(self):
        return self.name

    def __unicode__(self):       
        return self.name

class CompetitionMembership(BaseScoringModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    competition = models.ForeignKey(
        Competition,
        on_delete=models.PROTECT,
        unique=False,
        verbose_name=_("Competition"),
        help_text=_("format: required"),
        related_name='competitionmembership_competition'
    )
    round = models.ForeignKey(
        Round,
        on_delete=models.CASCADE,
        unique=False,
        verbose_name=_("Round"),
        help_text=_("format: required"),
        related_name='competitionmembership_round'
    )
    slug = AutoSlugField(
        populate_from=('competition__name', 'round__name',), 
        editable=True,
    )
    info = models.TextField(
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("Info"),
        help_text=_("format: not required"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        default=1,
        related_name='competitionmembership_author',
        verbose_name=_("Author"),
        help_text=_("format: required, default=1 (superuser)"),
    )

    class Meta:
        db_table = 'competitionmemberships'
        ordering = ['competition__name']
        verbose_name = _("Competition Membership")
        verbose_name_plural = _("Competition Memberships")

    def __str__(self):
        return f"{str(self.competition)} - {str(self.round)}"

    def __unicode__(self):
        return f"{str(self.competition)} - {str(self.round)}"

# TODO: models - End

# TODO: snippets - Begin

class ArcherSnippetViewSet(SnippetViewSet):
    model = Archer
    icon = "arrow-right-full"
    menu_label = "Archers"
    menu_order = 10
    add_to_settings_menu = False
    add_to_admin_menu = False
    list_display = ('last_name', 'first_name', 'middle_name', 'union_number', BooleanColumn('is_active'),)
    list_filter = ('is_active',)
    inspect_view_enabled = True
    copy_view_enabled = True
    history_view_enabled = True
    delete_view_enabled=True

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('last_name'),
                FieldPanel('first_name'),
                FieldPanel('middle_name'),
                FieldPanel('union_number'),
                FieldPanel('birth_date'),
                FieldPanel('image'),
                FieldPanel('info'),
            ],
            heading = "Basic Information",
        ),
        MultiFieldPanel(
            [
                FieldPanel('email'),
                FieldPanel('phone'),
                FieldPanel('address'),
                FieldPanel('city'),
                FieldPanel('zip_code'),
                FieldPanel('province'),
            ],
            heading = "Contact Information",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel('slug'),
                FieldPanel('author'),
            ],
            heading = "Extra Information",
            classname="collapsible collapsed",
        ),
    ]

class DisciplineSnippetViewSet(SnippetViewSet):
    model = Discipline
    menu_label = "Disciplines"
    icon = "list-ul"
    menu_order = 100
    add_to_settings_menu = False
    add_to_admin_menu = False
    list_display = ('name', BooleanColumn('is_active'),)
    list_filter = ('is_active',)
    inspect_view_enabled = True
    copy_view_enabled = True
    history_view_enabled = True
    delete_view_enabled=True

    panels = [
        FieldPanel('name'),
        FieldPanel('info'),
        FieldPanel('archers', widget=forms.CheckboxSelectMultiple),
        MultiFieldPanel(
            [
                FieldPanel('slug'),
                FieldPanel('author'),
            ],
            heading = "Extra Information",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel('is_active'),
            ],
            heading = "Special",
            classname="collapsible collapsed",
        ),
    ]

class DisciplineMembershipSnippetViewSet(SnippetViewSet):
    model = DisciplineMembership
    menu_label = "Discipline Memberships"
    icon = "list-ul"
    menu_order = 110
    add_to_settings_menu = False
    add_to_admin_menu = False
    list_display = ('discipline', 'archer', BooleanColumn('is_active'),)
    list_filter = ('is_active',)
    inspect_view_enabled = True
    copy_view_enabled = True
    history_view_enabled = True
    delete_view_enabled=True

    panels = [
        FieldPanel('discipline'),
        FieldPanel('archer'),
        MultiFieldPanel(
            [
                FieldPanel('slug'),
                FieldPanel('author'),
                FieldPanel('info'),
            ],
            heading = "Extra Information",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel('is_active'),
            ],
            heading = "Special",
            classname="collapsible collapsed",
        ),
    ]

class ClubSnippetViewSet(SnippetViewSet):
    model = Club
    menu_label = "Clubs"
    icon = "home"
    menu_order = 30
    add_to_settings_menu = False
    add_to_admin_menu = False
    list_display = ('name', 'town', BooleanColumn('is_active'),)
    list_filter = ('is_active',)
    inspect_view_enabled = True
    copy_view_enabled = True
    history_view_enabled = True
    delete_view_enabled=True

    panels = [
        FieldPanel('name'),
        FieldPanel('info'),
        FieldPanel('archers', widget=forms.CheckboxSelectMultiple),
        MultiFieldPanel(
            [
                FieldPanel('address'),
                FieldPanel('zip_code'),
                FieldPanel('town'),
                FieldPanel('phone'),
                FieldPanel('email'),
                FieldPanel('website'),
                FieldPanel('social_media'),
            ],
            heading = "Contact Information",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel('slug'),
                FieldPanel('author'),
            ],
            heading = "Extra Information",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel('is_active'),
            ],
            heading = "Special",
            classname="collapsible collapsed",
        ),
    ]

class ClubMembershipSnippetViewSet(SnippetViewSet):
    model = ClubMembership
    menu_label = "Club Memberships"
    icon = "list-ul"
    menu_order = 40
    add_to_settings_menu = False
    add_to_admin_menu = False
    list_display = ('archer', 'club', BooleanColumn('is_active'),)
    list_filter = ('is_active',)
    inspect_view_enabled = True
    copy_view_enabled = True
    history_view_enabled = True
    delete_view_enabled=True

    panels = [
        FieldPanel('club'),
        FieldPanel('archer'),
        MultiFieldPanel(
            [
                FieldPanel('start_date'),
                FieldPanel('end_date'),
            ],
            heading = "Information",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel('slug'),
                FieldPanel('author'),
                FieldPanel('info'),
            ],
            heading = "Extra Information",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel('is_active'),
            ],
            heading = "Special",
            classname="collapsible collapsed",
        ),
    ]

class CategorySnippetViewSet(SnippetViewSet):
    model = Category
    menu_label = "Categories"
    icon = "home"
    menu_order = 50
    add_to_settings_menu = False
    add_to_admin_menu = False
    list_display = ('name', BooleanColumn('is_active'),)
    list_filter = ('is_active',)
    inspect_view_enabled = True
    copy_view_enabled = True
    history_view_enabled = True
    delete_view_enabled=True

    panels = [
        FieldPanel('name'),
        FieldPanel('info'),
        FieldPanel('archers', widget=forms.CheckboxSelectMultiple),
        MultiFieldPanel(
            [
                FieldPanel('slug'),
                FieldPanel('author'),
            ],
            heading = "Extra Information",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel('is_active'),
            ],
            heading = "Special",
            classname="collapsible collapsed",
        ),
    ]

class AgeGroupSnippetViewSet(SnippetViewSet):
    model = AgeGroup
    menu_label = "Age Groups"
    icon = "user"
    menu_order = 20
    add_to_settings_menu = False
    add_to_admin_menu = False
    list_display = ('name', 'from_year', 'until_year', BooleanColumn('is_active'),)
    list_filter = ('is_active',)
    inspect_view_enabled = True
    copy_view_enabled = True
    history_view_enabled = True
    delete_view_enabled=True

    panels = [
        FieldPanel('name'),
        FieldPanel('info'),
        FieldPanel('from_year'),
        FieldPanel('until_year'),
        FieldPanel('agegroups'),
        MultiFieldPanel(
            [
                FieldPanel('slug'),
                FieldPanel('author'),
            ],
            heading = "Extra Information",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel('is_active'),
            ],
            heading = "Special",
            classname="collapsible collapsed",
        ),
    ]

class CategoryMembershipSnippetViewSet(SnippetViewSet):
    model = CategoryMembership
    menu_label = "Category Memberships"
    icon = "list-ul"
    menu_order = 60
    add_to_settings_menu = False
    add_to_admin_menu = False
    list_display = ('category', 'archer', 'agegroup', BooleanColumn('is_active'),)
    list_filter = ('is_active',)
    inspect_view_enabled = True
    copy_view_enabled = True
    history_view_enabled = True
    delete_view_enabled=True

    panels = [
        FieldPanel('category'),
        FieldPanel('archer'),
        FieldPanel('agegroup'),
        FieldPanel('info'),
        MultiFieldPanel(
            [
                FieldPanel('slug'),
                FieldPanel('author'),
            ],
            heading = "Extra Information",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel('is_active'),
            ],
            heading = "Special",
            classname="collapsible collapsed",
        ),
    ]

class TeamSnippetViewSet(SnippetViewSet):
    model = Team
    menu_label = "Teams"
    icon = "group"
    menu_order = 70
    add_to_settings_menu = False
    add_to_admin_menu = False
    list_display = ('name', BooleanColumn('is_active'),)
    list_filter = ('is_active',)
    inspect_view_enabled = True
    copy_view_enabled = True
    history_view_enabled = True
    delete_view_enabled=True

    panels = [
        FieldPanel('name'),
        FieldPanel('info'),
        FieldPanel('archers', widget=forms.CheckboxSelectMultiple),
        MultiFieldPanel(
            [
                FieldPanel('slug'),
                FieldPanel('author'),
            ],
            heading = "Extra Information",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel('is_active'),
            ],
            heading = "Special",
            classname="collapsible collapsed",
        ),
    ]

class TeamMembershipSnippetViewSet(SnippetViewSet):
    model = TeamMembership
    menu_label = "Team Memberships"
    icon = "list-ul"
    menu_order = 80
    add_to_settings_menu = False
    add_to_admin_menu = False
    list_display = ('team', 'archer', BooleanColumn('is_active'),)
    list_filter = ('is_active',)
    inspect_view_enabled = True
    copy_view_enabled = True
    history_view_enabled = True
    history_view_enabled = True
    delete_view_enabled=True

    panels = [
        FieldPanel('team'),
        FieldPanel('archer'),
        FieldPanel('info'),
        MultiFieldPanel(
            [
                FieldPanel('slug'),
                FieldPanel('author'),
            ],
            heading = "Extra Information",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel('is_active'),
            ],
            heading = "Special",
            classname="collapsible collapsed",
        ),
    ]   

class ScoringSheetSnippetViewSet(SnippetViewSet):
    model = ScoringSheet
    menu_label = "Scoring Sheets"
    icon = "doc-full"
    menu_order = 90
    add_to_settings_menu = False
    add_to_admin_menu = False
    list_display = ('name', 'columns', 'rows', BooleanColumn('is_active'),)
    list_filter = ('is_active',)
    inspect_view_enabled = True
    copy_view_enabled = True
    history_view_enabled = True
    delete_view_enabled=True

    panels = [  
        FieldPanel('name'),
        FieldRowPanel([
            FieldPanel('columns'),
            FieldPanel('rows'),            
        ]),
        FieldPanel('info'),
        MultiFieldPanel(
            [
                FieldPanel('slug'),
                FieldPanel('author'),
            ],
            heading = "Extra Information",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel('is_active'),
            ],
            heading = "Special",
            classname="collapsible collapsed",
        ),
    ]

class TargetFaceNameChoiceSnippetViewSet(SnippetViewSet):
    model = TargetFaceNameChoice
    icon = "arrow-right-full"
    menu_label = "Target Face Name Choices"
    menu_order = 110
    add_to_settings_menu = False
    add_to_admin_menu = False
    list_display = ('name', BooleanColumn('is_active'),)
    list_filter = ('is_active',)
    inspect_view_enabled = True
    copy_view_enabled = True
    history_view_enabled = True
    delete_view_enabled=True

    panels = [
        FieldPanel('name'),
        FieldPanel('environment'),
        FieldPanel('discipline'),
        FieldPanel('targetsize'),
        FieldPanel('keyfeature'),
        FieldPanel('info'),
        MultiFieldPanel(
            [
                FieldPanel('slug'),
                FieldPanel('author'),
            ],
            heading = "Extra Information",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel('is_active'),
            ],
            heading = "Special",
            classname="collapsible collapsed",
        ),
    ]

# TODO: TargetFaceSnippetViewSet finish
class TargetFaceSnippetViewSet(SnippetViewSet):
    model = TargetFace

    inspect_view_enabled = True
    copy_view_enabled = True
    history_view_enabled = True
    delete_view_enabled=True

class RoundSnippetViewSet(SnippetViewSet):
    model = Round
    menu_label = "Rounds"
    icon = "list-ul"
    menu_order = 36
    add_to_settings_menu = False
    add_to_admin_menu = False
    list_display = ('name', 'start_date', 'start_time', 'end_date', 'end_time', BooleanColumn('is_active'),)
    ordering = ['start_date']
    list_filter = ('is_active',)
    inspect_view_enabled = True
    copy_view_enabled = True
    history_view_enabled = True
    delete_view_enabled=True

    panels = [
        FieldPanel('name'),
        FieldPanel('start_date'),
        FieldPanel('start_time'),
        FieldPanel('end_date'),
        FieldPanel('end_time'),
        FieldPanel('archers', widget=forms.CheckboxSelectMultiple),
        MultiFieldPanel(
            [
                FieldPanel('slug'),
                FieldPanel('author'),
                FieldPanel('info'),
            ],
            heading = "Extra Information",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel('is_active'),
            ],
            heading = "Special",
            classname="collapsible collapsed",
        ),
    ]

class RoundMembershipSnippetViewset(SnippetViewSet):
    model = RoundMembership
    menu_label = "Round Memberships"
    icon = "list-ul"
    menu_order = 60
    add_to_settings_menu = False
    add_to_admin_menu = False
    list_display = ('round', 'archer', BooleanColumn('is_active'),)
    # ordering = ['round__start_date']
    list_filter = ('is_active', 'round', 'archer')
    inspect_view_enabled = True
    copy_view_enabled = True
    history_view_enabled = True
    delete_view_enabled=True

    panels = [
        FieldPanel('round'),
        FieldPanel('archer'),
        FieldPanel('info'),
        MultiFieldPanel(
            [
                FieldPanel('slug'),
                FieldPanel('author'),
            ],
            heading = "Extra Information",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel('is_active'),
            ],
            heading = "Special",
            classname="collapsible collapsed",
        ),
    ]
    
class ScoreSnippetViewSet(SnippetViewSet):
    model = Score
    icon = "snippet"
    menu_label = "Scores"
    menu_order = 110
    add_to_settings_menu = False
    add_to_admin_menu = False
    list_display = ('round_archer', 'score', 'number_of_arrows', BooleanColumn('is_active'),)
    list_filter = ('is_active',)
    inspect_view_enabled = True
    copy_view_enabled = True
    history_view_enabled = True
    delete_view_enabled=True

    panels = [
        FieldPanel('round_archer'),
        FieldPanel('score'),
        FieldPanel('number_of_arrows'),
        FieldPanel('info'),
        MultiFieldPanel(
            [
                FieldPanel('author'),
            ],
            heading = "Extra Information",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel('is_active'),
            ],
            heading = "Special",
            classname="collapsible collapsed",
        ),
    ]        

class CompetitionSnippetViewSet(SnippetViewSet):
    model = Competition
    menu_label = "Competitions"
    icon = "home"
    menu_order = 32
    add_to_settings_menu = False
    add_to_admin_menu = False
    list_display = ('name', 'start_date', 'end_date', BooleanColumn('is_active'),)
    list_filter = ('is_active',)
    inspect_view_enabled = True
    copy_view_enabled = True
    history_view_enabled = True
    delete_view_enabled=True

    panels = [
        FieldPanel('name'),
        FieldPanel('info'),
        FieldPanel('start_date'),
        FieldPanel('end_date'),
        FieldPanel('rounds', widget=forms.CheckboxSelectMultiple),
        MultiFieldPanel(
            [
                FieldPanel('slug'),
                FieldPanel('author'),
            ],
            heading = "Extra Information",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel('is_active'),
            ],
            heading = "Special",
            classname="collapsible collapsed",
        ),

    ]

class CompetitionMembershipSnippetViewSet(SnippetViewSet):
    model = CompetitionMembership
    menu_label = "Competition Memberships"
    icon = "list-ul"
    menu_order = 34
    add_to_settings_menu = False
    add_to_admin_menu = False
    list_display = ('competition', 'round', BooleanColumn('is_active'),)
    list_filter = ('is_active',)
    inspect_view_enabled = True
    copy_view_enabled = True
    history_view_enabled = True
    delete_view_enabled=True

    panels = [
        FieldPanel('competition'),
        FieldPanel('round'),
        MultiFieldPanel(
            [
                FieldPanel('slug'),
                FieldPanel('author'),
                FieldPanel('info'),
            ],
            heading = "Extra Information",
            classname="collapsible collapsed",
        ),
        MultiFieldPanel(
            [
                FieldPanel('is_active'),
            ],
            heading = "Special",
            classname="collapsible collapsed",
        ),
    ]

class ModelingSnippetViewSetGroup(SnippetViewSetGroup):
    menu_label = "Scoring Snippets"
    menu_icon = "folder-open-inverse"
    menu_order = 100
    items = (
        AgeGroupSnippetViewSet,
        ArcherSnippetViewSet,
        CategorySnippetViewSet,
        CategoryMembershipSnippetViewSet,
        CompetitionSnippetViewSet,
        CompetitionMembershipSnippetViewSet,
        DisciplineSnippetViewSet,
        DisciplineMembershipSnippetViewSet,
        ClubSnippetViewSet,
        ClubMembershipSnippetViewSet,
        RoundSnippetViewSet,
        RoundMembershipSnippetViewset,
        ScoreSnippetViewSet,
        ScoringSheetSnippetViewSet,
        TargetFaceNameChoiceSnippetViewSet,
        TargetFaceSnippetViewSet,
        TeamSnippetViewSet,
        TeamMembershipSnippetViewSet,
    )

register_snippet(ModelingSnippetViewSetGroup)    

# TODO: snippets - End

# TODO: Page models - Begin
        
from coderedcms.models import CoderedWebPage

class ArcherIndexPage(CoderedWebPage):
    """
    Landing page for archers
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.ArcherPage'

    subpage_types = ['scoring.ArcherPage']

    class Meta:
        verbose_name = "Archer Index Page"

    template = "scoring/pages/archer_index_page.html"

class ArcherPage(CoderedWebPage):
    """
    Custom page for individual archers
    """

    class Meta:
        verbose_name = "Archer Page"

    # Only allow this page to be created beneath an ArchersIndexPage.
    parent_page_types = ['scoring.ArcherIndexPage']
    subpage_types = []  # No subpages allowed under ArcherPage
    
    template = "scoring/pages/archer_page.html"

   # Archer Page model fields
    archer = models.ForeignKey(
        'scoring.Archer',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Archer associated with this page (optional, but recommended for proper functionality)",
    )
    description = RichTextField(
        verbose_name="Archer Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('archer'),
        FieldPanel('description'),
    ]

class DisciplineIndexPage(CoderedWebPage):
    """
    Landing page for disciplines
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.DisciplinePage'

    subpage_types = ['scoring.DisciplinePage']

    class Meta:
        verbose_name = "Discipline Index Page"

    template = "scoring/pages/discipline_index_page.html"

class DisciplinePage(CoderedWebPage):
    """
    Custom page for individual disciplines
    """

    class Meta:
        verbose_name = "Discipline Page"

    # Only allow this page to be created beneath a DisciplineIndexPage.
    parent_page_types = ['scoring.DisciplineIndexPage']

    template = "scoring/pages/discipline_page.html"

   # Discipline Page model fields
    discipline = models.ForeignKey(
        'scoring.Discipline',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Discipline associated with this page (optional, but recommended for proper functionality)",
    )
    description = RichTextField(
        verbose_name="Discipline Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('discipline'),
        FieldPanel('description'),
    ]

class ClubIndexPage(CoderedWebPage):
    """
    Landing page for clubs
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.ClubPage'

    subpage_types = ['scoring.ClubPage']

    class Meta:
        verbose_name = "Club Index Page"

    template = "scoring/pages/club_index_page.html"

class ClubPage(CoderedWebPage):
    """
    Custom page for individual clubs
    """

    class Meta:
        verbose_name = "Club Page"

    # Only allow this page to be created beneath a ClubIndexPage.
    parent_page_types = ['scoring.ClubIndexPage']

    template = "scoring/pages/club_page.html"

   # Discipline Page model fields
    club = models.ForeignKey(
        'scoring.Club',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Club associated with this page (optional, but recommended for proper functionality)",
    )
    description = RichTextField(
        verbose_name="Club Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('club'),
        FieldPanel('description'),
    ]

class CategoryIndexPage(CoderedWebPage):
    """
    Landing page for categories
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.CategoryPage'

    subpage_types = ['scoring.CategoryPage']

    class Meta:
        verbose_name = "Category Index Page"

    template = "scoring/pages/category_index_page.html"

class CategoryPage(CoderedWebPage):
    """
    Custom page for individual categories
    """

    class Meta:
        verbose_name = "Category Page"

    # Only allow this page to be created beneath a CategoryIndexPage.
    parent_page_types = ['scoring.CategoryIndexPage']

    template = "scoring/pages/category_page.html"

   # Category Page model fields
    category = models.ForeignKey(
        'scoring.Category',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Category associated with this page (optional, but recommended for proper functionality)",
    )
    description = RichTextField(
        verbose_name="Category Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('category'),
        FieldPanel('description'),
    ]
    
class AgeGroupIndexPage(CoderedWebPage):
    """
    Landing page for age groups
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.AgeGroupPage'

    subpage_types = ['scoring.AgeGroupPage']

    class Meta:
        verbose_name = "Age Group Index Page"

    template = "scoring/pages/agegroup_index_page.html"

class AgeGroupPage(CoderedWebPage):
    """
    Custom page for individual age groups
    """
    class Meta:
        verbose_name = "Age Group Page"

    # Only allow this page to be created beneath an AgeGroupIndexPage.
    parent_page_types = ['scoring.AgeGroupIndexPage']
    subpage_types = []

    template = "scoring/pages/agegroup_page.html"

    age_group = models.ForeignKey(
        'scoring.AgeGroup',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Age group associated with this page (optional, but recommended for proper functionality)",
    )
    description = RichTextField(
        verbose_name="AgeGroup Description",
        null=True,
        blank=True,
        default=""
    )
    photo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Agegroup Photo',
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('age_group'),
        FieldPanel('photo'),
        FieldPanel('description'),
    ]

class TeamIndexPage(CoderedWebPage):
    """
    Landing page for teams
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.TeamPage'

    subpage_types = ['scoring.TeamPage']

    class Meta:
        verbose_name = "Team Index Page"

    template = "scoring/pages/team_index_page.html"

class TeamPage(CoderedWebPage):
    """
    Custom page for individual teams
    """

    class Meta:
        verbose_name = "Team Page"

    # Only allow this page to be created beneath a TeamIndexPage.
    parent_page_types = ['scoring.TeamIndexPage']

    template = "scoring/pages/team_page.html"

    team = models.ForeignKey(
        'scoring.Team',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Team associated with this page (optional, but recommended for proper functionality)",
    )
    description = RichTextField(
        verbose_name="Team Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('team'),
    ]

class ScoringSheetIndexPage(CoderedWebPage):
    """
    Landing page for scoring sheets
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.ScoringSheetPage'

    subpage_types = ['scoring.ScoringSheetPage']

    class Meta:
        verbose_name = "Scoring Sheet Index Page"

    template = "scoring/pages/scoringsheet_index_page.html"

class ScoringSheetPage(CoderedWebPage):
    """
    Custom page for individual scoring sheets
    """

    class Meta:
        verbose_name = "Scoring Sheet Page"

    # Only allow this page to be created beneath a ScoringSheetIndexPage.
    parent_page_types = ['scoring.ScoringSheetIndexPage']

    template = "scoring/pages/scoringsheet_page.html"

    scoring_sheet = models.ForeignKey(
        'scoring.ScoringSheet',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Scoring sheet associated with this page (optional, but recommended for proper functionality)",
    )
    description = RichTextField(
        verbose_name="ScoringSheet Description",
        null=True,
        blank=True,
        default=""
    )
    
    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('scoring_sheet'),
        FieldPanel('description'),
    ]

class TargetFaceNameChoiceIndexPage(CoderedWebPage):
    """
    Landing page for target face name choices
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.TargetFaceNameChoicePage'

    subpage_types = ['scoring.TargetFaceNameChoicePage']

    class Meta:
        verbose_name = "Target Face Name Choice Index Page"

    template = "scoring/pages/targetfacenamechoice_index_page.html"

class TargetFaceNameChoicePage(CoderedWebPage):
    """
    Custom page for individual target face name choices
    """
    target_face_name_choice = models.ForeignKey(
        'scoring.TargetFaceNameChoice',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Target face name choice associated with this page (optional, but recommended for proper functionality)",
    )
    description = RichTextField(
        verbose_name="TargetFaceNameChoice Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('target_face_name_choice'),
        FieldPanel('description'),
    ]

    class Meta:
        verbose_name = "Target Face Name Choice Page"

    # Only allow this page to be created beneath a TargetFaceNameChoiceIndexPage.
    parent_page_types = ['scoring.TargetFaceNameChoiceIndexPage']

    template = "scoring/pages/targetfacenamechoice_page.html"

class TargetFaceIndexPage(CoderedWebPage):
    """
    Landing page for target faces
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.TargetFacePage'

    subpage_types = ['scoring.TargetFacePage']

    class Meta:
        verbose_name = "Target Face Index Page"

    template = "scoring/pages/targetface_index_page.html"

class TargetFacePage(CoderedWebPage):
    """
    Custom page for individual target faces
    """

    class Meta:
        verbose_name = "Target Face Page"

    # Only allow this page to be created beneath a TargetFaceIndexPage.
    parent_page_types = ['scoring.TargetFaceIndexPage']

    template = "scoring/pages/targetface_page.html"

    target_face = models.ForeignKey(
        'scoring.TargetFace',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Target face associated with this page (optional, but recommended for proper functionality)",
    )
    description = RichTextField(
        verbose_name="Target Face Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('target_face'),
        FieldPanel('description'),
    ]

class RoundIndexPage(CoderedWebPage):
    """
    Landing page for rounds
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.RoundPage'

    subpage_types = ['scoring.RoundPage']

    class Meta:
        verbose_name = "Round Index Page"

    template = "scoring/pages/round_index_page.html"

class RoundPage(CoderedWebPage):
    """
    Custom page for individual rounds
    """

    class Meta:
        verbose_name = "Round Page"

    # Only allow this page to be created beneath a RoundIndexPage.
    parent_page_types = ['scoring.RoundIndexPage']

    template = "scoring/pages/round_page.html"

    round = models.ForeignKey(
        'scoring.Round',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Round associated with this page (optional, but recommended for proper functionality)",
    )
    description = RichTextField(
        verbose_name="Round Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('round'),
        FieldPanel('description'),
    ]

class ScoreIndexPage(CoderedWebPage):
    """
    Landing page for scores
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.ScorePage'

    subpage_types = ['scoring.ScorePage']

    class Meta:
        verbose_name = "Score Index Page"

    template = "scoring/pages/score_index_page.html"

class ScorePage(CoderedWebPage):
    """
    Custom page for individual scores
    """

    class Meta:
        verbose_name = "Score Page"

    # Only allow this page to be created beneath a ScoreIndexPage.
    parent_page_types = ['scoring.ScoreIndexPage']

    template = "scoring/pages/score_page.html"

    score = models.ForeignKey(
        'scoring.Score',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Score associated with this page (optional, but recommended for proper functionality)",
    )
    description = RichTextField(
        verbose_name="Score Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('score'),
        FieldPanel('description'),
    ]

class CompetitionIndexPage(CoderedWebPage):
    """
    Landing page for competitions
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.CompetitionPage'

    subpage_types = ['scoring.CompetitionPage']

    class Meta:
        verbose_name = "Competition Index Page"

    template = "scoring/pages/competition_index_page.html"

class CompetitionPage(CoderedWebPage):
    """
    Custom page for individual competitions
    """

    class Meta:
        verbose_name = "Competition Page"

    # Only allow this page to be created beneath a CompetitionIndexPage.
    parent_page_types = ['scoring.CompetitionIndexPage']

    template = "scoring/pages/competition_page.html"

    competition = models.ForeignKey(
        'scoring.Competition',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Competition associated with this page (optional, but recommended for proper functionality)",
    )
    description = RichTextField(
        verbose_name="Archer Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('competition'),
        FieldPanel('description'),
    ]

class ScoringIndexPage(CoderedWebPage):
    """
    Landing page for the scoring system.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.ScoringPage'

    subpage_types = ['scoring.ScoringPage']

    class Meta:
        verbose_name = "Scoring Index Page"

    template = "scoring/pages/scoring_index_page.html"

class ScoringPage(CoderedWebPage):
    """
    Custom page for individual scoring information
    """

    # Only allow this page to be created beneath a ScoringIndexPage.
    parent_page_types = ['scoring.ScoringIndexPage']

    class Meta:
        verbose_name = "Scoring Page"

    template = "scoring/pages/scoring_page.html"

    description = RichTextField(
        verbose_name="Scoring Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class ArcherRankingIndexPage(CoderedWebPage):
    """
    Landing page for archer rankings.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.ArcherRankingPage'

    subpage_types = ['scoring.ArcherRankingPage']

    class Meta:
        verbose_name = "Archer Ranking Index Page"

    template = "scoring/pages/archer_ranking_index_page.html"

class ArcherRankingPage(CoderedWebPage):
    """
    Individual page for archer rankings.
    """

    class Meta:
        verbose_name = "Archer Ranking Page"

    template = "scoring/pages/archer_ranking_page.html"

class RulesIndexPage(CoderedWebPage):
    """
    Landing page for the rules of the scoring system.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.RulesPage'

    subpage_types = ['scoring.RulesPage']

    class Meta:
        verbose_name = "Rules Index Page"

    template = "scoring/pages/rules_index_page.html"

class RulesPage(CoderedWebPage):
    """
    Page detailing the rules of the scoring system.
    """

    class Meta:
        verbose_name = "Rules Page"

    template = "scoring/pages/rules_page.html"

class FAQIndexPage(CoderedWebPage):
    """
    Landing page for frequently asked questions.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.FAQPage'

    subpage_types = ['scoring.FAQPage']

    class Meta:
        verbose_name = "FAQ Index Page"

    template = "scoring/pages/faq_index_page.html"

class FAQPage(CoderedWebPage):
    """
    Page for frequently asked questions.
    """

    class Meta:
        verbose_name = "FAQ Page"

    template = "scoring/pages/faq_page.html"

class AboutIndexPage(CoderedWebPage):
    """
    Landing page for about us information.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.AboutPage'

    subpage_types = ['scoring.AboutPage']

    class Meta:
        verbose_name = "About Index Page"

    template = "scoring/pages/about_index_page.html"

class AboutPage(CoderedWebPage):
    """
    Page for about us information.
    """

    class Meta:
        verbose_name = "About Page"

    template = "scoring/pages/about_page.html"

class SponsorsIndexPage(CoderedWebPage):
    """
    Landing page for sponsors information.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.SponsorsPage'

    subpage_types = ['scoring.SponsorsPage']

    class Meta:
        verbose_name = "Sponsors Index Page"

    template = "scoring/pages/sponsors_index_page.html"

class SponsorsPage(CoderedWebPage):
    """
    Custom page for individual sponsors information.
    """

    class Meta:
        verbose_name = "Sponsors Page"

    # Only allow this page to be created beneath a SponsorsIndexPage.
    parent_page_types = ['scoring.SponsorsIndexPage']
    subpage_types = []

    template = "scoring/pages/sponsors_page.html"

    description = RichTextField(
        verbose_name="Sponsors Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class ResultsIndexPage(CoderedWebPage):
    """
    Landing page for results listings.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.ResultsPage'

    subpage_types = ['scoring.ResultsPage']

    class Meta:
        verbose_name = "Results Index Page"

    template = "scoring/pages/results_index_page.html"

class ResultsPage(CoderedWebPage):
    """
    Custom page for individual results listings.
    """

    class Meta:
        verbose_name = "Results Page"

    # Only allow this page to be created beneath a ResultsIndexPage.
    parent_page_types = ['scoring.ResultsIndexPage']
    subpage_types = []

    template = "scoring/pages/results_page.html"

    description = RichTextField(
        verbose_name="Results Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class RankingsIndexPage(CoderedWebPage):
    """
    Landing page for rankings listings.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.RankingsPage'

    subpage_types = ['scoring.RankingsPage']

    class Meta:
        verbose_name = "Rankings Index Page"

    template = "scoring/pages/rankings_index_page.html"

class RankingsPage(CoderedWebPage):
    """
    Custom page for individual rankings listings.
    """

    class Meta:
        verbose_name = "Rankings Page"

    # Only allow this page to be created beneath a RankingsIndexPage.
    parent_page_types = ['scoring.RankingsIndexPage']
    subpage_types = []

    template = "scoring/pages/rankings_page.html"

    description = RichTextField(
        verbose_name="Rankings Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class NewsIndexPage(CoderedWebPage):
    """
    Landing page for news listings.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.NewsPage'

    subpage_types = ['scoring.NewsPage']

    class Meta:
        verbose_name = "News Index Page"

    template = "scoring/pages/news_index_page.html"

class NewsPage(CoderedWebPage):
    """
    Custom page for individual news listings.
    """

    class Meta:
        verbose_name = "News Page"

    # Only allow this page to be created beneath a NewsIndexPage.
    parent_page_types = ['scoring.NewsIndexPage']
    subpage_types = []

    template = "scoring/pages/news_page.html"

    description = RichTextField(
        verbose_name="News Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class BlogIndexPage(CoderedWebPage):
    """
    Landing page for blog listings.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.BlogPage'

    subpage_types = ['scoring.BlogPage']

    class Meta:
        verbose_name = "Blog Index Page"

    template = "scoring/pages/blog_index_page.html"

class BlogPage(CoderedWebPage):
    """
    Custom page for individual blog listings.
    """

    class Meta:
        verbose_name = "Blog Page"

    # Only allow this page to be created beneath a BlogIndexPage.
    parent_page_types = ['scoring.BlogIndexPage']
    subpage_types = []

    template = "scoring/pages/blog_page.html"

    description = RichTextField(
        verbose_name="Blog Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class ResourcesIndexPage(CoderedWebPage):
    """
    Landing page for resources listings.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.ResourcesPage'

    subpage_types = ['scoring.ResourcesPage']

    class Meta:
        verbose_name = "Resources Index Page"

    template = "scoring/pages/resources_index_page.html"

class ResourcesPage(CoderedWebPage):
    """
    Custom page for individual resources listings.
    """

    class Meta:
        verbose_name = "Resources Page"

    # Only allow this page to be created beneath a ResourcesIndexPage.
    parent_page_types = ['scoring.ResourcesIndexPage']
    subpage_types = []

    template = "scoring/pages/resources_page.html"

    description = RichTextField(
        verbose_name="Resources Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class TutorialsIndexPage(CoderedWebPage):
    """
    Landing page for tutorials listings.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.TutorialsPage'

    subpage_types = ['scoring.TutorialsPage']

    class Meta:
        verbose_name = "Tutorials Index Page"

    template = "scoring/pages/tutorials_index_page.html"

class TutorialsPage(CoderedWebPage):
    """
    Custom page for individual tutorials listings.
    """

    class Meta:
        verbose_name = "Tutorials Page"

    # Only allow this page to be created beneath a TutorialsIndexPage.
    parent_page_types = ['scoring.TutorialsIndexPage']
    subpage_types = []

    template = "scoring/pages/tutorials_page.html"

    description = RichTextField(
        verbose_name="Tutorials Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class GuidesIndexPage(CoderedWebPage):
    """
    Landing page for guides listings.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.GuidesPage'

    subpage_types = ['scoring.GuidesPage']

    class Meta:
        verbose_name = "Guides Index Page"

    template = "scoring/pages/guides_index_page.html"

class GuidesPage(CoderedWebPage):
    """
    Custom page for individual guides listings.
    """

    class Meta:
        verbose_name = "Guides Page"

    # Only allow this page to be created beneath a GuidesIndexPage.
    parent_page_types = ['scoring.GuidesIndexPage']
    subpage_types = []

    template = "scoring/pages/guides_page.html"

    description = RichTextField(
        verbose_name="Guides Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class TestimonialsIndexPage(CoderedWebPage):
    """
    Landing page for testimonials listings.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.TestimonialsPage'

    subpage_types = ['scoring.TestimonialsPage']

    class Meta:
        verbose_name = "Testimonials Index Page"

    template = "scoring/pages/testimonials_index_page.html"

class TestimonialsPage(CoderedWebPage):
    """
    Custom page for individual testimonials listings.
    """

    class Meta:
        verbose_name = "Testimonials Page"

    # Only allow this page to be created beneath a TestimonialsIndexPage.
    parent_page_types = ['scoring.TestimonialsIndexPage']
    subpage_types = []

    subpage_types = []

    template = "scoring/pages/testimonials_page.html"

    description = RichTextField(
        verbose_name="Testimonials Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class PartnersIndexPage(CoderedWebPage):
    """
    Landing page for partners information.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.PartnersPage'

    subpage_types = ['scoring.PartnersPage']

    class Meta:
        verbose_name = "Partners Index Page"

    template = "scoring/pages/partners_index_page.html"

class PartnersPage(CoderedWebPage):
    """
    Custom page for individual partners information.
    """

    class Meta:
        verbose_name = "Partners Page"

    # Only allow this page to be created beneath a PartnersIndexPage.
    parent_page_types = ['scoring.PartnersIndexPage']
    subpage_types = []

    template = "scoring/pages/partners_page.html"

    description = RichTextField(
        verbose_name="Partners Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class CareersIndexPage(CoderedWebPage):
    """
    Landing page for careers information.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.CareersPage'

    subpage_types = ['scoring.CareersPage']

    class Meta:
        verbose_name = "Careers Index Page"

    template = "scoring/pages/careers_index_page.html"

class CareersPage(CoderedWebPage):
    """
    Custom page for individual careers information.
    """

    class Meta:
        verbose_name = "Careers Page"

    # Only allow this page to be created beneath a CareersIndexPage.
    parent_page_types = ['scoring.CareersIndexPage']
    subpage_types = []

    template = "scoring/pages/careers_page.html"

    description = RichTextField(
        verbose_name="Careers Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class PressIndexPage(CoderedWebPage):
    """
    Landing page for press information.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.PressPage'

    subpage_types = ['scoring.PressPage']

    class Meta:
        verbose_name = "Press Index Page"

    template = "scoring/pages/press_index_page.html"

class PressPage(CoderedWebPage):
    """
    Custom page for individual press information.
    """

    class Meta:
        verbose_name = "Press Page"

    # Only allow this page to be created beneath a PressIndexPage.
    parent_page_types = ['scoring.PressIndexPage']
    subpage_types = []

    template = "scoring/pages/press_page.html"

    description = RichTextField(
        verbose_name="Press Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class MediaIndexPage(CoderedWebPage):
    """
    Landing page for media listings.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.MediaPage'

    subpage_types = ['scoring.MediaPage']

    class Meta:
        verbose_name = "Media Index Page"

    template = "scoring/pages/media_index_page.html"

class MediaPage(CoderedWebPage):
    """
    Custom page for individual media listings.
    """

    class Meta:
        verbose_name = "Media Page"

    # Only allow this page to be created beneath a MediaIndexPage.
    parent_page_types = ['scoring.MediaIndexPage']
    subpage_types = []

    template = "scoring/pages/media_page.html"

    description = RichTextField(
        verbose_name="Media Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class GalleryIndexPage(CoderedWebPage):
    """
    Landing page for gallery listings.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.GalleryPage'

    subpage_types = ['scoring.GalleryPage']

    class Meta:
        verbose_name = "Gallery Index Page"

    template = "scoring/pages/gallery_index_page.html"

class GalleryPage(CoderedWebPage):
    """
    Custom page for individual gallery listings.
    """

    class Meta:
        verbose_name = "Gallery Page"

    # Only allow this page to be created beneath a GalleryIndexPage.
    parent_page_types = ['scoring.GalleryIndexPage']
    subpage_types = []

    template = "scoring/pages/gallery_page.html"

    description = RichTextField(
        verbose_name="Gallery Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class VideosIndexPage(CoderedWebPage):
    """
    Landing page for videos listings.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.VideosPage'

    subpage_types = ['scoring.VideosPage']

    class Meta:
        verbose_name = "Videos Index Page"

    template = "scoring/pages/videos_index_page.html"

class VideosPage(CoderedWebPage):
    """
    Custom page for individual videos listings.
    """

    class Meta:
        verbose_name = "Videos Page"

    # Only allow this page to be created beneath a VideosIndexPage.
    parent_page_types = ['scoring.VideosIndexPage']
    subpage_types = []

    template = "scoring/pages/videos_page.html"

    description = RichTextField(
        verbose_name="Videos Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class PodcastsIndexPage(CoderedWebPage):
    """
    Landing page for podcasts listings.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.PodcastsPage'

    subpage_types = ['scoring.PodcastsPage']

    class Meta:
        verbose_name = "Podcasts Index Page"

    template = "scoring/pages/podcasts_index_page.html"

class PodcastsPage(CoderedWebPage):
    """
    Custom page for individual podcasts listings.
    """

    class Meta:
        verbose_name = "Podcasts Page"

    # Only allow this page to be created beneath a PodcastsIndexPage.
    parent_page_types = ['scoring.PodcastsIndexPage']
    subpage_types = []

    template = "scoring/pages/podcasts_page.html"

    description = RichTextField(
        verbose_name="Podcasts Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class WebinarsIndexPage(CoderedWebPage):
    """
    Landing page for webinars listings.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.WebinarsPage'

    subpage_types = ['scoring.WebinarsPage']

    class Meta:
        verbose_name = "Webinars Index Page"

    template = "scoring/pages/webinars_index_page.html"

class WebinarsPage(CoderedWebPage):
    """
    Custom page for individual webinars listings.
    """

    class Meta:
        verbose_name = "Webinars Page"

    # Only allow this page to be created beneath a WebinarsIndexPage.
    parent_page_types = ['scoring.WebinarsIndexPage']
    subpage_types = []

    template = "scoring/pages/webinars_page.html"

    description = RichTextField(
        verbose_name="Webinars Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class WorkshopsIndexPage(CoderedWebPage):
    """
    Landing page for workshops listings.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.WorkshopsPage'

    subpage_types = ['scoring.WorkshopsPage']

    class Meta:
        verbose_name = "Workshops Index Page"

    template = "scoring/pages/workshops_index_page.html"

class WorkshopsPage(CoderedWebPage):
    """
    Custom page for individual workshops listings.
    """

    class Meta:
        verbose_name = "Workshops Page"

    # Only allow this page to be created beneath a WorkshopsIndexPage.
    parent_page_types = ['scoring.WorkshopsIndexPage']
    subpage_types = []

    template = "scoring/pages/workshops_page.html"

    description = RichTextField(
        verbose_name="Workshops Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class DownloadsIndexPage(CoderedWebPage):
    """
    Landing page for downloads listings.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.DownloadsPage'

    subpage_types = ['scoring.DownloadsPage']

    class Meta:
        verbose_name = "Downloads Index Page"

    template = "scoring/pages/downloads_index_page.html"

class DownloadsPage(CoderedWebPage):
    """
    Custom page for individual downloads listings.
    """

    class Meta:
        verbose_name = "Downloads Page"

    # Only allow this page to be created beneath a DownloadsIndexPage.
    parent_page_types = ['scoring.DownloadsIndexPage']
    subpage_types = []

    template = "scoring/pages/downloads_page.html"

    description = RichTextField(
        verbose_name="Downloads Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class DocumentationIndexPage(CoderedWebPage):
    """
    Landing page for documentation listings.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.DocumentationPage'

    subpage_types = ['scoring.DocumentationPage']

    class Meta:
        verbose_name = "Documentation Index Page"

    template = "scoring/pages/documentation_index_page.html"

class DocumentationPage(CoderedWebPage):
    """
    Custom page for individual documentation listings.
    """

    class Meta:
        verbose_name = "Documentation Page"

    # Only allow this page to be created beneath a DocumentationIndexPage.
    parent_page_types = ['scoring.DocumentationIndexPage']
    subpage_types = []

    template = "scoring/pages/documentation_page.html"

    description = RichTextField(
        verbose_name="Documentation Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class APIIndexPage(CoderedWebPage):
    """
    Landing page for API information.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.APIPage'

    subpage_types = ['scoring.APIPage']

    class Meta:
        verbose_name = "API Index Page"

    template = "scoring/pages/api_index_page.html"

class APIPage(CoderedWebPage):
    """
    Custom page for individual API information.
    """

    class Meta:
        verbose_name = "API Page"

    # Only allow this page to be created beneath a APIIndexPage.
    parent_page_types = ['scoring.APIIndexPage']
    subpage_types = []

    template = "scoring/pages/api_page.html"

    description = RichTextField(
        verbose_name="API Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class CommunityIndexPage(CoderedWebPage):
    """
    Landing page for community information.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.CommunityPage'

    subpage_types = ['scoring.CommunityPage']

    class Meta:
        verbose_name = "Community Index Page"

    template = "scoring/pages/community_index_page.html"

class CommunityPage(CoderedWebPage):
    """
    Custom page for individual community information.
    """

    class Meta:
        verbose_name = "Community Page"

    # Only allow this page to be created beneath a CommunityIndexPage.
    parent_page_types = ['scoring.CommunityIndexPage']
    subpage_types = []

    template = "scoring/pages/community_page.html"

    description = RichTextField(
        verbose_name="Community Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class ContactIndexPage(CoderedWebPage):
    """
    Landing page for contact information.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.ContactPage'

    subpage_types = ['scoring.ContactPage']

    class Meta:
        verbose_name = "Contact Index Page"

    template = "scoring/pages/contact_index_page.html"

class ContactPage(FormPage):
    """
    Custom page for individual contact information with a form.
    """

    class Meta:
        verbose_name = "Contact Page"

    # Only allow this page to be created beneath a ContactIndexPage.
    parent_page_types = ['scoring.ContactIndexPage']
    subpage_types = []

    template = "scoring/pages/contact_page.html"

    description = RichTextField(
        verbose_name="Contact Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class ForumIndexPage(CoderedWebPage):
    """
    Landing page for forum listings.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.ForumPage'

    subpage_types = ['scoring.ForumPage']

    class Meta:
        verbose_name = "Forum Index Page"

    template = "scoring/pages/forum_index_page.html"

class ForumPage(CoderedWebPage):
    """
    Custom page for individual forum listings.
    """

    class Meta:
        verbose_name = "Forum Page"

    # Only allow this page to be created beneath a ForumIndexPage.
    parent_page_types = ['scoring.ForumIndexPage']
    subpage_types = []

    template = "scoring/pages/forum_page.html"

    description = RichTextField(
        verbose_name="Forum Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class SupportIndexPage(CoderedWebPage):
    """
    Landing page for support information.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.SupportPage'

    subpage_types = ['scoring.SupportPage']

    class Meta:
        verbose_name = "Support Index Page"

    template = "scoring/pages/support_index_page.html"

class SupportPage(CoderedWebPage):
    """
    Custom page for individual support information.
    """

    class Meta:
        verbose_name = "Support Page"

    # Only allow this page to be created beneath a SupportIndexPage.
    parent_page_types = ['scoring.SupportIndexPage']
    subpage_types = []

    template = "scoring/pages/support_page.html"

    description = RichTextField(
        verbose_name="Support Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

class FeedBackIndexPage(CoderedWebPage):
    """
    Landing page for feedback information.
    """

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'scoring.FeedbackPage'

    subpage_types = ['scoring.FeedbackPage']

    class Meta:
        verbose_name = "Feedback Index Page"

    template = "scoring/pages/feedback_index_page.html"

class FeedbackPage(CoderedWebPage):
    """
    Custom page for individual feedback information.
    """

    class Meta:
        verbose_name = "Feedback Page"

    # Only allow this page to be created beneath a FeedbackIndexPage.
    parent_page_types = ['scoring.FeedbackIndexPage']
    subpage_types = []

    template = "scoring/pages/feedback_page.html"

    description = RichTextField(
        verbose_name="Feedback Description",
        null=True,
        blank=True,
        default=""
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('description'),
    ]

# TODO: Here

# TODO: Page models - End

# TODO: wagtail-flexible-form pages

from wagtail import blocks
from wagtail.images.blocks import ImageBlock
from wagtail_flexible_forms import blocks as wff_blocks

# First, let's define the fields we'd like our form to contain, as blocks.
# StreamForms can contain *any* block, not just form fields!
STREAMFORM_FIELDS = [
    # Include form field blocks from wagtail_flexible_forms.
    ("sf_singleline", wff_blocks.CharFieldBlock(group="Fields")),
    ("sf_multiline", wff_blocks.TextFieldBlock(group="Fields")),
    ("sf_checkboxes", wff_blocks.CheckboxesFieldBlock(group="Fields")),
    ("sf_radios", wff_blocks.RadioButtonsFieldBlock(group="Fields")),
    ("sf_dropdown", wff_blocks.DropdownFieldBlock(group="Fields")),
    ("sf_checkbox", wff_blocks.CheckboxFieldBlock(group="Fields")),
    ("sf_date", wff_blocks.DateFieldBlock(group="Fields")),
    ("sf_time", wff_blocks.TimeFieldBlock(group="Fields")),
    ("sf_datetime", wff_blocks.DateTimeFieldBlock(group="Fields")),
    ("sf_image", wff_blocks.ImageFieldBlock(group="Fields")),
    ("sf_file", wff_blocks.FileFieldBlock(group="Fields")),
    # And content blocks from Wagtail!
    ("text", blocks.RichTextBlock(group="Content")),
    ("image", ImageBlock(group="Content")),
]

from wagtail_flexible_forms.models import AbstractSessionFormSubmission
from wagtail_flexible_forms.models import AbstractSubmissionRevision

class MySubmissionRevision(AbstractSubmissionRevision):
    pass

class MySessionFormSubmission(AbstractSessionFormSubmission):
    @staticmethod
    def get_revision_class():
        return MySubmissionRevision

from wagtail.admin.panels import FieldPanel
from wagtail.contrib.forms.models import FormSubmission
from wagtail.fields import RichTextField
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail_flexible_forms.models import StreamFormMixin

class StreamFormPage(StreamFormMixin, Page):
    template = "scoring/forms/stream_form_page.html"
    landing_page_template = "scoring/forms/form_page_landing.html"

    # Typical Wagtail field, like any other page.
    intro = RichTextField(blank=True)

    # Set ``form_fields`` to contain our Streamform fields.
    form_fields = StreamField(STREAMFORM_FIELDS)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("form_fields"),
    ]

    @staticmethod
    def get_submission_class():
        """
        Submission class is used to store the final form
        submission, after the user has finished their session.

        For simplicity, use Wagtail's default FormSubmission class.
        """
        return FormSubmission

    @staticmethod
    def get_session_submission_class():
        """
        Session submission class is used to store temporary
        data while the form is being filled out, i.e. for
        multi-step forms.

        You must return something that inherits from
        ``AbstractSessionFormSubmission``.
        """
        return MySessionFormSubmission

