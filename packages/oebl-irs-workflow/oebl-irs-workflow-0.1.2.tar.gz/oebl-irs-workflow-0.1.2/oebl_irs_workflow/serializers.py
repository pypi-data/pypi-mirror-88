from rest_framework import serializers
from .models import Author, Editor, Issue, IssueLemma, LemmaStatus, Lemma, LemmaNote


class UserSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source="pk")
    name = serializers.SerializerMethodField(method_name="get_name")

    def get_name(self, object):
        if object.last_name is not None:
            return f"{object.last_name}, {object.first_name}"
        else:
            return object.username

    class Meta:
        model = Author
        fields = ["userId", "email", "name"]


class AuthorSerializer(UserSerializer):
    class Meta:
        model = Author
        fields = ["userId", "email", "name", "address"]


class EditorSerializer(UserSerializer):
    class Meta:
        model = Editor
        fields = ["userId", "email", "name"]


class LemmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lemma
        fields = "__all__"


class LemmaStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LemmaStatus
        fields = "__all__"


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"


class LemmaNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LemmaNote
        fields = "__all__"


class IssueLemmaSerializer(serializers.ModelSerializer):
    notes = serializers.SerializerMethodField(method_name="get_notes")

    def get_notes(self, object):
        res = LemmaNote.objects.filter(lemma=object.lemma)
        return LemmaNoteSerializer(res, many=True).data

    class Meta:
        model = IssueLemma
        fields = "__all__"
        read_only_fields = ["serialization"]
        depth = 1