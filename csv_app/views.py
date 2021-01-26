import os

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction
from django.conf import settings
from django.http import HttpResponse, Http404

from csv_app.forms import ColumnFormSet, SchemaForm
from csv_app.models import Schema, DataSet
from csv_app.tasks import generate_csv_file


class SchemaCreateView(CreateView):
    model = Schema
    template_name = 'csv_app/schema_create.html'
    form_class = SchemaForm

    def get_context_data(self, **kwargs):
        data = super(SchemaCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['columns'] = ColumnFormSet(self.request.POST)
        else:
            data['columns'] = ColumnFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        columns = context['columns']
        with transaction.atomic():
            form.instance.owner = self.request.user
            self.object = form.save()
            print(self.object)
            if columns.is_valid():
                columns.instance = self.object
                columns.save()
        return super(SchemaCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('schemas_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SchemaCreateView, self).dispatch(*args, **kwargs)


class SchemaListView(ListView):
    model = Schema

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SchemaListView, self).dispatch(*args, **kwargs)


class SchemaDeleteView(DeleteView):
    model = Schema

    def get_success_url(self):
        return reverse('schemas_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SchemaDeleteView, self).dispatch(*args, **kwargs)


class SchemaUpdateView(UpdateView):
    model = Schema
    template_name = 'csv_app/schema_create.html'
    form_class = SchemaForm

    def get_context_data(self, **kwargs):
        data = super(SchemaUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['columns'] = ColumnFormSet(self.request.POST, instance=self.object)
        else:
            data['columns'] = ColumnFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        columns = context['columns']
        with transaction.atomic():
            form.instance.owner = self.request.user
            self.object = form.save()
            print(columns.instance)
            print(self.object)
            if columns.is_valid():
                columns.instance = self.object
                columns.save()
        return super(SchemaUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('schemas_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SchemaUpdateView, self).dispatch(*args, **kwargs)


class DataSetCreateView(CreateView):
    model = DataSet
    fields = ['schema', ]

    def form_valid(self, form):
        num_rows = self.request.POST['num_rows']
        self.object = form.save()
        generate_csv_file.delay(form.instance.id, int(num_rows))
        return super(DataSetCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('dataset_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DataSetCreateView, self).dispatch(*args, **kwargs)


class DataSetListView(ListView):
    model = DataSet

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DataSetListView, self).dispatch(*args, **kwargs)


def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    return Http404


class DataSetDeleteView(DeleteView):
    model = DataSet

    def get_success_url(self):
        return reverse('dataset_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DataSetDeleteView, self).dispatch(*args, **kwargs)
