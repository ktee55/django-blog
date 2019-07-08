from django.db import models

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill

class Photo(models.Model):

    origin = models.ImageField(upload_to="photos/%y/%m/%d/")

    large = ImageSpecField(source="origin",
                         processors=[ResizeToFill(1280, 1024)],
                         format='JPEG'
                         )

    medium = ImageSpecField(source='origin',
                        processors=[ResizeToFill(600, 400)],
                        format="JPEG",
                        options={'quality': 75}
                        )

    small = ImageSpecField(source='origin',
                            processors=[ResizeToFill(250,250)],
                            format="JPEG",
                            options={'quality': 60}
                            )

    thumbnail= ImageSpecField(source='origin',
                            processors=[ResizeToFill(75,75)],
                            format="JPEG",
                            options={'quality': 50}
                            )
