from itertools import chain
import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

from notesapp.models import Project, Note


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = '__all__'


class NoteType(DjangoObjectType):
    class Meta:
        model = Note
        fields = '__all__'


class Query(graphene.ObjectType):
    all_notes = graphene.List(NoteType)
    all_projects = graphene.List(ProjectType)
    users_by_project_id = graphene.List(
        UserType,
        id=graphene.Int(required=True)
    )
    users_by_project_name = graphene.List(
        UserType,
        name=graphene.String(required=True)
    )
    users_note_author_by_project_id = graphene.List(
        UserType,
        id=graphene.Int(required=True)
    )

    def resolve_all_notes(root, info):
        # one of the way to restrict anonymous access
        # if info.context.user.is_anonymous:
        #     return None
        return Note.objects.all()

    def resolve_all_projects(root, info):
        return Project.objects.all()

    def resolve_users_by_project_id(root, info, id):
        try:
            users = Project.objects.get(pk=id).users.all()
        except Project.DoesNotExist:
            users = None
        return users

    def resolve_users_by_project_name(root, info, name):
        try:
            users = Project.objects.get(name=name).users.all()
        except Project.DoesNotExist:
            users = None
        except Project.MultipleObjectsReturned:
            users = set(
                chain.from_iterable(
                    project.users.all()
                    for project in Project.objects.filter(name=name).prefetch_related('users')
                )
            )
        return users

    def resolve_users_note_author_by_project_id(root, info, id):
        return {
            note.author
            for note in Note.objects.filter(project__id=id).select_related('author')
        }


class NoteDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    
    message = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, id):
        try:
            note = Note.objects.get(pk=id)
        except Note.DoesNotExist:
            return NoteDeleteMutation(message=f'Note with id={id} does not exist.')
        note.is_active = False
        note.save()
        return NoteDeleteMutation(message=f'Note with id={id} marked as non-active.')


class NoteUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        body = graphene.String(required=True)

    note = graphene.Field(NoteType)

    @classmethod
    def mutate(cls, root, info, id, body):
        try:
            note = Note.objects.get(pk=id)
        except Note.DoesNotExist:
            return NoteUpdateMutation(note=None)
        note.body = body
        note.save()
        return cls(note=note)


class Mutation(graphene.ObjectType):
    delete_note = NoteDeleteMutation.Field()
    update_note = NoteUpdateMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
