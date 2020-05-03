from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Uploads a file to default storage"

    def add_arguments(self, parser):
        parser.add_argument('source', type=str, help='Path of file to upload (on local disk)')
        parser.add_argument('destination', type=str, help='Remove path, where we are placing the file (default django storage)')

    def handle(self, *args, **options):
        source = options['path']
        destination = options['destination']

        print(f"Uploading: {source} ...")
        default_storage.save(destination, ContentFile(open(source, 'rb').read()))
        print("...done!")
