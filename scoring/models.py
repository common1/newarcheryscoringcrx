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
        verbose_name=_("Image"),
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
        on_delete=models.PROTECT,
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
        on_delete=models.PROTECT,
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
        on_delete=models.PROTECT,
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
        on_delete=models.PROTECT,
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
        help_text=_("format: H:M:S, not required"),
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
        help_text=_("format: H:M:S, not required"),
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
        ordering = ['name']
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
        on_delete=models.PROTECT,
        unique=False,
        default=1,
        verbose_name=_("Round"),
        help_text=_("format: required"),
        related_name='roundmembership_round'
    )
    archer = models.ForeignKey(
        Archer,
        on_delete=models.PROTECT,
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
        on_delete=models.PROTECT,
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
    deletete_view_enabled=False

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
    list_display = ('name', BooleanColumn('is_active'),)
    list_filter = ('is_active',)
    inspect_view_enabled = True
    copy_view_enabled = True

    panels = [
        FieldPanel('name'),
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
    list_filter = ('is_active',)
    inspect_view_enabled = True
    copy_view_enabled = True

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
    archer = models.ForeignKey(
        'scoring.Archer',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Archer associated with this page (optional, but recommended for proper functionality)",
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('archer'),
    ]

    class Meta:
        verbose_name = "Archer Page"

    # Only allow this page to be created beneath an ArchersIndexPage.
    parent_page_types = ['scoring.ArcherIndexPage']

    template = "scoring/pages/archer_page.html"

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
    discipline = models.ForeignKey(
        'scoring.Discipline',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Discipline associated with this page (optional, but recommended for proper functionality)",
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('discipline'),
    ]

    class Meta:
        verbose_name = "Discipline Page"

    # Only allow this page to be created beneath a DisciplineIndexPage.
    parent_page_types = ['scoring.DisciplineIndexPage']

    template = "scoring/pages/discipline_page.html"

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
    club = models.ForeignKey(
        'scoring.Club',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Club associated with this page (optional, but recommended for proper functionality)",
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('club'),
    ]

    class Meta:
        verbose_name = "Club Page"

    # Only allow this page to be created beneath a ClubIndexPage.
    parent_page_types = ['scoring.ClubIndexPage']

    template = "scoring/pages/club_page.html"

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
    category = models.ForeignKey(
        'scoring.Category',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Category associated with this page (optional, but recommended for proper functionality)",
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('category'),
    ]

    class Meta:
        verbose_name = "Category Page"

    # Only allow this page to be created beneath a CategoryIndexPage.
    parent_page_types = ['scoring.CategoryIndexPage']

    template = "scoring/pages/category_page.html"

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
    age_group = models.ForeignKey(
        'scoring.AgeGroup',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Age group associated with this page (optional, but recommended for proper functionality)",
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('age_group'),
    ]

    class Meta:
        verbose_name = "Age Group Page"

    # Only allow this page to be created beneath an AgeGroupIndexPage.
    parent_page_types = ['scoring.AgeGroupIndexPage']

    template = "scoring/pages/agegroup_page.html"

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
    team = models.ForeignKey(
        'scoring.Team',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Team associated with this page (optional, but recommended for proper functionality)",
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('team'),
    ]

    class Meta:
        verbose_name = "Team Page"

    # Only allow this page to be created beneath a TeamIndexPage.
    parent_page_types = ['scoring.TeamIndexPage']

    template = "scoring/pages/team_page.html"

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
    scoring_sheet = models.ForeignKey(
        'scoring.ScoringSheet',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Scoring sheet associated with this page (optional, but recommended for proper functionality)",
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('scoring_sheet'),
    ]

    class Meta:
        verbose_name = "Scoring Sheet Page"

    # Only allow this page to be created beneath a ScoringSheetIndexPage.
    parent_page_types = ['scoring.ScoringSheetIndexPage']

    template = "scoring/pages/scoringsheet_page.html"

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

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('target_face_name_choice'),
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
    target_face = models.ForeignKey(
        'scoring.TargetFace',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Target face associated with this page (optional, but recommended for proper functionality)",
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('target_face'),
    ]

    class Meta:
        verbose_name = "Target Face Page"

    # Only allow this page to be created beneath a TargetFaceIndexPage.
    parent_page_types = ['scoring.TargetFaceIndexPage']

    template = "scoring/pages/targetface_page.html"

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
    round = models.ForeignKey(
        'scoring.Round',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Round associated with this page (optional, but recommended for proper functionality)",
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('round'),
    ]

    class Meta:
        verbose_name = "Round Page"

    # Only allow this page to be created beneath a RoundIndexPage.
    parent_page_types = ['scoring.RoundIndexPage']

    template = "scoring/pages/round_page.html"

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
    score = models.ForeignKey(
        'scoring.Score',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Score associated with this page (optional, but recommended for proper functionality)",
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('score'),
    ]

    class Meta:
        verbose_name = "Score Page"

    # Only allow this page to be created beneath a ScoreIndexPage.
    parent_page_types = ['scoring.ScoreIndexPage']

    template = "scoring/pages/score_page.html"

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
    competition = models.ForeignKey(
        'scoring.Competition',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Competition associated with this page (optional, but recommended for proper functionality)",
    )

    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('competition'),
    ]

    class Meta:
        verbose_name = "Competition Page"

    # Only allow this page to be created beneath a CompetitionIndexPage.
    parent_page_types = ['scoring.CompetitionIndexPage']

    template = "scoring/pages/competition_page.html"

# TODO: Here

class ScoringInfoPage(CoderedWebPage):
    """
    Information page about the scoring system.
    """

    class Meta:
        verbose_name = "Scoring Info Page"

    template = "scoring/pages/scoring_info_page.html"

class RulesPage(CoderedWebPage):
    """
    Page detailing the rules of the scoring system.
    """

    class Meta:
        verbose_name = "Rules Page"

    template = "scoring/pages/rules_page.html"

class FAQPage(CoderedWebPage):
    """
    Frequently Asked Questions page.
    """

    class Meta:
        verbose_name = "FAQ Page"

    template = "scoring/pages/faq_page.html"

class AboutPage(CoderedWebPage):
    """
    About us page.
    """

    class Meta:
        verbose_name = "About Page"

    template = "scoring/pages/about_page.html"

class SponsorsPage(CoderedWebPage):
    """
    Sponsors information page.
    """

    class Meta:
        verbose_name = "Sponsors Page"

    template = "scoring/pages/sponsors_page.html"

class EventsPage(CoderedWebPage):
    """
    Events listing page.
    """

    class Meta:
        verbose_name = "Events Page"

    template = "scoring/pages/events_page.html"

class ResultsPage(CoderedWebPage):
    """
    Results listing page.
    """

    class Meta:
        verbose_name = "Results Page"

    template = "scoring/pages/results_page.html"

class RankingsPage(CoderedWebPage):
    """
    Rankings listing page.
    """

    class Meta:
        verbose_name = "Rankings Page"

    template = "scoring/pages/rankings_page.html"

class NewsPage(CoderedWebPage):
    """
    News listing page.
    """

    class Meta:
        verbose_name = "News Page"

    template = "scoring/pages/news_page.html"

class BlogPage(CoderedWebPage):
    """
    Blog listing page.
    """

    class Meta:
        verbose_name = "Blog Page"

    template = "scoring/pages/blog_page.html"

class ResourcesPage(CoderedWebPage):
    """
    Resources listing page.
    """

    class Meta:
        verbose_name = "Resources Page"

    template = "scoring/pages/resources_page.html"

class TutorialsPage(CoderedWebPage):
    """
    Tutorials listing page.
    """

    class Meta:
        verbose_name = "Tutorials Page"

    template = "scoring/pages/tutorials_page.html"

class GuidesPage(CoderedWebPage):
    """
    Guides listing page.
    """

    class Meta:
        verbose_name = "Guides Page"

    template = "scoring/pages/guides_page.html"

class TestimonialsPage(CoderedWebPage):
    """
    Testimonials listing page.
    """

    class Meta:
        verbose_name = "Testimonials Page"

    template = "scoring/pages/testimonials_page.html"

class PartnersPage(CoderedWebPage):
    """
    Partners information page.
    """

    class Meta:
        verbose_name = "Partners Page"

    template = "scoring/pages/partners_page.html"

class TeamPage(CoderedWebPage):
    """
    Team information page.
    """

    class Meta:
        verbose_name = "Team Page"

    template = "scoring/pages/team_page.html"

class CareersPage(CoderedWebPage):
    """
    Careers information page.
    """

    class Meta:
        verbose_name = "Careers Page"

    template = "scoring/pages/careers_page.html"

class PressPage(CoderedWebPage):
    """
    Press information page.
    """

    class Meta:
        verbose_name = "Press Page"

    template = "scoring/pages/press_page.html"

class MediaPage(CoderedWebPage):
    """
    Media listing page.
    """

    class Meta:
        verbose_name = "Media Page"

    template = "scoring/pages/media_page.html"

class GalleryPage(CoderedWebPage):
    """
    Gallery listing page.
    """

    class Meta:
        verbose_name = "Gallery Page"

    template = "scoring/pages/gallery_page.html"

class VideosPage(CoderedWebPage):
    """
    Videos listing page.
    """

    class Meta:
        verbose_name = "Videos Page"

    template = "scoring/pages/videos_page.html"

class PodcastsPage(CoderedWebPage):
    """
    Podcasts listing page.
    """

    class Meta:
        verbose_name = "Podcasts Page"

    template = "scoring/pages/podcasts_page.html"

class WebinarsPage(CoderedWebPage):
    """
    Webinars listing page.
    """

    class Meta:
        verbose_name = "Webinars Page"

    template = "scoring/pages/webinars_page.html"

class WorkshopsPage(CoderedWebPage):
    """
    Workshops listing page.
    """

    class Meta:
        verbose_name = "Workshops Page"

    template = "scoring/pages/workshops_page.html"

class DownloadsPage(CoderedWebPage):
    """
    Downloads listing page.
    """

    class Meta:
        verbose_name = "Downloads Page"

    template = "scoring/pages/downloads_page.html"

class DocumentationPage(CoderedWebPage):
    """
    Documentation listing page.
    """

    class Meta:
        verbose_name = "Documentation Page"

    template = "scoring/pages/documentation_page.html"

class APIPage(CoderedWebPage):
    """
    API information page.
    """

    class Meta:
        verbose_name = "API Page"

    template = "scoring/pages/api_page.html"

class CommunityPage(CoderedWebPage):
    """
    Community information page.
    """

    class Meta:
        verbose_name = "Community Page"

    template = "scoring/pages/community_page.html"

class ForumPage(CoderedWebPage):
    """
    Forum listing page.
    """

    class Meta:
        verbose_name = "Forum Page"

    template = "scoring/pages/forum_page.html"

class EventsLandingPage(CoderedWebPage):
    """
    Landing page for events-related content.
    """

    class Meta:
        verbose_name = "Events Landing Page"

    template = "scoring/pages/events_landing_page.html"

class ResultsLandingPage(CoderedWebPage):
    """
    Landing page for results-related content.
    """

    class Meta:
        verbose_name = "Results Landing Page"

    template = "scoring/pages/results_landing_page.html"

class RankingsLandingPage(CoderedWebPage):
    """
    Landing page for rankings-related content.
    """

    class Meta:
        verbose_name = "Rankings Landing Page"

    template = "scoring/pages/rankings_landing_page.html"

class NewsLandingPage(CoderedWebPage):
    """
    Landing page for news-related content.
    """

    class Meta:
        verbose_name = "News Landing Page"

    template = "scoring/pages/news_landing_page.html"

class BlogLandingPage(CoderedWebPage):
    """
    Landing page for blog-related content.
    """

    class Meta:
        verbose_name = "Blog Landing Page"

    template = "scoring/pages/blog_landing_page.html"

class ResourcesLandingPage(CoderedWebPage):
    """
    Landing page for resources-related content.
    """

    class Meta:
        verbose_name = "Resources Landing Page"

    template = "scoring/pages/resources_landing_page.html"

class TutorialsLandingPage(CoderedWebPage):
    """
    Landing page for tutorials-related content.
    """

    class Meta:
        verbose_name = "Tutorials Landing Page"

    template = "scoring/pages/tutorials_landing_page.html"

class GuidesLandingPage(CoderedWebPage):
    """
    Landing page for guides-related content.
    """

    class Meta:
        verbose_name = "Guides Landing Page"

    template = "scoring/pages/guides_landing_page.html" 

class SupportLandingPage(CoderedWebPage):
    """
    Landing page for support-related content.
    """

    class Meta:
        verbose_name = "Support Landing Page"

    template = "scoring/pages/support_landing_page.html"    

class ContacUsPage(FormPage):
    """
    Contact us page with a form.
    """
    
    class Meta:
        verbose_name = "Contact Us Page"

    template = "scoring/pages/contact_us_page.html"

class SupportPage(FormPage):
    """
    Support page with a form.
    """

    class Meta:
        verbose_name = "Support Page"

    template = "scoring/pages/support_page.html"

class FeedbackPage(FormPage):
    """
    Feedback page with a form.
    """

    class Meta:
        verbose_name = "Feedback Page"

    template = "scoring/pages/feedback_page.html"

# TODO: Page models - End

