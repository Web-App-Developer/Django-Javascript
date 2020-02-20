
from django.shortcuts import render, redirect
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,TemplateView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import CajeroForm,PuntoVentaForm,TerminalForm
from django.http import HttpResponse, JsonResponse
import json
from django.db.models import Count


from django.template.response import TemplateResponse
from django.db.models import Sum
from django.db.models import Q
import datetime

# Create your views here.
class Home(LoginRequiredMixin,TemplateView):

    template_name=	'dashboard.html'
    login_url='/login'
    context_object_name='obj'



# class Reportes(LoginRequiredMixin,ListView):
class Reportes(ListView):
    
    model:CartonKeno
    template_name=	'reportes.html'
    context_object_name='obj'
    queryset = []
    allset = CartonKeno.objects.all()
    allset_aggregate = allset.values('id_cajero__id_pos_pc__id_pv__localidad', 'id_cajero__id_pos_pc__id_pv__nombre_pv').order_by('id_cajero__id_pos_pc__id_pv__localidad').annotate(tickets=Count('id_c_k'), ventas=Sum('valor_apuesta_k'))
    queryset.append(allset_aggregate)

    model:PuntoVenta
    filterset_localidad = PuntoVenta.objects.values('localidad').annotate(dcount=Count('localidad'))
    queryset.append(filterset_localidad)

    filterset_pdv = PuntoVenta.objects.values('nombre_pv').annotate(dcount=Count('nombre_pv'))
    queryset.append(filterset_pdv)

    allset_carton_charts = CartonCartas.objects.all()
    allset_carton_charts_aggregate = allset_carton_charts.values('id_cajero__id_pos_pc__id_pv__localidad', 'id_cajero__id_pos_pc__id_pv__nombre_pv').order_by('id_cajero__id_pos_pc__id_pv__localidad').annotate(tickets=Count('id_c_c'), ventas=Sum('valor_apuesta_c'))
    queryset.append(allset_carton_charts_aggregate)


def ajax_reportes(request):
    # get post data
    localidad = request.POST.get('localidad') # localidad
    nombre_pv = request.POST.get('nombre_pv') # nombre_pv
    selecclonar = request.POST.get('selecclonar') # selecclonar (hoy, selecclone de)
    inicial = request.POST.get('inicial') # inicial date
    final = request.POST.get('final') # final date
    # print(localidad)
    # response queryset as a list
    queryset = []

    # count and sum
    tickets = 0
    ventas = 0
    premios = 0
    saldo = 10
    percentage = 10

    if localidad == "" and nombre_pv == "":
        # get all QuerySet
        # allset_not_group = CartonKeno.objects.all()
        allset = CartonKeno.objects.values('id_cajero').order_by('id_cajero').annotate(count=Count('id_cajero'))
        allset_aggregate = allset.values('id_cajero__id_pos_pc__id_pv__localidad', 'id_cajero__id_pos_pc__id_pv__nombre_pv').order_by('id_cajero__id_pos_pc__id_pv__localidad').annotate(tickets=Count('id_c_k'), ventas=Sum('valor_apuesta_k'))
        # append all set for datatable

        queryset.append(allset_aggregate)
    else:   	 
        # filtered QuerySet
        # print (request.POST)
        # filterd_set = CartonKeno.objects.all().filter( fecha_keno__range=[inicial, final] ).filter( id_cajero__id_pos_pc__id_pv__localidad=localidad ).filter( id_cajero__id_pos_pc__id_pv__nombre_pv=nombre_pv )
        filterd_set = CartonKeno.objects.all().filter( id_cajero__id_pos_pc__id_pv__localidad=localidad ).filter( id_cajero__id_pos_pc__id_pv__nombre_pv=nombre_pv )
        filterd_set_aggregate = filterd_set.values('id_cajero__id_pos_pc__id_pv__localidad', 'id_cajero__id_pos_pc__id_pv__nombre_pv').order_by('id_cajero__id_pos_pc__id_pv__localidad').annotate(tickets=Count('id_c_k'), ventas=Sum('valor_apuesta_k'))
        # append filtered set for datatable
        queryset.append(filterd_set_aggregate)

        # calculate tickets
        # Count( CartonKeno.id_ck )
        tickets = filterd_set.count()

        # calculate the ventas
        # SUM( CartonKeno.valor_apuesta_k + CartonCartas.valor_apuesta_c )
        vantas_cartonkeno = filterd_set.aggregate(Sum('valor_apuesta_k'))['valor_apuesta_k__sum']
        # b = Publisher.objects.filter(book__rating__gt=3.0).annotate(num_books=Count('book'))
        # filterd_set_cartonCarts = CartonCartas.objects.all().filter( id_cajero__id_pos_pc__id_pv__localidad=localidad ).filter( id_cajero__id_pos_pc__id_pv__nombre_pv=nombre_pv ).filter( fecha_cartas__gte=inicial ).filter( fecha_cartas__lte=final )
        filterd_set_cartonCarts = CartonCartas.objects.all().filter( id_cajero__id_pos_pc__id_pv__localidad=localidad ).filter( id_cajero__id_pos_pc__id_pv__nombre_pv=nombre_pv )
        vantas_cartoncarts = filterd_set_cartonCarts.aggregate(Sum('valor_apuesta_c'))['valor_apuesta_c__sum']

        if vantas_cartonkeno is not None:
            ventas += vantas_cartonkeno

        # if vantas_cartoncarts is not None:
        #     ventas += vantas_cartoncarts




    # filterd by localidad for localidad select list		
    filterset_localidad = PuntoVenta.objects.values('localidad').annotate(dcount=Count('localidad'))
    queryset.append(filterset_localidad)

    # filterd by nombre_pv for pdv select list
    filterset_pdv = PuntoVenta.objects.values('nombre_pv').annotate(dcount=Count('nombre_pv'))
    queryset.append(filterset_pdv)

    # return Response
    # obj : queryset
    # localidad : localidad
    # nombre_pv : nombre_pv
    # selecclonar : selecclonar
    # inicial : inicial
    # final : final
    # tickets : tickets
    # ventas : ventas
    # premios : premios
    # saldo : saldo
    # percentage : percentage

    return TemplateResponse(request, 'reportes.html', {'obj':queryset, 'localidad':localidad, 'nombre_pv':nombre_pv, 'selecclonar':selecclonar, 'inicial':inicial, 'final':final, 'tickets':tickets, 'ventas':ventas, 'premios':premios, 'saldo':saldo, 'percentage':percentage})
    
    # return TemplateResponse(request, 'test.html', {'obj': queryset, 'localidad': localidad, 'nombre_pv': nombre_pv, 'sele

class CajeroCreate(LoginRequiredMixin,CreateView):
    model = Cajero
    form_class = CajeroForm
    template_name = "cajeros.html"
    context_object_name = "obj"
    success_url = reverse_lazy('core:cajerosall')
    login_url='/login'

    def form_valid(self, form):
        form.instance.user = self.request.user.id
        return super().form_valid(form)

class CajeroViews(LoginRequiredMixin,ListView):
    Model:Cajero
    template_name="cajerosall.html"
    context_object_name="obj"
    #queryset = Cajero.objects.all()
    login_url='/login'

    def get_queryset(self, *args, **kwargs):
        return Cajero.objects.filter(id_pos_pc__id_pv__user=self.request.user)

class CajeroUpdate(LoginRequiredMixin,UpdateView):
    model = Cajero
    form_class = CajeroForm
    template_name = "cajeros_edit.html"
    success_url = reverse_lazy('core:cajerosall')
    context_object_name = "obj"


    def form_valid(self, form):
        form.instance.user = self.request.user.id
        return super().form_valid(form)

class CajeroDelete(LoginRequiredMixin,DeleteView):
    model = Cajero
    context_object_name = "obj"
    form_class = CajeroForm
    template_name = "cajeros_delete.html"
    success_url = reverse_lazy('core:cajerosall')
    login_url='/login'

    def form_valid(self, form):
        form.instance.user = self.request.user.id
        return super().form_valid(form)

def cajero_inactivar(request, id_cajero):
    template_name = 'cajeros_delete.html'
    contexto = {}
    cajero = Cajero.objects.filter(pk=id_cajero).first()

    if not cajero:
        return HttpResponse('Cajero no encontrado' + str(id_cajero))

    if request.method=='GET':
        contexto={'obj':cajero}

    if request.method=='POST':
        cajero.estado_cajero="inactivo"
        cajero.save()
        contexto={'obj':'OK'}
        return HttpResponse('Cajero inactivado')

    return render(request,template_name,contexto)

class PuntoventaViews(LoginRequiredMixin,ListView):
    Model:PuntoVenta
    template_name="Allpv.html"
    context_object_name="obj"
    #queryset = PuntoVenta.objects.all()
    login_url='/login'

    def get_queryset(self, *args, **kwargs):
        return PuntoVenta.objects.filter(user=self.request.user)

class PuntoVentaCreate(CreateView):
    model = PuntoVenta
    form_class = PuntoVentaForm
    template_name = "puntoventa.html"
    success_url = reverse_lazy('core:allpv')

class PuntoVentaUpdate(LoginRequiredMixin,UpdateView):
    model = PuntoVenta
    form_class = PuntoVentaForm
    template_name = "puntoventa_edit.html"
    success_url = reverse_lazy('core:allpv')
    context_object_name = "obj"


    """def form_valid(self, form):
        form.instance.user = self.request.user.id
        return super().form_valid(form)"""

def puntoventa_inactivar(request, id_pv):
    template_name = 'puntoventa_delete.html'
    contexto = {}
    puntoventa = PuntoVenta.objects.filter(pk=id_pv).first()

    if not puntoventa:
        return HttpResponse('Punto de Venta no encontrado' + str(id_pv))

    if request.method=='GET':
        contexto={'obj':puntoventa}

    if request.method=='POST':
        puntoventa.estado_pv="inactivo"
        puntoventa.save()
        contexto={'obj':'OK'}
        return HttpResponse('Punto de Venta inactivado')

    return render(request,template_name,contexto)

class TermnalesViews(LoginRequiredMixin,ListView):
    Model:PosPc
    template_name="terminalesall.html"
    context_object_name="obj"
    #queryset = PosPc.objects.all()
    login_url='/login'

    def get_queryset(self, *args, **kwargs):
        return PosPc.objects.filter(id_pv__user=self.request.user)

class TerminalCreate(CreateView):
    model = PosPc
    form_class = TerminalForm
    template_name = "terminal_create.html"
    success_url = reverse_lazy('core:terminalesall')

class TerminalUpdate(LoginRequiredMixin,UpdateView):
    model = PosPc
    form_class = TerminalForm
    template_name = "terminal_edit.html"
    success_url = reverse_lazy('core:terminalesall')
    context_object_name = "obj"


    """def form_valid(self, form):
        form.instance.user = self.request.user.id
        return super().form_valid(form)"""

def terminal_inactivar(request, id_pos_pc):
    template_name = 'terminal_delete.html'
    contexto = {}
    terminal = PosPc.objects.filter(pk=id_pos_pc).first()

    if not terminal:
        return HttpResponse('Terminal no encontrado' + str(id_pv))

    if request.method=='GET':
        contexto={'obj':terminal}

    if request.method=='POST':
        terminal.estado_pos_pc="inactivo"
        terminal.save()
        contexto={'obj':'OK'}
        return HttpResponse('Terminal inactivado')

    return render(request,template_name,contexto)



