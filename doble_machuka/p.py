import time 
import psycopg2


conexion = psycopg2.connect(host="kenodatabase-do-user-6913433-0.db.ondigitalocean.com" , dbname="KENO", user="doadmin" , password="xqnx5vsclxga1zwb", port="25060")
cursor = conexion.cursor()

cursor.execute("SELECT * FROM ADMINISTRADOR")

P = cursor.fetchall()

for x in P: print(x)

conexion.commit()
conexion.close()

class reporte:

	def consulta(self, root, user, pv, localidad, fecha):

		self.root = root
		self.user = user
		self.pv = pv
		self.localidad = localidad
		self.fecha = fecha


		conexion = psycopg2.connect(host="localhost" , dbname="KENO", user="postgres" , password="009988")
		cursor = conexion.cursor()

		cursor.execute(

			SELECT 

				LOCALIDAD.NOMBRE_LOCALIDAD,
				PUNTO_VENTA.NOMBRE_PV,
				COUNT(CARTON_KENO.ID_C_K),
				SUM(CARTON_KENO.VALOR_APUESTA_K + CARTON_CARTAS.VALOR_APUESTA_C ),	
				SUM(GANADORES_KENO.VALOR_GANADO_K +	GANADORES_CARTAS.VALOR_GANADO_C),
				(SUM(GANADORES_KENO.VALOR_GANADO_K +	GANADORES_CARTAS.VALOR_GANADO_C) - SUM(CARTON_KENO.VALOR_APUESTA_K + CARTON_CARTAS.VALOR_APUESTA_C ) ),
				(SUM(CARTON_KENO.VALOR_APUESTA_K + CARTON_CARTAS.VALOR_APUESTA_C ) * 100/ SUM(GANADORES_KENO.VALOR_GANADO_K +	GANADORES_CARTAS.VALOR_GANADO_C) ) 

			
			FROM SUPER_USUARIOS	 

				FULL OUTER JOIN USUARIOS 		 ON SUPER_USUARIOS.ID_ROOT 	 = USUARIOS.ID_ROOT 	 
				FULL OUTER JOIN PUNTO_VENTA 	 ON USUARIOS.ID_USUARIOS 	 = PUNTO_VENTA.ID_USUARIOS
				FULL OUTER JOIN LOCALIDAD 		 ON PUNTO_VENTA.ID_LOCALIDAD = LOCALIDAD.ID_LOCALIDAD
				FULL OUTER JOIN POS_PC 			 ON PUNTO_VENTA.ID_PV 		 = POS_PC.ID_PV 
				FULL OUTER JOIN CAJERO 			 ON POS_PC.ID_POS_PC 		 =  CAJERO.ID_POS_PC
				FULL OUTER JOIN CARTON_KENO 	 ON CAJERO.ID_CAJERO 		 = CARTON_KENO.ID_CAJERO
				FULL OUTER JOIN CARTON_CARTAS 	 ON CAJERO.ID_CAJERO 		 = CARTON_CARTAS.ID_CAJERO
				FULL OUTER JOIN GANADORES_KENO 	 ON CARTON_KENO.ID_C_K 		 = GANADORES_KENO.ID_C_K
				FULL OUTER JOIN GANADORES_CARTAS ON CARTON_CARTAS.ID_C_C 	 = GANADORES_CARTAS.ID_C_C


			WHERE SUPER_USUARIOS.NOMBRE_ROOT = %s 

				OR USUARIOS.NOMBRE_USUARIOS = %s 
				OR PUNTO_VENTA.NOMBRE_PV = %s 
				OR LOCALIDAD.NOMBRE_LOCALIDAD = %s 
				OR CARTON_KENO.FECHA_KENO = %s


			GROUP BY LOCALIDAD.NOMBRE_LOCALIDAD,PUNTO_VENTA.NOMBRE_PV

			, (root,user,pv,localidad,fecha) )


		TODO = cursor.fetchall()

		for x in TODO: print(x)


		conexion.commit()
		conexion.close()

