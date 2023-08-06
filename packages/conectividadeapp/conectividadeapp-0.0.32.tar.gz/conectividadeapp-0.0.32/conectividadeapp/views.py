import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import View, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.db.models import Q

from dcim.models import Device, DeviceRole
from utilities.views import BulkDeleteView, ObjectEditView, ObjectListView, ObjectDeleteView

from .forms import ActivityForm, ActorForm, ActorFilterForm
from .models import Activity, Actor, OldDevice
from .filters import ActorFilter
from .tables import ActorTable


class ListConectividadeView(LoginRequiredMixin, View):
    """
    List all reg in the database.
    """
    rg = Activity.objects.all()
    dv = Device.objects.all()
    dr = DeviceRole.objects.all()

    def get(self, request):

        rg = Activity.objects.all()
        dv = Device.objects.all()
        dr = DeviceRole.objects.all()

        return render(request, 'conectividadeapp/listagem.html', {
            'registro': rg,
            'device': dv,
            'devicerole': dr,

        })

    def post(self, request):

        rg = Activity.objects.all()
        dr = DeviceRole.objects.all()
        dv = Device.objects.all()

        data = {}
        data['deviceid'] = request.POST['deviceid']
        data['devicerole'] = dr
        data['registro'] = rg
        data['device'] = dv
        data['form'] = ActivityForm()

        if data['deviceid']:
            device_ob = Device.objects.get(id=data['deviceid'])
            data['device_obj'] = device_ob
            # fazer tratamento
        else:
            data['device_obj'] = []

        return render(request, 'conectividadeapp/listagem.html', data)


class CreateactivityView(LoginRequiredMixin, View):
    def get(self, request):
        pass

    def post(self, request):

        data = {}
        data['activities'] = Activity.objects.all()

        form = ActivityForm(request.POST)

        if form.is_valid():

            if form.save():
            #fazer tratamento

                activity_ob = Activity.objects.last()

                gravadevice = OldDevice.objects.create(
                activity=activity_ob,
                name=request.POST['device_name'],
                serial=request.POST['serial'],
                mac=request.POST['mac'], 
                ipv4=request.POST['ip'],
                masc_ipv4="Test", 
                ipv6="cafe::cafe",
                masc_ipv6="::32", 
                tombo=request.POST['asset_tag'],
                site=request.POST['site'],
                model=request.POST['devicetype'], 
                rack=request.POST['rack']
                )

        return render(request, 'conectividadeapp/activity_list.html', data)
        # return redirect('conectividadeapp/activity_list.html')


class ActivityListView(LoginRequiredMixin, View):

    def get(self, request):

        # Current year
        current_year = datetime.date.today().year
        current_month = datetime.date.today().month
        current_day = datetime.date.today().day

        # Template to be rendered
        template_name = 'conectividadeapp/activity_list.html'

        # Search and Filters setup
        r = request.GET

        search = None
        year_month_day_researched = None
        year_month_researched = None
        year_researched = None

        first_activity = Activity.objects.first()

        if 'btn-search-research' in r:
            if r.get('search') is not None:
                search = r.get('search')

                activity_list = (
                    Activity.objects.filter(type__icontains=search)
                    | Activity.objects.filter(actor__name__icontains=search)
                    | Activity.objects.filter(description__icontains=search)
                ).order_by('-when')

        elif 'btn-year-month-day-research' in r:
            if r.get('year_month_day') is not None:
                year_month_day_researched = datetime.datetime.strptime(r.get('year_month_day'), '%Y-%m-%d')

                activity_list = Activity.objects.filter(
                    when__year=year_month_day_researched.year,
                    when__month=year_month_day_researched.month,
                    when__day=year_month_day_researched.day,
                ).order_by('-when')

        elif 'btn-year-month-research' in r:
            if r.get('year_month') is not None:
                year_month_researched = datetime.datetime.strptime(r.get('year_month'), '%Y-%m')

                activity_list = Activity.objects.filter(
                    when__year=year_month_researched.year,
                    when__month=year_month_researched.month,
                ).order_by('-when')

        elif 'btn-year-research' in r:
            if r.get('year') is not None:
                year_researched = datetime.datetime.strptime(r.get('year'), '%Y')

                activity_list = Activity.objects.filter(
                    when__year=year_researched.year,
                ).order_by('-when')

        else:
            activity_list = Activity.objects.all().order_by('-when')

        # Quantity of activities after the filter
        quantity = len(activity_list)

        # Context dictionary for rendering
        context = {
            'current_year': current_year,
            'current_month': current_month,
            'current_day': current_day,
            'activity_list': activity_list,
            'quantity': quantity,
            'first_activity': first_activity,
            'year_month_researched': year_month_researched,
            'year_month_day_researched': year_month_day_researched,
            'year_researched': year_researched,
        }

        return render(request, template_name, context)


class ActorView(View):
    """Single virtual circuits view, identified by ID."""

    def get(self, request, pk):
        actor = get_object_or_404(Actor.objects.filter(id=pk))

        return render(request, 'conectividadeapp/actor.html', {
            'actor': actor,
        })


class CreateActor(LoginRequiredMixin,PermissionRequiredMixin, ObjectEditView):
    permission_required = ''
    model = Actor
    queryset = Actor.objects.all()
    model_form =  ActorForm
    template_name = 'conectividadeapp/actor_edit.html'
    default_return_url = 'plugins:conectividadeapp:actor_list'


class EditActor(CreateActor):
    permission_required = ''


class ActorListView(LoginRequiredMixin, PermissionRequiredMixin, ObjectListView):
    permission_required = ''
    queryset = Actor.objects.all()
    filterset = ActorFilter
    filterset_form = ActorFilterForm
    table = ActorTable
    template_name = 'conectividadeapp/actor_list.html'


class DeleteActor(LoginRequiredMixin, PermissionRequiredMixin, ObjectDeleteView):
    permission_required = ''
    model = Actor
    default_return_url = 'plugins:conectividadeapp:actor_list'


class BulkDeleteActor(LoginRequiredMixin, PermissionRequiredMixin, BulkDeleteView):
    permission_required = ''
    queryset = Actor.objects.filter()
    table = ActorTable
    default_return_url = 'plugins:conectividadeapp:actor_list'


class ListDeviceView(LoginRequiredMixin, ListView):
    model = Device
    template_name = 'conectividadeapp/searchdevice.html'


class SearchDeviceView(LoginRequiredMixin, ListView):
    model = Device
    template_name = 'conectividadeapp/searchdeviceresult.html'

    def get_queryset(self):

        query = self.request.GET.get('q')
        object_list = Device.objects.filter(
            Q(asset_tag__icontains=query)
        )
        return object_list
