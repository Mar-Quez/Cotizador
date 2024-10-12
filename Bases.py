# --------------------------------------------------------------------
#
#
# --------------------------------------------------------------------

import psycopg2

import pandas.io.sql as psql

import pandas as pd

import numpy as np

import datetime

from tkinter.messagebox import showinfo

from datetime import datetime
from sqlalchemy import create_engine

from datetime import date

Esquema = "Aplicot"

DType={'boolean':16,
'bytea': 17,
'char':	 18,
'name':	 19,
'int8':	 23,
'int2':	 23,
'int4':	 23,
'integer':23,
'smallint': 23,
'regproc':	24,
'text':	25,
'oid':	26,
'tid':	27,
'xid':	28,
'cid':	29,
'oidvector':30,
'pg_type':	71,
'float4':	701,
'float8':	701,
'double precision':	701,
'money':	790,
'character varying':	1043,
'date':	1082,
'time':	1083,
'timestamp':	1114,
'timestamptz':	1184,
'interval':	    1186,
'numeric':	    1700,
'uuid':	        2950,
'json':	        114,
'jsonb':	    3802,
'array':	    1007}

def BD(Nombre,Columnas='*',Accion='select',Condicion='',Orden='',Valores='',Especial=''):
    # Ejemplos
    # accesar toda la base de datos BD(NOMBRE) = "select * from NOMBRE"
    # Borrar un registro BD(NOMBRE,,delete,"COLXX"='30' and "COLYY"='23') = "delete from NOMBRE where "COLXX"='30' and "COLYY"='23'"
    # Condicion debe incorporar la palabra
    Accion = Accion.upper()
    if Accion in ["INSERT INTO",'UPDATE','DELETE']:
        Columnas=''
    if Condicion!='':
        Condicion="where "+Condicion
    Comando=0
    if Accion in ["update",'UPDATE']:
        Comando=1
    if Orden!='':
        Orden="order by "+'%s'%(Orden)
    Nombre=""" "Aplicot"."%s" """%(Nombre)
    conexion = psycopg2.connect(
        host="localhost", dbname="Cotiza", user="postgres", password="Nitram65")
    cursor = conexion.cursor()
    if Comando == 0:
        if Accion in ["insert into","INSERT INTO"]:
            if Columnas != "*":
                Valores =str(tuple(Valores))
                query="%s %s %s VALUES %s %s "%(Accion,Nombre,Columnas,Valores,Especial)
            else:
                Valores =str(tuple(Valores))
                query="%s %s values %s "%(Accion,Nombre,Valores)
        else:
            query="%s %s from %s %s %s %s"%(Accion,Columnas,Nombre,Condicion,Orden,Especial)
    else:
        query = "%s %s SET %s %s" % (Accion,Nombre,Valores, Condicion)
    cursor.execute(query)
    if Comando==0:
        if Accion in ["insert into","INSERT INTO","delete","DELETE"]:
            Registros=True
        else:
            Registros = cursor.fetchall()
    else:
        Registros=True
    conexion.commit()
    cursor.close()
    return(Registros)



def UBD(Nombre,Columnas='',Condicion='',Valores=''):
    # Ejemplos
    # accesar toda la base de datos BD(NOMBRE) = "select * from NOMBRE"
    # Borrar un registro BD(NOMBRE,,delete,"COLXX"='30' and "COLYY"='23') = "delete from NOMBRE where "COLXX"='30' and "COLYY"='23'"
    # Condicion debe incorporar la palabra
    Accion='UPDATE'
    if Condicion!='':
        Condicion="where "+Condicion
    Nombre=""" "%s"."%s" """%(Esquema,Nombre)
    conexion = psycopg2.connect(host="localhost", dbname=BaseDatos, user="postgres", password="Nitram65")
    cursor = conexion.cursor()
    Val = ", ".join(list(map(lambda x,y:'"'+x+'"'+" = "+"'"+str(y)+"'",Columnas,Valores)))
    Val = Val
    query = "%s %s SET %s %s" % (Accion,Nombre,Val, Condicion)
    cursor.execute(query)
    Registros=True
    conexion.commit()
    cursor.close()
    return(Registros)

def BDInfo(Nombre):
    # Ejemplos
    # Description 0 Nombre de las columnas  1 tipo de dato  2 display size   4 precision  5 decimales en el
    # 23 Integer   16 boolean   1082  date   701  double
    engine = create_engine('postgresql+psycopg2://postgres:Nitram65@localhost/Cotiza')
    query = "select * from INFORMATION_SCHEMA.COLUMNS WHERE table_name = '%s'  ORDER BY ordinal_position" % (Nombre)
    Selec = pd.read_sql_query(query, engine)
    engine.dispose()
    Selec = Selec[['column_name', 'data_type', 'character_maximum_length','column_default']]
    Selec.columns = ('Name', 'Ntype', 'Max','Default')
    Selec['Tipos'] = Selec['Ntype'].map(DType)
    Selec.loc[Selec['Ntype'] == 'boolean', 'Max'] = 6
    Selec.loc[Selec['Ntype'] == 'integer', 'Max'] = 8
    Selec.loc[Selec['Ntype'] == 'smallint', 'Max'] = 4
    Selec.loc[Selec['Ntype'] == 'date', 'Max'] = 13
    Selec.loc[Selec['Ntype'] == 'text', 'Max'] = 60
    Selec.loc[Selec['Ntype'] == 'double precision', 'Max'] = 14
    # Selec['Max'].replace(np.nan, 15, inplace=True)
    Selec.replace({'Max': {np.nan: 15}}, inplace=True)
    return(Selec)

def BDtoDF(Nombre,Columnas='*',Condicion=''):
    # Solo aplica para accesr información
    Nombre=""" "%s"."%s" """%(Esquema,Nombre)
    engine = create_engine('postgresql+psycopg2://postgres:Nitram65@localhost/Cotiza')
    if Condicion!='':
        Cond="where %s"%(Condicion)
    else:
        Cond=''
    query="select %s from %s %s "%(Columnas,Nombre,Cond)
    DF=psql.read_sql(query,engine)
    engine.dispose()
    # session.bind.dispose() investigar si con esto se cierra la sesion
    return(DF)

def RecupClaves():
    Aux = BDtoDF("Claves")
    DicClaves = {campo: dict(zip(group['IDnumerico'], group['IDalfa'])) for campo, group in Aux.groupby('Campo')}
    AuxInv = {b: a for a, b in enumerate(DicClaves)}
    AuxVal = [[f"{x}.  {y}" for x, y in sorted(aux_items.items())] for aux_items in DicClaves.values()]
    Regresa = dict(zip(DicClaves.keys(),AuxVal))
    return [AuxInv,Regresa,list(DicClaves.values())]

# Duplica: Genera una duplicado de la base de datos "De" con el nuevo nombre "Como", opcionalmente puede incluir
# condiciones para seleccionar los registros a incluir en el duplicado
#De = "BasePolizas"
#Como = "BP"
#Cond= """ "IDAsegurado" = '130'"""
# Duplica(De,Como,Cond)

def RecupRela(Nombre):
    Relaciones = BDtoDF("RelaTab",Condicion=""" "Primario"='%s'"""%(Nombre))
    return Relaciones

def Duplica(De, Como, Condicion = ""):
    De ='"%s"."%s"'%(Esquema,De)
    Como = '"%s"."%s"'%(Esquema,Como)
    if Condicion == '':
        QUERY = "CREATE TABLE %s AS TABLE %s"%(Como,De)
    else:
        QUERY = "CREATE TABLE %s AS SELECT * FROM %s WHERE %s"%(Como,De,Condicion)
    conexion = psycopg2.connect(
        host="localhost", dbname=BaseDatos, user="postgres", password="Nitram65")
    cursor = conexion.cursor()
    Drop = "DROP TABLE IF EXISTS %s"%Como
    cursor.execute(Drop)
    cursor.execute(QUERY)
    conexion.commit()
    cursor.close()

def Integra(Origen,Adicion):
    Origen = '"%s"."%s"'%(Esquema,Origen)
    Adicion ='"%s"."%s"'%(Esquema,Adicion)
    QUERY = "INSERT INTO %s (SELECT * FROM %s)"%(Origen,Adicion)
    conexion = psycopg2.connect(
        host="localhost", dbname="APRES", user="postgres", password="Nitram65")
    cursor = conexion.cursor()
    cursor.execute(QUERY)
    conexion.commit()
    cursor.close()

def Alfa_a_fecha(Fecha):
    if "/" in Fecha[0:4]:
        born=datetime.strptime(Fecha,'%d/%m/%Y').date()
    elif "-" in Fecha[0:4]:
        born=datetime.strptime(Fecha,'%d-%m-%Y').date()
    elif "." in Fecha[0:4]:
        born=datetime.strptime(Fecha,'%d.%m.%Y').date()
    elif "/"==Fecha[4]:
        born=datetime.strptime(Fecha,'%Y/%m/%d').date()
    elif "."==Fecha[4]:
        born=datetime.strptime(Fecha,'%Y.%m.%d').date()
    elif "-"==Fecha[4]:
        born=datetime.strptime(Fecha,'%Y-%m-%d').date()
    return (born)


