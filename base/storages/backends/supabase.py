from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from supabase import create_client, Client
import os

class SupabaseStorage(Storage):
    def __init__(self, *args, **kwargs):
        self.supabase: Client = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        self.bucket_name = os.getenv('SUPABASE_BUCKET')
        super().__init__(*args, **kwargs)

    def _save(self, name, content):
        file_path = f"{name}"
        content.seek(0)
        self.supabase.storage.from_(self.bucket_name).upload(file_path, content.read())
        return name

    def url(self, name):
        return f"{os.getenv('SUPABASE_URL')}/storage/v1/object/public/{self.bucket_name}/{name}"

    def _open(self, name, mode='rb'):
        file_path = f"{self.bucket_name}/{name}"
        response = self.supabase.storage.from_(self.bucket_name).download(file_path)
        return ContentFile(response.content)

    def exists(self, name):
        file_path = f"{self.bucket_name}/{name}"
        try:
            self.supabase.storage.from_(self.bucket_name).get_public_url(file_path)
            return True
        except:
            return False
