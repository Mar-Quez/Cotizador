"""
======================================================================================================================
                                 ApliCot                  Aplicacion para COTIZAR
----------------------------------------------------------------------------------------------------------------------

Es una aplicación que lleva la administración de un portafolio de reaseguro para una compañia de seguros directa
dentro de su alcance considera:

* Diferentes ramos y operaciones
* Diferentes monedas
* Multiples contratos para un mismo ramo/operacion - Moneda
* Dentro de un contrato:
    + Multiples lineas de retencion / lineas de plenos
    + Multiples coberturas
    + Seguimiento documental por reasegurador
    + Dentro de una linea de retención
        - Diferentes reaseguradores
        - Porcentajes de participación independienes por linea - reasegurador
* Contratos automaticos y facultativos
* Registro de movimientos a petición del usuario y automaticos
* Vistas de información por:
    + Contrato
    + Periodo
    + Reasegurador
    + Regulador
* Procesos automatizados para la generación de bordereaux de primas / siniestros
* Interfaces con la operación de emision, siniestros y contabiliad a traves de archivos CSV
    + Generación de diccionarios de interacción
* Procesos automatizados y programables
    + Base de tareas automatizadas
    + Opciones para generar ciclos
* Reporteria
    + Para reaseguradores
    + Para Contabilidad
    + Para reguladores
    + Para análisis técnico
    + Para análisis operativo
"""

from tkinter import *

import tkinter as tk

from tkinter.messagebox import showinfo

import Bases

import ABCGeneral

class Usuario():
    def __init__(self):
        self.BaseUsuarios()
        self.Captura()

    def BaseUsuarios(self):
        self.Users=Bases.BDtoDF("Suscriptores")

    def Captura(self):
        self.Captura=Tk()
        w = 450 # width for the Tk root
        h = 200 # height for the Tk root

        # get screen width and height
        ws = self.Captura.winfo_screenwidth() # width of the screen
        hs = self.Captura.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # set the dimensions of the screen
        # and where it is placed
        self.Captura.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.Captura.title("ApliCot     Validacion de credenciales de usuario")
        self.Captura.config(bg="#84a6cf")
        Credenciales=LabelFrame(self.Captura,text="Credenciales",bg="#84a6cf")
        Credenciales.pack(fill="x", expand="yes", padx=10)
        Usuario=Label(Credenciales,text="Alias :",pady=20,bg="#84a6cf").grid(row=0, column=0,sticky=W)
        Password=Label(Credenciales,text="Contraseña :",pady=40,bg="#84a6cf").grid(row=2, column=0,sticky=W)
        self.UsEntry=Entry(Credenciales,width=6)
        self.UsEntry.grid(row=0,column=1,sticky=W)
        self.PsEntry=Entry(Credenciales,width=12,show="*")
        self.PsEntry.grid(row=2,column=1,sticky=W)
        Credenciales.columnconfigure(3,weight=1)
        Credenciales.columnconfigure(4,weight=1)
        BValida=Button(Credenciales,text="Valida Credenciales",bg="#226ea1",fg="#edede8",padx=40,command=self.Acceso)
        BValida.grid(row=0,column=4,columnspan=2)
        BCambia=Button(Credenciales,text="Cambia  Contraseña",bg="#226ea1",fg="#edede8",padx=40,command=self.Cambia)
        BCambia.grid(row=2,column=4)


    def Acceso(self):
        if self.Valida():
            self.Captura.destroy()
            SplashScreen()


    def Valida(self):
        global VNom,VNivel
        User=self.UsEntry.get()
        Pass=self.PsEntry.get()
        Users=set(self.Users['AliasSuscrip'])
        if User in Users:
            self.Registro=self.Users[self.Users['AliasSuscrip']==User]
            self.Registro=self.Registro.reset_index()
            VPass=self.Users[self.Users['AliasSuscrip']==User]['Clave']
            VPass=list(map(str,VPass))
            VNom=self.Users[self.Users['AliasSuscrip']==User]['NombreSuscrip']
            VNom=list(map(str,VNom))
            VNivel=self.Users[self.Users['AliasSuscrip']==User]['Nivel']
            VNivel=list(map(int,VNivel))
            if Pass==VPass[0]:
                return(TRUE)
            else:
                showinfo(title='Validación de Usuario', message="Contraseña Invalida")
                return(FALSE)
        else:
            showinfo(title='Validación de Usuario', message="Usuario no registrado")
            return(FALSE)

    def Cambia(self):
        global SCambia

        if self.Valida():

            SCambia=Tk()
            w = 450 # width for the Tk root
            h = 200 # height for the Tk root

            # get screen width and height
            ws = SCambia.winfo_screenwidth() # width of the screen
            hs = SCambia.winfo_screenheight() # height of the screen

            # calculate x and y coordinates for the Tk root window
            x = (ws/2) - (w/2)
            y = (hs/2) - (h/2)

            # set the dimensions of the screen
            # and where it is placed
            SCambia.geometry('%dx%d+%d+%d' % (w, h, x, y))
            SCambia.title("ApliCot     Cambio de Contraseña")
            SCambia.config(bg="#84a6cf")
            NuevaCon=LabelFrame(SCambia,text="Contraseña",bg="#84a6cf")
            NuevaCon.pack(fill="x", expand="yes", padx=10)
            ContAnt=Label(NuevaCon,text="Anterior :",pady=20,bg="#84a6cf").grid(row=0, column=0,sticky=W)
            ContNva=Label(NuevaCon,text="Nueva   :",pady=40,bg="#84a6cf").grid(row=2, column=0,sticky=W)
            self.AntCont=Entry(NuevaCon,width=12,show="*")
            self.AntCont.grid(row=0,column=1,sticky=W)
            self.NvaCont=Entry(NuevaCon,width=12,show="*")
            self.NvaCont.grid(row=2,column=1,sticky=W)
            NuevaCon.columnconfigure(3,weight=1)
            NuevaCon.columnconfigure(4,weight=1)
            BActualiza=Button(NuevaCon,text="Cambia  Contraseña",bg="#226ea1",fg="#edede8",padx=40,command=self.Actualiza)
            BActualiza.grid(row=2,column=4)

            SCambia.mainloop()


    def Actualiza(self):
        global SCambia
        x=1
        if self.AntCont.get()==self.Registro.loc[0][6]:
            Valores="""  "Password" ='%s' """ %(self.NvaCont.get())
            Condicion=""" "IDUsuario" = '%s' """%self.Registro.loc[0][1]
            Bases.BD("Usuarios",Columnas='',Accion='UPDATE',Condicion=Condicion,Valores=Valores)
            SCambia.destroy()
        else:
            showinfo(title='Cambio de contraseña', message="Contraseña Anterior Invalida")

class Window(Frame):
    def __init__(self, master=None):
        global VNivel
        Frame.__init__(self, master)
        self.master = master
        menu = Menu(self.master)
        self.master.config(menu=menu)

        CatMenu = Menu(menu)
        ContaMenu=Menu(CatMenu,tearoff=0)
        OperMenu=Menu(CatMenu,tearoff=0)
        SuscripcionMenu=Menu(CatMenu,tearoff=0)
        TecMenu=Menu(CatMenu,tearoff=0)
        if VNivel[0] <= 1:
            TecMenu.add_command(label="Claves",command=lambda: ABCGeneral.ABC(tk.Toplevel(),"Claves"))
        CatMenu.add_cascade(label="Contable/Financiero",menu=ContaMenu)
        CatMenu.add_cascade(label="Opererativos",menu=OperMenu)
        OperMenu.add_command(label="Agentes",command=lambda: ABCGeneral.ABC(tk.Toplevel(),"Agentes"))
        OperMenu.add_command(label="Esquema Entidad/Relación",command=lambda: ABCGeneral.ABC(tk.Toplevel(),"RelaTab"))
        OperMenu.add_command(label="Monedas",command=lambda: ABCGeneral.ABC(tk.Toplevel(),"Prueba"))
        OperMenu.add_command(label="Test Operaciones",command=lambda: ABCGeneral.ABC(tk.Toplevel(),"Test01"))
        OperMenu.add_command(label="Ramos",command=lambda: ABCGeneral.ABC(tk.Toplevel(),"Prueba"))
        OperMenu.add_command(label="Reaseguradores",command=lambda: ABCGeneral.ABC(tk.Toplevel(),"Prueba"))
        OperMenu.add_command(label="Paises",command=lambda: ABCGeneral.ABC(tk.Toplevel(),"Prueba"))
        OperMenu.add_command(label="Cotizaciones",command=lambda: ABCGeneral.ABC(tk.Toplevel(),"Prueba"))
        OperMenu.add_command(label="Menus",command=lambda: ABCGeneral.ABC(tk.Toplevel(),"Prueba"))

        OperMenu.add_command(label="Tarifas",command=self.Tarifas)
        CatMenu.add_cascade(label="Propuestas", menu=SuscripcionMenu)
        SuscripcionMenu.add_command(label="Mantenimiento",command=lambda: ABCGeneral.ABC(tk.Toplevel(),"Propuestas"))
        TecMenu.add_command(label="Estatus",command=lambda: ABCGeneral.ABC(tk.Toplevel(),"Estatus"))

        CatMenu.add_cascade(label="Tecnico", menu=TecMenu)
        TecMenu.add_command(label="Mapeo de Campos",command=lambda: ABCGeneral.ABC(tk.Toplevel(),"MapaRelacion"))
        TecMenu.add_command(label="Fundamentales",command=lambda: ABCGeneral.ABC(tk.Toplevel(),"Fundamentales"))
        TecMenu.add_command(label="Usuarios",command=lambda: ABCGeneral.ABC(tk.Toplevel(),"Usuarios"))
        CatMenu.add_command(label="Salir", command=self.exitProgram)
        menu.add_cascade(label="Catalogos", menu=CatMenu)


        ContaMenu.add_command(label="Cuentas Contables",command=lambda: ABCGeneral.ABC(tk.Toplevel(),"CatCtasCon"))
        ContaMenu.add_command(label="Movimientos Contables",command=lambda: ABCGeneral.ABC(tk.Toplevel(),"MovContable"))
        ContaMenu.add_command(label="Tipos de Cambio",command=lambda: ABCGeneral.ABC(tk.Toplevel(),"TipoCambio"))


        ConMenu = Menu(menu)
        AnaMenu=Menu(ConMenu,tearoff=0)
        AnaMenu.add_command(label="Por Contrato")
        AnaMenu.add_command(label="Por Ramo")
        AnaMenu.add_command(label="Por Reasegurador")
        AnaMenu.add_command(label="Filtro Dinamico")

        ConMenu.add_command(label="Mantenimiento",command=self.ManContrat)
        ConMenu.add_command(label="Renovación")
        ConMenu.add_cascade(label="Analisis",menu=AnaMenu)
        menu.add_cascade(label="Contratos", menu=ConMenu)


        FacMenu=Menu(menu)
        FacMenu.add_command(label="Ofertas")
        FacMenu.add_command(label="Asignaciones")
        FacMenu.add_command(label="Renovaciones")
        menu.add_cascade(label="Facultativos", menu=FacMenu)

        ProMenu = Menu(menu)
        CargaMenu=Menu(ProMenu)
        CargaMenu.add_command(label="Polizas")
        CargaMenu.add_command(label="Reclamaciones")

        ProMenu.add_command(label="Actividades",command=lambda: ABCGeneral.ABC(Tk(),"Actividad"))
        ProMenu.add_cascade(label="Cargas",menu=CargaMenu)
        ProMenu.add_command(label="Procesos",command=lambda: ABCGeneral.ABC(Tk(),"Procesos"))
        ProMenu.add_command(label="Ciclos",command=lambda: ABCGeneral.ABC(Tk(),"Ciclos"))
        ProMenu.add_command(label="Estructura",command=lambda: ABCGeneral.ABC(Tk(),"EstrucProces"))
        ProMenu.add_command(label="Lanzamiento",command=self.DefCiclos)
        menu.add_cascade(label="Procesos", menu=ProMenu)

        ContaMenu = Menu(menu)
        ContaMenu.add_command(label="Estados de Cuenta")
        ContaMenu.add_command(label="Conciliación")
        ContaMenu.add_command(label="Mantenimiento Manual")
        menu.add_cascade(label="Contabilidad", menu=ContaMenu)

        NormaMenu = Menu(menu)
        NormaMenu.add_command(label="Manual de Reaseguro")
        NormaMenu.add_command(label="Apetito de riesgo")
        NormaMenu.add_command(label="Limite Máximo de Retención",command=lambda: ABCGeneral.ABC(Tk(),"LimiteMaxRet"))
        menu.add_cascade(label="Normatividad", menu=NormaMenu)

    def ManContrat(self):
        import Contratos01

    def DefCiclos(self):
        import DefCiclos

    def Tarifas(self):
        import Tarifas

    def exitProgram(self):
        exit()

def MENUS():
    global Splash
    Splash.destroy()
    ApliCot = Tk()
    w = 800 # width for the Tk root
    h = 450 # height for the Tk root

    # get screen width and height
    ws = ApliCot.winfo_screenwidth() # width of the screen
    hs = ApliCot.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen
    # and where it is placed
    ApliCot.geometry('%dx%d+%d+%d' % (w, h, x, y))
    ApliCot.call('wm', 'iconphoto', ApliCot._w, PhotoImage(file='Delta1.png'))
    app = Window(ApliCot)
    ApliCot.wm_title("ApliCot  Aplicación Universal de REAseguro")
    ApliCot.config(bg="#8bc49f")

def SplashScreen():
    global Splash,VNom
    Splash=Tk()

    w = 800 # width for the Tk root
    h = 450 # height for the Tk root

    # get screen width and height
    ws = Splash.winfo_screenwidth() # width of the screen
    hs = Splash.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen
    # and where it is placed
    Splash.geometry('%dx%d+%d+%d' % (w, h, x, y))
    #Splash.geometry("900x500")
    #Splash.eval('tk::PlaceWindow . center')
    Splash.overrideredirect(True)
    Splash.config(bg="#76b08a",relief="solid")
    AUser=StringVar()
    AUser="Sesion iniciada por: %s"%(VNom[0])
    bg=PhotoImage(file="Delta1.png")
    ApliCot=Label(Splash,text="Generador de cotizaciones ",font=('Arial',14),bg="#76b08a")
    ApliCot1=Label(Splash,text="ApliCot",font=('Arial',18),bg="#76b08a")
    Delta=Label(Splash,text="Power by: Delta Wise Consultores S.C.",font=('Arial',10),bg="#76b08a",fg="white")
    ApliCotUser=Label(Splash,text=AUser,font=('Arial',14),bg="#76b08a")
    Logo=Label(Splash,image=bg)
    ApliCot.pack(pady=30)
    ApliCot1.pack(pady=5)
    ApliCotUser.pack(pady=10)
    #Logo.pack()
    Delta.pack(pady=10,side=RIGHT)
    x=1
    Splash.after(4000,MENUS)

Usuario()

mainloop()