from django_filters import rest_framework as filters

from .models import Project, Note


class ProjectInstancesFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = Project
        fields = ['name']


class NoteInstancesFilter(filters.FilterSet):
    project = filters.ModelChoiceFilter(queryset=Project.objects.all())
    created = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Note
        fields = ['project', 'created']
