from django.forms import ModelForm
from.models import CreateImages

class ImagesPost(ModelForm):
    class Meta:
        model = CreateImages
        fields = ['author', 'caption', 'image', 'created_at']