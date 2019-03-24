from django.template.defaultfilters import slugify
from django.db import models
from markdown import markdown
from django.contrib.contenttypes.models import ContentType
from PIL import Image
from html_image.models import \
        BaseHtmlImage, OwnedImageMixin, OwnedImageToOneField, SizedImageMixin
from django.utils.translation import ugettext_lazy as _

class ProjectImageMixin(SizedImageMixin):
    MIN_WIDTH, MAX_WIDTH, MIN_HEIGHT, MAX_HEIGHT = (331, 331, 221, 221)


class ProjectImpactLocationImageMixin(SizedImageMixin):
    MIN_WIDTH, MAX_WIDTH, MIN_HEIGHT, MAX_HEIGHT = (100, 300, 100, 400)


class ProjectPressLinkImageMixin(SizedImageMixin):
    MIN_WIDTH, MAX_WIDTH, MIN_HEIGHT, MAX_HEIGHT = (10, 300, 10, 500)


class ProjectSectionImageMixin(SizedImageMixin):
    MIN_WIDTH, MAX_WIDTH, MIN_HEIGHT, MAX_HEIGHT = (10, 400, 10, 700)


class ProjectMediaMixin(SizedImageMixin):
    MIN_WIDTH, MAX_WIDTH, MIN_HEIGHT, MAX_HEIGHT = (331, 818, 221, 320)


class PersonImageMixin(SizedImageMixin):
    MIN_WIDTH, MAX_WIDTH, MIN_HEIGHT, MAX_HEIGHT = (165, 165, 221, 221)


class PersonDetailImageMixin(SizedImageMixin):
    MIN_WIDTH, MAX_WIDTH, MIN_HEIGHT, MAX_HEIGHT = (331, 331, 221, 221)


class PartnerImageMixin(SizedImageMixin):
    MIN_WIDTH, MAX_WIDTH, MIN_HEIGHT, MAX_HEIGHT = (331, 331, 115, 115)


class ProjectCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    sort_order = models.IntegerField()

    class Meta:
        ordering = ['sort_order']
        verbose_name_plural = 'Project Categories'
    
    def __unicode__(self):
	return u'#%s: %s' % (self.sort_order, self.name)


class PersonCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    sort_order = models.IntegerField()

    class Meta:
        ordering = ['sort_order']
        verbose_name_plural = 'People Categories'
    
    def __unicode__(self):
	return u'#%s: %s' % (self.sort_order, self.name)   


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    sort_order = models.IntegerField()
    affiliates = models.ManyToManyField('self', symmetrical=False, null=True, blank=True, help_text="Affiliated projects will be highlighted in the navigation when the user mouses over this project.")
    categories = models.ManyToManyField(ProjectCategory, related_name="projects", blank=True)
    slug = models.SlugField(editable=False)
    quote = models.CharField(max_length=130)
    detail_title = models.CharField(blank=True, null=True, max_length=200, help_text="Title on the detail page. Defaults to [Name]: [Quote]")
    url = models.CharField(max_length=100, blank=True, null=True, help_text="Ex: http://www.google.com")
    url_title = models.CharField(max_length=20, blank=True, null=True)
    info_text = models.TextField(blank=True, help_text="Information about project collaborators & affiliaties. Uses Markdown. Use two spaces + return for a line break.")
    info_html = models.TextField(blank=True, editable=False)
        
    class Meta:
	ordering = ['sort_order', 'slug']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.info_html = markdown(self.info_text)
        if not self.detail_title:
            self.detail_title = u'%s: %s' % (self.name, self.quote)
        super(Project, self).save(*args, **kwargs)
        if len(ProjectOverview.objects.filter(project=self)) == 0:
            overview = ProjectOverview()
            overview.project_id = self.id
            overview.save()

    def get_next(self):
        objs = Project.objects.all().order_by('sort_order', 'slug')
        i = 0
        for index, item in enumerate(objs):
            if item == self:
                i = index
        if len(objs) > i + 1:
            return objs[i+1]
        return objs[0]

    def get_prev(self):
        objs = Project.objects.all().order_by('sort_order', 'slug')
        i = 0
        for index, item in enumerate(objs):
            if item == self:
                i = index
        if objs[0] == self:
            return objs[len(objs) - 1]
        return objs[i-1]

    def overview_medias(self):
        return self.medias.filter(show_on_overview_section=True)
    
    def process_medias(self):
        return self.medias.filter(show_on_process_section=True)

    def __unicode__(self):
	return u'#%s: %s' % (self.sort_order, self.name)


class ProjectImage(ProjectImageMixin, OwnedImageMixin, BaseHtmlImage):
    owner = OwnedImageToOneField(Project)


class ProjectSection(models.Model):
    content_type = models.ForeignKey(ContentType,editable=False,null=True)
    name = models.CharField(max_length=50)
    sort_order = models.IntegerField(default=5)
    priority = models.IntegerField(editable=False, default=2)
    slug = models.SlugField(editable=False)
    project = models.ForeignKey(Project, related_name="sections")
    
    class Meta:
	ordering = ['sort_order', 'priority']
	unique_together = ['name', 'project']

    def save(self, *args, **kwargs):
        if(not self.content_type):
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        self.slug = slugify(self.name)
        super(ProjectSection, self).save(*args, **kwargs)

    def as_leaf_class(self):
        content_type = self.content_type
        model = content_type.model_class()
        return model.objects.get(id=self.id)

    def __unicode__(self):
	return u'%s: %s' % (self.project.name, self.name)


class ProjectOverview(ProjectSection):
    """
    Assumed that all projects have an overview section.
    """
    
    class Meta:
        verbose_name_plural = "Project Overview Section"
    
    def save(self, *args, **kwargs):
        self.name = "Overview"
        self.sort_order = 1
        super(ProjectOverview, self).save(*args, **kwargs)


class ProjectProcess(ProjectSection):
    process_text = models.TextField(blank=True, help_text="Uses Markdown.")
    process_html = models.TextField(blank=True, editable=False)
    process_footer_text = models.TextField(blank=True, help_text="Uses Markdown.")
    process_footer_html = models.TextField(blank=True, editable=False)

    class Meta:
        verbose_name_plural = "Project Process Section"
 
    def save(self, *args, **kwargs):
        self.name = "Process"
        self.sort_order = 3
        self.process_html = markdown(self.process_text)
        self.process_footer_html = markdown(self.process_footer_text)
        super(ProjectProcess, self).save(*args, **kwargs)


class ProjectImpact(ProjectSection):

    class Meta:
        verbose_name_plural = "Project Impact Sections"
  
    def save(self, *args, **kwargs):
        self.name = "Impact"
        self.sort_order = 2
        super(ProjectImpact, self).save(*args, **kwargs)


class ProjectImpactLocationImage(ProjectImpactLocationImageMixin, OwnedImageMixin, BaseHtmlImage):
    owner = OwnedImageToOneField(ProjectImpact)


class ProjectImpactItem(models.Model):
    impact = models.ForeignKey(ProjectImpact, related_name="items")
    sort_order = models.IntegerField()
    content_type = models.ForeignKey(ContentType,editable=False,null=True)

    class Meta:
        ordering = ['sort_order']

    def as_leaf_class(self):
        content_type = self.content_type
        model = content_type.model_class()
        return model.objects.get(id=self.id)

    def save(self, *args, **kwargs):
        if(not self.content_type):
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        super(ProjectImpactItem, self).save(*args, **kwargs)

    def __unicode__(self):
	return u'Impact Item: %s' % (self.sort_order)


class ProjectImpactStatisticItem(ProjectImpactItem):
    number = models.CharField(max_length=5)
    description = models.CharField(max_length=50)

    def is_statistic(self):
        return True


class ProjectImpactQuoteItem(ProjectImpactItem):

    GRID_CHOICES = (
            (1, '1 grid long'),
            (2, '2 grids long'),
    )
    quote = models.CharField(max_length=200)
    source = models.CharField(max_length=50, help_text="Example: John Smith, Manager")
    number_of_grids = models.IntegerField(choices=GRID_CHOICES, help_text="Quotes can be displayed in one grid or across two grids.")

    def is_quote(self):
        return True


class ProjectPress(ProjectSection):

    class Meta:
        verbose_name_plural = "Project Press Sections"

    def save(self, **kwargs):
        self.name = "Press"
        self.sort_order = 4
        super(ProjectPress, self).save(**kwargs)


class ProjectPressLink(models.Model):
    sort_order = models.IntegerField()
    quote = models.CharField(max_length=200)
    source = models.CharField(max_length=100, help_text="Example: Birmingham News")
    attribution = models.CharField(max_length=100, help_text="Example: John Doe, Mayor")
    url = models.CharField(max_length=100)
    owner = models.ForeignKey(ProjectPress, related_name="items")
    content_type = models.ForeignKey(ContentType,editable=False,null=True)

    class Meta:
        ordering = ['sort_order']

    def as_leaf_class(self):
        content_type = self.content_type
        model = content_type.model_class()
        return model.objects.get(id=self.id)

    def save(self, *args, **kwargs):
        if(not self.content_type):
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        super(ProjectPressLink, self).save(*args, **kwargs)
        
    def __unicode__(self):
	return u'Press Link: %s' % (self.source)


class ProjectPressNoImageLink(ProjectPressLink):

    def __unicode__(self):
	return u'#%s: %s' % (self.sort_order, self.source)
        
    
class ProjectPressImageLink(ProjectPressLinkImageMixin, OwnedImageMixin, BaseHtmlImage, ProjectPressLink):

    def __unicode__(self):
	return u'#%s: %s' % (self.sort_order, self.source)
        
    
class ProjectCustomSection(ProjectSection):
    section_text = models.TextField(help_text="Uses Markdown.")
    section_html = models.TextField(editable=False)

    class Meta:
        verbose_name_plural = "Project Custom Sections"

    def save(self, *args, **kwargs):
        self.priority = 1
        self.section_html = markdown(self.section_text)
        super(ProjectCustomSection, self).save(**kwargs)


class ProjectSectionImage(ProjectSectionImageMixin, OwnedImageMixin, BaseHtmlImage):
    owner = OwnedImageToOneField(ProjectSection)
    

class ProjectMedia(ProjectMediaMixin, OwnedImageMixin, BaseHtmlImage):
    """
    Media for the Overview or Process sections
    """
    owner = models.ForeignKey(Project, related_name="medias")
    caption = models.CharField(max_length="300", blank=True)    
    sort_order = models.IntegerField()
    video_html = models.TextField(blank=True, help_text="Add video embed iframe code if this is a video. iframe must be smaller than 818x320", null=True)
    show_on_overview_section = models.BooleanField()
    show_on_process_section = models.BooleanField()
    
    class Meta:
        ordering = ['sort_order']
        verbose_name_plural = 'Project Media'
  
    def suffixed_url(self, suffix, root):
        filename = root.rsplit('/', 1)[1].rsplit('.', 1)[0]  
        fullpath = root.rsplit('/', 1)[0]  
        return fullpath + "/" + filename + suffix

    def small_url(self):
        return self.suffixed_url("_small.jpg", str(self.image.url))

    def large_url(self):
        return self.suffixed_url("_large.jpg", str(self.image.url))
    
    def save(self, *args, **kwargs):
        self.video_html = self.video_html.replace("'", '"')
        """
        Save a resized version of the image for display on detail pages
        """
        super(ProjectMedia, self).save(*args, **kwargs)
        path = str(self.image.path)
        if not path == '':
            img = Image.open(path)
            ratio = img.size[0] / img.size[1]
            if (ratio > 1.5):
                area = img.crop((0, 0, int(img.size[1] * 1.5), img.size[1]))
            elif (ratio < 1.5):
                area = img.crop((0, 0, img.size[0], int(img.size[0] * 2/3)))
            area = area.resize((333, 222), Image.ANTIALIAS)
            area.save(self.suffixed_url("_large.jpg", path))
            area = area.resize((165, 110), Image.ANTIALIAS)
            area.save(self.suffixed_url("_small.jpg", path))
            
    def delete(self):
        try:
            os.remove(self.suffixed_url("_large.jpg", path))
            os.remove(self.suffixed_url("_small.jpg", path))
        except:
            pass
        super(ProjectMedia, self).delete()

    def __unicode__(self):
	return u'%s: Media #%s' % (self.owner.name, self.sort_order)
    

class Person(models.Model):
    sort_order = models.IntegerField()
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    role = models.CharField(max_length=120, blank=True)
    quote = models.CharField(max_length=130)
    bio = models.TextField(blank=True)
    categories = models.ManyToManyField(PersonCategory, related_name="people", blank=True)
    email = models.EmailField(max_length=100, blank=True)
    twitter_username = models.CharField(max_length=100, blank=True, help_text="Example: aplusk")
    site_url = models.CharField(max_length=150, blank=True, help_text="Example: http://www.google.com")
    facebook_url = models.CharField(max_length=150, blank=True, help_text="Example: http://www.facebook.com/johndoe")
    slug = models.SlugField(editable=False)
        
    class Meta:
	ordering = ['sort_order', 'slug']
	verbose_name_plural = 'People'
	unique_together = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        self.slug = slugify('%s %s' % (self.first_name, self.last_name))
        super(Person, self).save(*args, **kwargs)

    def get_next(self):
        objs = Person.objects.all().order_by('sort_order', 'slug')
        i = 0
        for index, item in enumerate(objs):
            if item == self:
                i = index
        if len(objs) > i + 1:
            return objs[i+1]
        return objs[0]

    def get_prev(self):
        objs = Person.objects.all().order_by('sort_order', 'slug')
        i = 0
        for index, item in enumerate(objs):
            if item == self:
                i = index
        if objs[0] == self:
            return objs[len(objs) - 1]
        return objs[i-1]
    
    def __unicode__(self):
	return u'#%s: %s %s' % (self.sort_order, self.first_name, self.last_name)


class PersonImage(PersonImageMixin, OwnedImageMixin, BaseHtmlImage):
    owner = OwnedImageToOneField(Person)

    
class PersonDetailImage(PersonDetailImageMixin, OwnedImageMixin, BaseHtmlImage):
    owner = OwnedImageToOneField(Person)


class PersonQuestion(models.Model):
    sort_order = models.IntegerField()
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=300)
    person = models.ForeignKey(Person, related_name="questions")

    class Meta:
        ordering = ['sort_order']
        
    def __unicode__(self):
	return u'Question #%s:' % (self.sort_order)


class Partner(PartnerImageMixin, BaseHtmlImage):
    sort_order = models.IntegerField()
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=300, blank=True)
    site_url = models.CharField(max_length=200)
    
    class Meta:
	ordering = ['sort_order']

    def __unicode__(self):
	return u'%s' % (self.name)


class ContactInfo(models.Model):
    info = models.TextField(help_text="Uses Markdown. Two spaces + return for a line break.")
    info_html = models.TextField(editable=False)
    email = models.EmailField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = 'Contact Info'

    def save(self, *args, **kwargs):
        self.info_html = markdown(self.info)
        super(ContactInfo, self).save(*args, **kwargs)

    def __unicode__(self):
	return u'Contact info'
