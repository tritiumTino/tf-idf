from django.shortcuts import render, redirect, get_object_or_404
from .models import FileForAnalysis, Word
from .forms import DocumentForm
from .utils import get_text_content
from collections import Counter


def index(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.save()
            return redirect('main:file_to_analysis', id=file.id)
    else:
        form = DocumentForm()
    return render(request, 'main/index.html', {
        'form': form,
    })


def file_to_analysis(request, id):
    documents_all = FileForAnalysis.objects.count()
    file = get_object_or_404(FileForAnalysis, id=id)
    text = get_text_content(file).split()
    text_counter = Counter(text).most_common(50)

    words = {}

    for word in text_counter:
        word_to_list = get_object_or_404(Word, name=word[0])
        word_idf = round(word_to_list.count_of_documents / documents_all, 4)
        words.update({word[0]: (word[1], word_idf)})

    sort_dic = sorted(words.items(), key=lambda dicx: dicx[1][1], reverse=True)
    sort_dic = dict(sort_dic)

    return render(request, 'main/analysis.html', context={'words': sort_dic})
