from re import template
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages
from rest_framework.exceptions import NotFound
from django.contrib.auth.decorators import permission_required
from rest_framework.decorators import permission_classes
from rest_framework.pagination import PageNumberPagination

from .models import Part
from .serializers import PartSerializer
from .forms import UploadCSVFileForm
from utils.ftp import handle_uploaded_csv_file, take_files_form_csv_folder, get_data_from_csv, import_parts

class SmallPagesPagination(PageNumberPagination):  
    page_size = 40

class PartViewset(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PartSerializer
    pagination_class = SmallPagesPagination

    def get_queryset(self):
        parts = Part.objects.all()
        vin = self.request.query_params.get('vin', None)
        if vin is not None:
            parts = parts.filter(vin=vin)
            if parts:
                return parts
            else:
                raise NotFound()
        return parts

@permission_classes([IsAuthenticated])
@permission_required('admin.can_add_log_entry')
def upload_csv_from_form(request):
    template = 'parts/upload_csv.html'
    file_name = ''
    message = ''
    data = []
    context = {}
    # files = take_files_form_csv_folder()

    if request.method == 'POST':
        form = UploadCSVFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['csv_file'].name
            saved_file = handle_uploaded_csv_file(request.FILES['csv_file'])
            # data = get_data_from_csv(uploaded_filename)
            context = {'uploaded_file': uploaded_file, 'saved_file': saved_file, 'form': form, 'data': data,}
            
        else:
            message = 'Not valid file!'
    else:
        filename_from_get = request.GET.get('fff')
        is_import = request.GET.get('import')
        if filename_from_get:
            data = get_data_from_csv(filename_from_get)
            if is_import == 'yes':
                import_parts(filename_from_get)
                
        form = UploadCSVFileForm()
        context = {'file': file_name, 'form': form, 'message': message, 'data': data}

    context['files_name'] = take_files_form_csv_folder()
    return render(request, template, context)