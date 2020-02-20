from django.db import models
from django.contrib.auth.models import User


class PuntoVenta(models.Model):
    status = [
    ("ACTIVO", 'Activo'),
    ("INACTIVO", 'Inactivo')

]

    id_pv = models.AutoField(db_column='ID_PV', primary_key=True)  # Field name made lowercase.
    nombre_pv = models.CharField(max_length=50,blank=True,null=True)  # Field name made lowercase.
    estado_pv = models.CharField(max_length=10,choices=status,default="activo",db_column='ESTADO_PV')  # Field name made lowercase.
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    localidad = models.CharField(max_length=25,db_column='LOCALIDAD')  # Field name made lowercase

    def __str__(self):
        return '{}'.format(self.nombre_pv)

    def save(self):
        self.nombre_pv = self.nombre_pv.upper()
        self.estado_pv = self.estado_pv.upper()
        self.localidad = self.localidad.upper()
        super(PuntoVenta, self).save()


    class Meta:
        managed = False
        db_table = 'PUNTO_VENTA'

class PosPc(models.Model):
    status = [
    ("ACTIVO", 'Activo'),
    ("INACTIVO", 'Inactivo')
    ]

    id_pos_pc = models.AutoField(db_column='ID_POS_PC', primary_key=True)  # Field name made lowercase.
    codigo_pos_pc = models.IntegerField(db_column='CODIGO_POS_PC')  # Field name made lowercase.
    estado_pos_pc = models.CharField(max_length=10,choices=status,default="activo",db_column='ESTADO_POS_PC')  # Field name made lowercase.
    id_pv = models.ForeignKey('PuntoVenta', models.DO_NOTHING, db_column='ID_PV')  # Field name made lowercase.
    
    def __str__(self):
        return '{}'.format(self.codigo_pos_pc)

    def save(self):
        self.estado_pos_pc = self.estado_pos_pc.upper()
        super(PosPc, self).save()

    class Meta:
        managed = False
        db_table = 'POS_PC'



class Cajero(models.Model):
    status = [
    ("ACTIVO", 'Activo'),
    ("INACTIVO", 'Inactivo')
    ]
    id_cajero = models.AutoField(db_column='ID_CAJERO', primary_key=True)  # Field name made lowercase.
    nombre_cajero = models.CharField(max_length=15,db_column='NOMBRE_CAJERO')  # Field name made lowercase.
    clave_cajero = models.CharField(max_length=15,db_column='CLAVE_CAJERO')  # Field name made lowercase.
    estado_cajero = models.CharField(max_length=10,choices=status,default="activo",db_column='ESTADO_CAJERO')  # Field name made lowercase.
    id_pos_pc = models.ForeignKey('PosPc', models.DO_NOTHING, db_column='ID_POS_PC')  # Field name made lowercase.

    def save(self):
        self.nombre_cajero = self.nombre_cajero.upper()
        self.estado_cajero = self.estado_cajero.upper()
        super(Cajero, self).save()
    
    class Meta:
        managed = False
        db_table = 'CAJERO'

class Sorteos(models.Model):
    id_sorteos = models.AutoField(db_column='ID_SORTEOS', primary_key=True)  # Field name made lowercase.
    numeros_sorteos = models.IntegerField(db_column='NUMEROS_SORTEOS')  # Field name made lowercase.
    bonos = models.TextField(db_column='BONOS')  # Field name made lowercase.
    carta_ganadora = models.IntegerField(db_column='CARTA_GANADORA')  # Field name made lowercase.
    fecha_sorteos = models.DateField(db_column='FECHA_SORTEOS')  # Field name made lowercase.
    hora_sorteos = models.TimeField(db_column='HORA_SORTEOS')  # Field name made lowercase.
    estado_sorteos = models.TextField(db_column='ESTADO_SORTEOS')  # Field name made lowercase.
    numero_carta = models.IntegerField(db_column='NUMERO_CARTA')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SORTEOS'

class CartonCartas(models.Model):
    id_c_c = models.AutoField(db_column='ID_C_C', primary_key=True)  # Field name made lowercase.
    alta_baja = models.TextField(db_column='ALTA_BAJA')  # Field name made lowercase.
    color = models.TextField(db_column='COLOR')  # Field name made lowercase.
    valor_apuesta_c = models.IntegerField(db_column='VALOR_APUESTA_C')  # Field name made lowercase.
    fecha_cartas = models.DateField(db_column='FECHA_CARTAS')  # Field name made lowercase.
    hora_cartas = models.TimeField(db_column='HORA_CARTAS')  # Field name made lowercase.
    id_sorteos = models.ForeignKey('Sorteos', models.DO_NOTHING, db_column='ID_SORTEOS')  # Field name made lowercase.
    id_cajero = models.ForeignKey('Cajero', models.DO_NOTHING, db_column='ID_CAJERO')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CARTON_CARTAS'


class CartonKeno(models.Model):
    id_c_k = models.AutoField(db_column='ID_C_K', primary_key=True)  # Field name made lowercase.
    apuesta_keno = models.TextField(db_column='APUESTA_KENO')  # Field name made lowercase.
    valor_apuesta_k = models.IntegerField(db_column='VALOR_APUESTA_K')  # Field name made lowercase.
    fecha_keno = models.DateField(db_column='FECHA_KENO')  # Field name made lowercase.
    hora_keno = models.TimeField(db_column='HORA_KENO')  # Field name made lowercase.
    id_sorteos = models.ForeignKey('Sorteos', models.DO_NOTHING, db_column='ID_SORTEOS')  # Field name made lowercase.
    id_cajero = models.ForeignKey('Cajero', models.DO_NOTHING, db_column='ID_CAJERO')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CARTON_KENO'


class GanadoresCartas(models.Model):
    id_ganadores_c = models.AutoField(db_column='ID_GANADORES_C', primary_key=True)  # Field name made lowercase.
    valor_ganado_c = models.IntegerField(db_column='VALOR_GANADO_C')  # Field name made lowercase.
    fecha_ganadores_c = models.DateField(db_column='FECHA_GANADORES_C')  # Field name made lowercase.
    hora_ganadores_c = models.TimeField(db_column='HORA_GANADORES_C')  # Field name made lowercase.

    id_c_c = models.ForeignKey(CartonCartas, models.DO_NOTHING, db_column='ID_C_C')  # Field name made lowercase.

    id_c_c = models.ForeignKey('CartonCartas', models.DO_NOTHING, db_column='ID_C_C')  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'GANADORES_CARTAS'


class GanadoresJackpot(models.Model):
    id_ganadores_j = models.AutoField(db_column='ID_GANADORES_J', primary_key=True)  # Field name made lowercase.
    valor_ganado_j = models.IntegerField(db_column='VALOR_GANADO_J')  # Field name made lowercase.
    fecha_ganadores_j = models.DateField(db_column='FECHA_GANADORES_J')  # Field name made lowercase.
    hora_ganadores_j = models.TimeField(db_column='HORA_GANADORES_J')  # Field name made lowercase.
    id_c_k = models.IntegerField(db_column='ID_C_K')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GANADORES_JACKPOT'


class GanadoresKeno(models.Model):
    id_ganadores_k = models.AutoField(db_column='ID_GANADORES_K', primary_key=True)  # Field name made lowercase.
    valor_ganado_k = models.IntegerField(db_column='VALOR_GANADO_K')  # Field name made lowercase.
    fecha_ganadores_k = models.DateField(db_column='FECHA_GANADORES_K')  # Field name made lowercase.
    hora_ganadores_k = models.TimeField(db_column='HORA_GANADORES_K')  # Field name made lowercase.
    id_c_k = models.IntegerField(db_column='ID_C_K')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GANADORES_KENO'


class Jackpot(models.Model):
    id_jackpot = models.AutoField(db_column='ID_JACKPOT', primary_key=True)  # Field name made lowercase.
    monto_actual = models.IntegerField(db_column='MONTO_ACTUAL')  # Field name made lowercase.
    monto_activacion_j = models.IntegerField(db_column='MONTO_ACTIVACION_J')  # Field name made lowercase.
    activacion_bono = models.IntegerField(db_column='ACTIVACION_BONO')  # Field name made lowercase.
    fecha_jackpot = models.DateField(db_column='FECHA_JACKPOT')  # Field name made lowercase.
    hora_jackpot = models.TimeField(db_column='HORA_JACKPOT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'JACKPOT'

class Localidad(models.Model):
    id_localidad = models.AutoField(db_column='ID_LOCALIDAD', primary_key=True)
    nombre_localidad = models.CharField(max_length=15,db_column='NOMBRE_LOCALIDAD')


    class Meta:
        managed = False
        db_table = 'LOCALIDAD'


