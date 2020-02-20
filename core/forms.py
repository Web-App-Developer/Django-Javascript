from django import forms
from .models import PuntoVenta, Cajero,PosPc

class CajeroForm(forms.ModelForm):

	class Meta:
		model = Cajero

		CHOICES = [('1', 'ACTIVO'), ('2', 'INACTIVO')]


		fields = [

		'nombre_cajero',
		'clave_cajero',
		'estado_cajero',
		'id_pos_pc',


		]

		labels = {

		'nombre_cajero': 'Nombre Cajero',
		'clave_cajero': 'Clave Cajero',
		'estado_cajero': 'Estado Cajero',
		'id_pos_pc': 'Terminal Asignada'


		}

		widgets = {

		'nombre_cajero': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre Cajero'}),
		'clave_cajero': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Clave Cajero'}),
		'estado_cajero': forms.Select(attrs={'class':'form-control'}),
		'id_pos_pc': forms.Select(attrs={'class':'form-control'}),

		

		}
	

		

"""class UsuariosForm(forms.ModelForm):

	class Meta:
		model = Usuarios


		fields = [

		'nombre_usuarios',
		'estado_usuarios',
		'ip_usuarios',


		]

		labels = {

		'nombre_usuarios': 'Nombre Usuario',
		'estado_usuarios': 'Estado Usuario',
		'ip_usuarios': 'IP Usuario',


		}

		widgets = {

		'nombre_usuarios': forms.TextInput(attrs={'class':'form-control'}),
		'estado_usuarios': forms.TextInput(attrs={'class':'form-control'}),
		'ip_usuarios': forms.TextInput(attrs={'class':'form-control'}),


		}"""


class PuntoVentaForm(forms.ModelForm):

	class Meta:
		model = PuntoVenta

		CHOICES = [('1', 'ACTIVO'), ('2', 'INACTIVO')]

		fields = [

		'nombre_pv', 
    	'estado_pv',
    	'user',
    	'localidad',
    

		]

		labels = {

		'nombre_pv': 'Punto de Venta', 
    	'estado_pv': 'Estado Punto de Venta',
    	'user': 'Usuario',
    	'localidad': 'Localidad',


		}

		widgets = {

		'nombre_pv': forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre Punto de Venta'}), 
    	'estado_pv': forms.Select(attrs={'class':'form-control','placeholder':'Estado Punto de Venta'}),
    	'user': forms.Select(attrs={'class':'form-control',}),
    	'localidad': forms.TextInput(attrs={'class':'form-control','placeholder':'Localidad'}),

		}


class TerminalForm(forms.ModelForm):

	class Meta:
		model = PosPc

		CHOICES = [('1', 'ACTIVO'), ('2', 'INACTIVO')]


		fields = [

		'codigo_pos_pc',
    	'estado_pos_pc',
    	'id_pv',
    

		]

		labels = {

		'codigo_pos_pc': 'Codigo Terminal', 
    	'estado_pos_pc': 'Estado Terminal',
    	'id_pv': 'Punto de Venta Asignado',


		}

		widgets = {

		'codigo_pos_pc': forms.TextInput(attrs={'class':'form-control','placeholder':'Codigo Terminal'}), 
    	'estado_pos_pc': forms.Select(attrs={'class':'form-control','placeholder':'Estado Terminal'}),
    	'id_pv': forms.Select(attrs={'class':'form-control','placeholder':'Punto de Venta'}),

		}
