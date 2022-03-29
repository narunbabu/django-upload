from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
import segyio
from segpy.reader import create_reader
from segpy.writer import write_segy
from .segpy_numpy.dtypes import make_dtype
from .segpy_numpy.extract import extract_inline_3d

from .forms import BookForm
from .models import Book
from .segpy_functions import *
from .plots import get_chart
from django.shortcuts import render
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.express as px
import numpy as np



class Home(TemplateView):
    template_name = 'home.html'



def testplot(request):
    x_data = [0,1,2,3]
    y_data = [x**2 for x in x_data]
    img = np.arange(15**2).reshape((15, 15))
    plot_div = px.imshow(img).to_html()

    # plot_div = plot([Scatter(x=x_data, y=y_data,
    #                     mode='lines', name='test',
    #                     opacity=0.8, marker_color='green')],
    #            output_type='div')
    return render(request, "testplot.html", context={'plot_div': plot_div})



def upload(request):
    context = {}
    
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        # path =uploaded_file.file.name
        # print('opening...',path)
        chart = get_chart()

        # report_segy(uploaded_file)

        seg_y_dataset = create_reader(uploaded_file, endian='>')  # Non-standard Rev 1 little-endian
        inL,xL,trace_num=getILXLranges(seg_y_dataset)
        # print('inL,xL,trace_num ',inL,xL,trace_num)
        il_no=inL[10]
        # inline=getInline(seg_y_dataset,il_no)
        inline_array = extract_inline_3d(seg_y_dataset,il_no)
        # plot_div = px.imshow(inline_array.T).to_html()
        plot_div = px.imshow(inline_array.T[200:800,0:600], color_continuous_scale='RdBu_r', origin='upper').to_html()
        
        # print(il_no,inline_array.sum(axis=1))
        # f = segyio.open(path)
        # # SourceX = f.attributes(segyio.TraceField.CDP_X)[:]
        # # SourceY = f.attributes(segyio.TraceField.CDP_Y)[:]
        # my_uploaded_file = request.FILES['document'].read()
        # print(my_uploaded_file)
        # fs = FileSystemStorage()
        # name = fs.save(uploaded_file.name, uploaded_file)
        # context['url'] = fs.url(name)
    # return render(request, 'upload.html', context)
        context = {

        'chart': chart,
        'plot_div': plot_div
       
    }
    return render(request, 'upload.html',context)


def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {
        'books': books
    })


def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'upload_book.html', {
        'form': form
    })


def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')


class BookListView(ListView):
    model = Book
    template_name = 'class_book_list.html'
    context_object_name = 'books'


class UploadBookView(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('class_book_list')
    template_name = 'upload_book.html'
