from django.test import TestCase
from .models import Word, FileForAnalysis
from django.core.files.uploadedfile import SimpleUploadedFile
from .utils import get_text_content
import re


class FileAnalysisCases(TestCase):

    def setUp(self) -> None:
        self.data = """
            Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, 
            totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta 
            sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia 
            consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui 
            dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi 
            tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, 
            quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? 
            Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel 
            illum qui dolorem eum fugiat quo voluptas nulla pariatur?
        """
        f_obj = SimpleUploadedFile(name='test.txt', content=self.data.encode('utf-8'), content_type='text/plain')
        self.file = FileForAnalysis.objects.create(upload=f_obj)
        new_f_obj = SimpleUploadedFile(name='test1.txt', content=self.data[:50].encode('utf-8'),
                                       content_type='text/plain')
        self.file_without_end = FileForAnalysis.objects.create(upload=new_f_obj)

    def test_clear_text(self):
        text_content = get_text_content(self.file)
        test_data = re.sub(r'[^\w\s]', ' ', self.data.lower())
        self.assertEqual(text_content, test_data)

    def test_document_count(self):
        word = Word.objects.get(name='sed')
        self.assertEqual(word.count_of_documents, 2)

    def test_update_count(self):
        word = Word.objects.get(name='pariatur')
        self.assertEqual(word.count_of_documents, 1)
