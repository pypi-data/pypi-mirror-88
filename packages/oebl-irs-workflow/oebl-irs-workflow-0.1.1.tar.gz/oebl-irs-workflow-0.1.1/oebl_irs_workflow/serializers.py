from rest_framework import serializers
from .models import Author, Editor, Issue, IssueLemma, LemmaStatus, Lemma


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


class IssueLemmaSerializer(serializers.ModelSerializer):
    author = AuthorSerializer
    editor = EditorSerializer
    lemma = LemmaSerializer
    status = LemmaStatusSerializer
    issue = IssueSerializer

    class Meta:
        model = IssueLemma
        fields = "__all__"
        read_only_fields = ["serialization"]