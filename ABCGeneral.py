# ---------------------------------------------------------
#      Aplicación Generaal de Altas Bajas y Cambios
# ---------------------------------------------------------
from tkinter import *

from tkinter import ttk

import tkinter as tk

from tkinter.messagebox import showinfo

import Bases

import numpy as np

import datetime

y=60
class ABC(Frame):

    def __init__(self, master, Nombre,Liga='',ValLiga=''):
        Frame.__init__(self, master)
        self.master = master
        self.Nombre = Nombre
        self.Liga = Liga
        self.ValLiga = ValLiga
        # noinspection PyRedundantParentheses
        self.BD = """ "Aplicot"."%s" """ % self.Nombre
        self.Columnas = []
        self.BDnames = []
        self.Valores = []
        self.LargoPantalla = 1000
        self.AnchoPantalla = 500
        self.PantallaG = "%dx%d" % (self.LargoPantalla, self.AnchoPantalla)
        self.AuxInv={}
        self.result_dict={}
        self.AuxString=[]
        self.DicAux = Bases.RecupClaves()
        for a, b in enumerate(self.DicAux[0]):
            self.AuxInv.update({b: a})
            self.AuxString.append(StringVar())
        self.AuxVal = self.DicAux[1]

        # self.vista.bind("<ButtonRelease-1>", self.escoge)
        # self.vista.pack()
        self.Screen()

    def InfoBase(self):
        self.BDescrip = Bases.BDInfo(self.Nombre)
        self.BDnames = self.BDescrip[self.BDescrip.columns[0]]
        self.BDmax = np.array(self.BDescrip[self.BDescrip.columns[2]])
        self.BDmax[self.BDnames.isin(["Descripcion"])]=40
        self.BDmax[self.BDnames.isin(["Nombre"])]=20
        self.BDtipos = np.array(self.BDescrip[self.BDescrip.columns[4]])
        self.BDdefault = np.array(self.BDescrip[self.BDescrip.columns[3]])
        self.BDlong = self.BDmax * 4

    def DefCol(self):
        NoCol = len(self.BDnames)
        self.vista['columns'] = tuple(self.BDnames)
        self.vista.column("#0", width=0, stretch=NO)
        self.vista.heading("#0", text="Nada", anchor=CENTER)
        Largo = tuple(map(int, self.BDlong * (800/self.BDlong.sum())))
        for i in range(NoCol):
            self.vista.column(self.BDnames[i], anchor='w', width=Largo[i])
            self.vista.heading(self.BDnames[i], text=self.BDnames[i], anchor=CENTER)
            if self.BDtipos[i] == 701:
                self.vista.column(self.BDnames[i], anchor='e')

    def Ordena(self):
        self.RecupEntry()
        self.vista.delete(*self.vista.get_children())
        criterio = ''
        inicial = 1
        inicial = 1
        for i  in range(len(self.BDnames)):
            if self.Valores[i] != '':
                if (self.Valores[i] == "-" or self.Valores[i] == "0"):
                    forma = "DESC"
                else:
                    forma = "ASC"
                if inicial == 1:
                    if i == 0 and self.Valores[0] == '0':
                        pass
                    else:
                        criterio = '"%s" %s'%(self.BDnames[i],forma)
                        inicial = 0
                else:
                    criterio = criterio + ',  "%s" %s' % (self.BDnames[i],forma)
        if criterio != '':
            self.vista.delete(*self.vista.get_children())
        Registros = Bases.BD(self.Nombre, Orden=criterio)
        self.Despliega(Registros)

    def RecupEntry(self):
        self.Valores = []
        for i in range(len(self.BDnames)):
            if self.BDnames[i] in self.DicAux[0].keys():
                if  self.Inputi[i].get().find('.') > 0:
                    ID = self.AuxString[self.DicAux[0].get(self.BDnames[i])].get()
                    Noa=ID.find('.')
                    if Noa > 0 :
                        ID = int(ID[0:ID.find('.')])
                        self.Valores.append(ID)
                else:
                    self.Valores.append(self.Inputi[i].get())
            else:
                self.Valores.append(self.Inputi[i].get())

    def Limpia(self):
        # Limpia variables
        for i in range(len(self.BDnames)):
            self.Inputi[i].delete(0, END)

    def Despliega(self, Registros):
        i = 0
        # El indice "i"  corre sobre el numero de variables
        for row in Registros:
            Num = len(row)
            Valor = []
            for j in range(Num):
                Valor.append(row[j])
            if i % 2 == 0:
                self.vista.insert(parent='', index='end', iid=i, text='', values=Valor, tags=("evenrow",))
            else:
                self.vista.insert(parent='', index='end', iid=i, text='', values=Valor, tags=('oddrow',))
            i += 1

    def CargaBase(self):
        Criterio = '"%s"'%(self.BDnames[0])
        Registros = Bases.BD(self.Nombre, Orden=Criterio)
        self.Despliega(Registros)

    def AltaRegistro(self):
        self.RecupEntry()
        if self.ValidaFinal():
            cond = self.Valores
            if self.BDdefault[0] != "None":
                Criterio ='"%s" DESC  LIMIT 1'%(self.BDnames[0])
                Cols = '"%s"'%(self.BDnames[0])
                Ultimo = Bases.BD(self.Nombre,Columnas=Cols, Orden=Criterio)
                cond[0]=Ultimo[0][0]+1
            Bases.BD(self.Nombre, Columnas='', Accion='INSERT INTO', Orden='', Valores=cond)
            self.Limpia()
            self.vista.delete(*self.vista.get_children())
            self.CargaBase()

    def ModificaRegistro(self):
        NoCol = len(self.BDnames)
        self.RecupEntry()
        valores = ""
        for i in range(1, NoCol):
            if i < (NoCol - 1):
                valores = valores + """ "%s"='%s' , """ % (self.BDnames[i], self.Valores[i])
            else:
                valores = valores + """ "%s"='%s' """ % (self.BDnames[i], self.Valores[i])
        Condicion = '"%s"= %s' % (self.BDnames[0], self.Valores[0])
        if self.ValidaFinal():
            Bases.BD(self.Nombre, Columnas='', Accion='UPDATE', Condicion=Condicion, Valores=valores)
            self.Limpia()
            self.vista.delete(*self.vista.get_children())
            self.CargaBase()

    def escoge(self, e):
        self.Limpia()
        selected = self.vista.focus()
        valores = self.vista.item(selected, 'values')
        if len(valores) > 0:
            for i in range(len(self.BDnames)):
                if self.BDnames[i] in self.DicAux[0].keys():
                    DicVal = {}
                    for a, b in enumerate(self.DicAux[2][self.DicAux[0].get(self.BDnames[i])]):
                        DicVal.update({b: a})
                    Comp = self.DicAux[1].get(self.BDnames[i])[DicVal.get(int(valores[i]))]
#                    Comp = self.DicAux[1].get(self.BDnames[i])[int(valores[i])]
                    self.AuxString[self.DicAux[0].get(self.BDnames[i])].set(Comp)
                else:
                    self.Inputi[i].insert(0, valores[i])
        self.result_dict = dict(zip(self.BDnames, valores))

    def FiltraVinculo(self,BDvar,BDval):
        #self.RecupEntry()
        criterio = """ "%s" = %s """ % (BDvar, BDval)
        self.vista.delete(*self.vista.get_children())
        Registros = Bases.BD(self.Nombre,Condicion=criterio)
        self.Despliega(Registros)

    def Filtro(self):
        self.RecupEntry()
        criterio = ''
        inicial = 1
        for i  in range(len(self.BDnames)):
            if self.Valores[i] != '':
                if inicial == 1:
                    if i == 0 and self.Valores[0] == '0':
                        pass
                    else:
                        criterio = '"%s"  %s' % (self.BDnames[i],self.Valores[i])
                        inicial = 0
                else:
                    criterio = criterio + ' AND "%s"  %s' % (self.BDnames[i],self.Valores[i])
        if criterio != '':
            self.vista.delete(*self.vista.get_children())
        Registros = Bases.BD(self.Nombre,Condicion=criterio)
        self.Despliega(Registros)
        self.Limpia()
        self.Valores=[]

    def Borra(self):
        try:
            ID = int(self.Inputi[0].get())
            Cond = ' "%s" = %d' % (self.BDnames[0], ID)
        except:
            ID = self.Inputi[0].get()
            Cond = """ "%s" = '%s' """ % (self.BDnames[0], ID)
        Bases.BD(self.Nombre, Accion='DELETE', Condicion=Cond)
        self.Limpia()
        self.vista.delete(*self.vista.get_children())
        self.CargaBase()

    def EnPantalla(self):
        global Auxiliares, Stack
        CuadroRegistro = LabelFrame(self.Cuadrovista, text = "Registros", bg = "#b4cacf")
        CuadroRegistro.pack(fill = "x", expand = "yes", padx = 10)
        self.Etiqi = []
        self.Inputi = []
        # Declaración de etiquetas y entradas
        Largo = self.BDlong
        for i in range(len(self.BDnames)):
            Reg = Label(CuadroRegistro, text = self.BDnames[i], bg = "#b4cacf")
            Ent = Entry(CuadroRegistro, width = int(Largo[i] / 5), validate = "key",justify = "left")
            if self.BDtipos[i] == 1082:
                Ent['validatecommand'] = (Ent.register(self.ValidaFecha), "%P")
            if self.BDnames[i] in self.DicAux[0].keys():
                Ent= ttk.Combobox(CuadroRegistro,textvariable=self.AuxString[self.AuxInv.get(self.BDnames[i])])
                Ent['values'] = self.DicAux[1].get(self.BDnames[i])
            self.Etiqi.append(Reg)
            self.Inputi.append(Ent)
        # Posicion de etiquetas y entradas
        Ren = 0
        Col = 0
        Acum = 0
        # Pantalla.grid_columnconfigure(3, weight=3)
        for i in range(len(self.BDnames)):
            Acum += (self.BDlong[i] / 4 + 10 + len(self.BDnames[i]))
            self.Etiqi[i].grid(row=Ren, column=Col, pady=5, padx=5, sticky=W)
            Col += 1
            self.Inputi[i].grid(row=Ren, column=Col, padx=3, pady=5, sticky=W)
            if self.BDtipos[i] == 1082:
                self.Inputi[i]['validatecommand'] = (self.Inputi[i].register(self.ValidaFecha), "%P")

            Col += 1
            if Col > 7 and Acum > .15 * self.LargoPantalla:
                Col = 0
                Acum = 0
                Ren += 4

    # ----------------------------------------
    def AyudaSel(self, e):
        msg = f"Filtros validos:\n= <valor>  igual al valor \n<=  <valor>  menor que el valor \n<>  <valor> diferente l valor \n" \
              f"like  '%cadena%'  cadena en cualquier posición  \nlike '_00' cadena de tres caracteres los dos ultimos 00"
        showinfo(title='Ayuda de Filtros', message=msg)

    def AyudaOrd(self, e):
        msg = f"Digita '-' ó '0' para ordenar la tabla por el campo en orden descendente, cualquier otro caracter para ordenar la tabla en orden ascendente"
        showinfo(title='Criterio de orden', message=msg)

    def Aviso(self, Tex):
        Ayuda = Tk()
        Ayuda.title("Ayuda de Seleccion")
        Ayuda.geometry('600x50')
        Ayuda.overrideredirect(True)
        Ayuda.configure(bg='yellow')
        AyudaTexto = Label(Ayuda,
                           font=("Arial", 12),
                           bg='yellow',
                           text=Tex)
        # AyudaTexto.place(x=30,y=80,width=500,height=600)
        AyudaTexto.pack()
        Ayuda.after(4000, Ayuda.destroy)
        Ayuda.mainloop()

    def Barra_Lateral(self,container):
        frame = ttk.Frame(container)

        frame.columnconfigure(0, weight=1)

        Barra = LabelFrame(container, text="Vinculos", bg="#b4cacf", highlightcolor="#f5ef42")

        Vinculos = Bases.RecupRela(self.Nombre)

        if Vinculos.empty:
            Button(Barra, text='Sin Vinculos', bg="#D0D0D0", fg="#000000", width=8).grid(column=0, row=1, pady=10)
        else:
            for NumVinculo, Vinculo in enumerate(Vinculos.itertuples()):
                Button(Barra, text=Vinculo.Secundario, bg="#D0D0D0", fg="#000000", width=8,
                       command=lambda: ABC(tk.Toplevel(),Vinculo.Secundario,Liga=Vinculo.Liga,
                                          ValLiga=self.result_dict.get(Vinculo.Liga) )).grid(column=0,
                                                                row=(NumVinculo), padx=10, pady=10)


        for widget in frame.winfo_children():
            widget.grid(padx=5, pady=10)
        Barra.grid(column=1, row=0,padx=10,pady=10, sticky="n",rowspan=2)
        return frame

    def BarraAcciones(self):
        CuadroBotones = LabelFrame(self.Cuadrovista, text="Acciones", bg="#b4cacf")
        CuadroBotones.pack(fill="x", expand="yes", pady=30)

        BotonAlta = Button(CuadroBotones, text="Alta", bg="#21395c", fg="#edede8",
                           width=8, command=self.AltaRegistro)
        BotonAlta.grid(row=0, column=0, padx=10, pady=10)

        BotonCambio = Button(CuadroBotones, text="Cambia",
                             bg="#21395c", fg="#edede8", width=8, command=self.ModificaRegistro)
        BotonCambio.grid(row=0, column=2, padx=10, pady=10)

        BotonBaja = Button(CuadroBotones, text="Borra",
                           width=8, bg="#21395c", fg="#edede8", command=self.Borra)
        BotonBaja.grid(row=0, column=1, padx=10, pady=10)

        BotonLimpia = Button(CuadroBotones, text="Limpia",
                             width=8, bg="#21395c", fg="#edede8", command=self.Limpia)
        BotonLimpia.grid(row=0, column=4, padx=20, pady=10)

        BotonSeleccion = Button(CuadroBotones, text="Filtros",
                                width=8, bg="#21395c", fg="#edede8", command=self.Filtro)
        BotonSeleccion.bind("<Button-3>", self.AyudaSel)

        BotonSeleccion.grid(row=0, column=5, padx=10, pady=10)
        # 21395c
        BotonOrdena = Button(CuadroBotones, text="Ordena",
                             width=8, bg="#21395c", fg="#edede8", command=self.Ordena)
        BotonOrdena.grid(row=0, column=6, padx=10, pady=10)
        BotonOrdena.bind("<Button-3>", self.AyudaOrd)

    def ValidaFinal(self):
        checks = []
        msg = "VALIDACION: \n"
        for i in range(len(self.BDnames)):
            if self.BDtipos[i] == 16:
                if self.Valores[i] in ("t", "T", "true", "True", "TRUE", "v", "V", "verdadero", "Verdadero"):
                    self.Valores[i] = "True"
                    checks.append(True)
                elif self.Valores[i] in ("f", "F", "false", "False", "FALSE", "Falso", "falso"):
                    self.Valores[i] = "False"
                    checks.append(True)
                else:
                    msg = msg + "Campo %s: Valor logico requerido True/False \n " % (self.BDnames[i])
                    checks.append(False)
            if self.BDtipos[i] == 1082:
                try:
                    datetime.datetime.strptime(self.Valores[i], '%Y-%m-%d')
                    checks.append(True)
                except:
                    msg = msg + "Campo %s: Formato de fecha invalido \n " % (self.BDnames[i])
                    checks.append(False)
            elif self.BDtipos[i] == 23:
                if self.BDdefault[i] == "None":
                    try:
                        int(self.Valores[i])
                        checks.append(True)
                    except:
                        msg = msg + "Campo %s: Requiere valor Entero \n" % (self.BDnames[i])
                        checks.append(False)
                else:
                    checks.append(True)
            elif self.BDtipos[i] == 701:
                try:
                    float(self.Valores[i])
                    checks.append(True)
                except:
                    msg = msg + "Campo %s: Requiere valor numerico \n " % (self.BDnames[i])
                    checks.append(False)
            elif self.BDtipos[i] == 1043:
                if len(self.Valores[i]) > self.BDmax[i]:
                    msg = msg + "Campo %s: Excede el máximo de caracteres permitidos, truncar a %s caracteres \n " % (
                    self.BDnames[i], self.BDmax[i])
                    checks.append(False)
        if not all(checks):
            showinfo(title='Validación', message=msg)
        return (all(checks))

    def ValidaFecha(self, new_text):
        if len(new_text) > 10:
            return False
        checks = []
        if len(new_text) == 10:
            try:
                datetime.datetime.strptime(new_text, '%Y-%m-%d')
                checks.append(True)
            except:
                msg = f" El formato debe ser AAAA-MM-DD \n Con parametros de mes y día validos"
                showinfo(title='Fecha Invalida', message=msg)
                checks.append(False)
        for i, char in enumerate(new_text):
            # En los índices 2 y 5 deben estar los caracteres "/".
            if i in (4, 7):
                checks.append(char == "-")
            else:
                # En el resto de los casos, la única restricción es que sean
                # números entre el 0 y el 9.
                checks.append(char.isdecimal())
        # `all()` retorna verdadero si todos los chequeos son verdaderos.
        return all(checks)
    # ---------------------------------------------
    #      Inicio del programa
    # ---------------------------------------------
    def Screen(self):
        # Ventana = Tk()
        self.master.geometry(self.PantallaG)

        for child in self.master.winfo_children():
            child.destroy()
        self.master.config(bg="#b4cacf")
        self.master.title("ApliCot        ABC General        Tabla: %s" % self.Nombre)

        # Definir estilo
        estilo = ttk.Style()
        # Definir un tema
        estilo.theme_use("default")

        # Configurar los colores de la vista
        estilo.configure("Treeview", background="#a9b3e8",
                         foreground="#4f5fb8", rowheight=25, fieldbackground="#8ca7d4")

        # definir color del registro seleccionado
        estilo.map("Treeview", background=[('selected', "#3261ad")])

        # craer una cuadro de vista
        self.Marco = Frame(self.master, width=600,height=300,bg="#b4cacf")
        self.Marco.columnconfigure(0, weight=7)
        self.Marco.columnconfigure(1, weight=1)
        self.Marco.rowconfigure(0, weight=7)
        self.Marco.rowconfigure(1, weight=1)
        self.Marco.pack()
        BarraLateral=self.Barra_Lateral(self.Marco)
        BarraLateral.grid(column=1,row=0,padx=10)
        self.Cuadrovista = Frame(self.Marco, width=500, height=250, bg="#b4cacf")
        self.Cuadrovista.config(bg="#b4cacf")
        self.Cuadrovista.grid(column=0,row=0,padx=20)
        self.TreeVista = Frame(self.Cuadrovista,width=500)
        self.TreeVista.pack(pady=10)
        self.vistascroll = Scrollbar(self.TreeVista)
        self.vistascroll.pack(side=RIGHT, fill=Y)
        # crear la vista
        self.vista = ttk.Treeview(
            self.TreeVista, yscrollcommand=self.vistascroll.set, selectmode="extended")
        self.vistascroll.config(command=self.vista.yview)
        self.InfoBase()
        self.DefCol()
        if self.Liga !='' and (self.ValLiga!=None or self.ValLiga!='' ):
            self.FiltraVinculo(BDvar=self.Liga,BDval=self.ValLiga)
        else:
            self.CargaBase()
        self.vista.pack()

        # crear striped rows
        self.vista.tag_configure('evenrow', background="#ebecf7")
        self.vista.tag_configure('oddrow', background="white")

        # subir informacion a la pantalla

        self.CuadroDatos = LabelFrame(self.Cuadrovista, text="Registro", bg="#b4cacf")

        self.EnPantalla()

        self.BarraAcciones()

        self.vista.bind("<ButtonRelease-1>", self.escoge)

        self.master.mainloop()
