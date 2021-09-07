from django.db import models
from .utils import get_text_content


class Word(models.Model):
    name = models.CharField(max_length=256, verbose_name='Word', db_index=True)
    count_of_documents = models.IntegerField(verbose_name='Count of documents with the word', default=1)

    class Meta:
        verbose_name = 'Word'
        verbose_name_plural = 'Words'
        ordering = ['name']

    def __str__(self):
        return self.name


class FileForAnalysis(models.Model):
    upload = models.FileField(upload_to='media/%Y/%m/%d', verbose_name='File')
    upload_at = models.DateTimeField(auto_now_add=True, verbose_name='Upload_at')

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'
        ordering = ['-upload_at']

    def save(self, *args, **kwargs):
        instance = super(FileForAnalysis, self).save(*args, **kwargs)
        self.update_word_list()
        return instance

    def update_word_list(self):
        text_content = get_text_content(self)
        words = set(text_content.split())
        for word in words:
            try:
                saved_word = Word.objects.get(name=word)
                saved_word.count_of_documents += 1
                saved_word.save()
            except:
                new_word = Word(name=word, count_of_documents=1)
                new_word.save()
