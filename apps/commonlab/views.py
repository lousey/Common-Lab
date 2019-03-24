from django.views.generic import DetailView, FormView
from django.views.generic.edit import SingleObjectMixin
from commonlab.models import Project, ProjectSection, Person, PersonQuestion
from commonlab.forms import PersonQuestionForm
from django.http import Http404, HttpResponse
from django.core.mail import send_mail
from django.template.loader_tags import BlockNode, ExtendsNode
from django.template import loader, Context, RequestContext, TextNode

class ProjectDetailView(DetailView):

    context_object_name = "project"
    model = Project
    section = ""

    def get_context_data(self, *args, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        project = self.get_object()
        # Add in a QuerySet of all the books
        if self.kwargs.get('section'):
            self.section = self.kwargs['section']
        sec = project.sections.filter(slug=self.section);
        if len(sec) == 0:
            raise Http404
        context['section'] = sec[0].as_leaf_class()      
        return context


class PersonDetailView(FormView, SingleObjectMixin):
    form_class = PersonQuestionForm
    model = Person

    def get_success_url(self):
        return '#submit'

    def get_context_data(self, *args, **kwargs):
        context = super(PersonDetailView, self).get_context_data(**kwargs)
        person = self.get_object()
        context['person'] = person
        return context

    def form_valid(self, form):
        #q = PersonQuestion(question=form.cleaned_data['question'], sort_order=1)
        #self.get_object().questions.add(q)
        send_mail(("Question asked for %s %s on Commonlab") % (self.get_object().first_name,
                                                                self.get_object().last_name),
                  form.cleaned_data['question'], "site@commonlab.com", ["commonlabquestion@gmail.com"])
        return super(PersonDetailView, self).form_valid(form)
        


