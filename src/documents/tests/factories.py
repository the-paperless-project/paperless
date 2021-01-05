import factory

from ..models import Document, Correspondent


class CorrespondentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Correspondent

    name = factory.Faker("name")


class DocumentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Document
