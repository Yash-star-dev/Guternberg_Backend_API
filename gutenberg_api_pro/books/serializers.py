from rest_framework import serializers
from .models import *


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksAuthor
        fields = ["name", "birth_year", "death_year"]


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksFormat
        fields = ["mime_type", "url"]


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()
    bookshelves = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()
    download_links = serializers.SerializerMethodField()

    class Meta:
        model = BooksBook
        fields = [
            "title",
            "authors",
            "languages",
            "subjects",
            "bookshelves",
            "download_links",
        ]

    def get_authors(self, obj):
        return AuthorSerializer(
            [a.author for a in obj.booksbookauthors_set.all()], many=True
        ).data

    def get_subjects(self, obj):
        return [s.subject.name for s in obj.booksbooksubjects_set.all()]

    def get_bookshelves(self, obj):
        return [b.bookshelf.name for b in obj.booksbookbookshelves_set.all()]

    def get_languages(self, obj):
        return [l.language.code for l in obj.booksbooklanguages_set.all()]

    def get_download_links(self, obj):
        return FormatSerializer(obj.booksformat_set.all(), many=True).data
