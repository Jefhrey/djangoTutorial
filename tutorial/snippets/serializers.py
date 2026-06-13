from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from rest_framework import serializers
from django.contrib.auth.models import User


# Create and save only affect DB operations. the serialization itself is handle4d when you defined the meta class and stuff
class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username") #controls how owners is treated for read operations when it needs to be sent in responses. Writing is still controlled by the perfoerm save function
    highlight = serializers.HyperlinkedIdentityField(
        view_name="snippet-highlight", format="html"
    )
    class Meta:
        model = Snippet
        fields = ["url", "id", "title", "code", "linenos", "language", "style", "owner", "highlight"]

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data) 
    
    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get("title", instance.title)
        instance.code = validated_data.get("code", instance.code)
        instance.linenos = validated_data.get("linenos", instance.linenos)
        instance.language = validated_data.get("language", instance.language)
        instance.style = validated_data.get("style", instance.style)
        instance.save()
        return instance
    


    
class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(
        many=True, view_name = "snippet-detail", read_only = True
    )

    class Meta:
        model = User
        fields = ["url", "id", "username", "snippets"]