from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class for Snippet model.
    Converts model instances to JSON format and vice versa.
    """
    # Read-only field to display the username of the owner of the snippet
    owner = serializers.ReadOnlyField(source='owner.username')
    # Hyperlinked field to the highlighted version of the snippet
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        # Specify the model to be serialized
        model = Snippet
        # Specify the fields to be included in the serialization
        fields = ['url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class for User model.
    Converts model instances to JSON format and vice versa.
    """
    # Hyperlinked field to represent the related snippets of the user
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        # Specify the model to be serialized
        model = User
        # Specify the fields to be included in the serialization
        fields = ['url', 'id', 'username', 'snippets']
