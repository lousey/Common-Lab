from commonlab.models import *
from commonlab.forms import *
from django.contrib import admin

class ProjectImpactLocationImageInline(admin.StackedInline):
    model = ProjectImpactLocationImage

class ProjectImpactQuoteItemInline(admin.StackedInline):
    model = ProjectImpactQuoteItem
    extra = 1
    
class ProjectImpactStatisticItemInline(admin.StackedInline):
    model = ProjectImpactStatisticItem
    extra = 1

class ProjectImpactAdmin(admin.ModelAdmin):
    exclude = ('name', 'sort_order',)
    inlines = [ProjectImpactLocationImageInline, ProjectImpactQuoteItemInline, ProjectImpactStatisticItemInline]

class ProjectPressNoImageLinkInline(admin.StackedInline):
    model = ProjectPressNoImageLink

class ProjectPressImageLinkInline(admin.StackedInline):
    model = ProjectPressImageLink

class ProjectPressAdmin(admin.ModelAdmin):
    exclude = ('name', 'sort_order',)
    inlines = [ProjectPressNoImageLinkInline, ProjectPressImageLinkInline]

class ProjectSectionImageInline(admin.StackedInline):
    model = ProjectSectionImage

class ProjectCustomSectionAdmin(admin.ModelAdmin):
    inlines = [ProjectSectionImageInline]

class ProjectImageInline(admin.StackedInline):
    model = ProjectImage

class ProjectProcessInline(admin.StackedInline):
    model = ProjectProcess
    exclude = ('name', 'sort_order',)
    max_num = 1

class ProjectMediaInline(admin.StackedInline):
    model = ProjectMedia 
    fieldsets = (
        (None, {
            'fields': ('image', 'alt', 'caption', 'sort_order'),
            'description': "Recommended size and max size: 818px x 320px. Min size: 331px x 221px"
        }),
        (None, {
            'fields': ('video_html', 'show_on_overview_section', 'show_on_process_section'),
        }),
    )

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline, ProjectProcessInline, ProjectMediaInline]

class PersonQuestionInline(admin.StackedInline):
    model = PersonQuestion

class PersonImageInline(admin.StackedInline):
    model = PersonImage

class PersonDetailImageInline(admin.StackedInline):
    model = PersonDetailImage

class PersonAdmin(admin.ModelAdmin):
    inlines = [PersonQuestionInline, PersonImageInline, PersonDetailImageInline]

class ContactAdmin(admin.ModelAdmin):
    max_num = 1

admin.site.register(Partner)
admin.site.register(ContactInfo, ContactAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(ProjectCategory)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectImpact, ProjectImpactAdmin)
admin.site.register(ProjectPress, ProjectPressAdmin)
admin.site.register(ProjectCustomSection, ProjectCustomSectionAdmin)

