from django.db.models import FileField
from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

class ContentTypeRestrictedFileField(FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB 104857600
            250MB - 214958080
            500MB - 429916160
    """
    def __init__(self, *args, **kwargs):
        if 'content_types' in kwargs and 'max_upload_size' in kwargs:
            self.content_types = kwargs.pop("content_types")
            self.max_upload_size = kwargs.pop("max_upload_size")
        else:
            self.content_types = ['image/*']
            self.max_upload_size = 5242880

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)

        file = data.file
        try:
            if file._size > self.max_upload_size:
                raise forms.ValidationError(_('Please keep filesize under %(max_upload_size)s. Current filesize %(file_size)s') % ({
                    'max_upload_size': filesizeformat(self.max_upload_size),
                    'file_size': filesizeformat(file._size),
                }))
        except AttributeError:
            pass

        return data