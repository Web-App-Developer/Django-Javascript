from django.urls import path,include
from django.conf.urls import url
from .views import Home,PuntoventaViews,CajeroViews,TermnalesViews,CajeroCreate,Reportes,PuntoVentaCreate,TerminalCreate,CajeroUpdate,CajeroDelete,cajero_inactivar,PuntoVentaUpdate,puntoventa_inactivar,TerminalUpdate,terminal_inactivar, ajax_reportes
from django.contrib.auth import views as auth_views





urlpatterns = [
    #path('admin/', admin.site.urls),
    path('',Home.as_view(),name='home'),
    path('login/',auth_views.LoginView.as_view(template_name='login/login-page.html'),
    	name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='login/login-page.html'),
    	name='logout'),
    #Terminales
    path('terminalesall', TermnalesViews.as_view(), name='terminalesall'),
    url(r'^terminal_crear$', TerminalCreate.as_view(),name='terminal_crear'),
    path('terminal_editar/<pk>', TerminalUpdate.as_view(),name='terminal_editar'),
    path('terminal_eliminar/<id_pos_pc>', terminal_inactivar, name='terminal_eliminar'),

    #Puntos de Venta
    path('allpv', PuntoventaViews.as_view(), name='allpv'),
    url(r'^puntoventa_crear$', PuntoVentaCreate.as_view(),name='puntoventa_crear'),
    path('puntoventa_editar/<pk>', PuntoVentaUpdate.as_view(),name='puntoventa_editar'),
    path('puntoventa_eliminar/<id_pv>', puntoventa_inactivar, name='puntoventa_eliminar'),
    
    #Cajeros
    url(r'^cajeros_crear$', CajeroCreate.as_view(),name='cajeros_crear'),
    path('cajerosall', CajeroViews.as_view(), name='cajerosall'),
    path('cajeros_editar/<pk>', CajeroUpdate.as_view(), name='cajeros_editar'),
    path('cajeros_eliminar/<id_cajero>', cajero_inactivar, name='cajeros_eliminar'),
    
    #Reportes
    path('reportes', Reportes.as_view(), name='Reportes'),
    path('ajax_reportes', ajax_reportes, name='ajax_reportes')

]
