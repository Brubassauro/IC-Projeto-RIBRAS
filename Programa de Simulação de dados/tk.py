import matplotlib.pyplot as plt
from tkinter import *

window = Tk()
window.title("Biparamétrico")

def close_window():
	window.destroy()
	exit()

def desenhar():
	Nome1 = str(Nome1.get())
	E1 = str(E1.get())
	Ncont = str(Ncont.get())
	N = str(N.get())
	Inc = str(Inc.get())
	NomeAlvo = str(NomeAlvo.get())
	WidAlvo = str(WidAlvo.get())
	NomeDet = str(NomeDet.get())
	WidDet = str(WidDet.get())
	Contaminantes(Ncont)

def Contaminantes(Ncont):
	contaminantes= Tk()
	contaminantes.title('Contaminantes')
	Label (contaminantes, text="Nome") .grid(row=1, column=1, sticky=W)
	Cont=[0]*Ncont
	for i in range(Ncont):
		Cont[i]=Entry(window, width=10, bg="white")
		Cont[i].grid(row=i+1, column=1, sticky=W)
	Button(contaminantes, text="Sair", width= 8, command=close_window) .grid(row=12, column=1,sticky=W)
	Button(contaminantes, text="Iniciar", width=8, command=desenhar) .grid(row=12, column=0, sticky=W)

	contaminantes.mainloop()	

	# Entradas
N=Entry(window, width=10, bg="white")
N.grid(row=2, column=4, sticky=W)
Label (window, text="       ") .grid(row=3, column=4, sticky=W)
Inc= Entry(window, width=10, bg="white")
Inc.grid(row=5, column=4, sticky=W)
Angulo= Entry(window, width=10, bg="white")
Angulo.grid(row=7, column=4, sticky=W)
Nome1=Entry(window, width=10, bg="white")
Nome1.grid(row=2, column=1, sticky=W)
E1=Entry(window, width=10, bg="white")
E1.grid(row=2, column=2, sticky=W)
Ncont=Entry(window, width=10, bg="white")
Ncont.grid(row=4, column=1, sticky=W)

	# Textos
Label (window, text="Nome") .grid(row=1, column=1, sticky=W)
Label (window, text="Energia (MeV)") .grid(row=1, column=2, sticky=W)
Label (window, text="Feixe de interesse") .grid(row=2, column=0, sticky=W)
Label (window, text="Nº de contaminantes") .grid(row=4, column=0, sticky=W)
Label (window, text="Alvo") .grid(row=10, column=0, sticky=W)
Label (window, text="Detector") .grid(row=11, column=0, sticky=W)
Label (window, text="       ") .grid(row=1, column=3, sticky=W)
Label (window, text="Nome") .grid(row=9, column=1, sticky=W)
Label (window, text="Espessura (cm)") .grid(row=9, column=2, sticky=W)
Label (window, text="Nº de iterações") .grid(row=1, column=4, sticky=W)
Label (window, text="Incerteza (MeV)") .grid(row=4, column=4, sticky=W)
Label (window, text="Ang do detector (º)") .grid(row=6, column=4, sticky=W)

	# Absorvedores entrada
NomeAlvo=Entry(window, width=10, bg="white")
NomeAlvo.grid(row=10, column=1, sticky=W)
WidAlvo=Entry(window, width=10, bg="white")
WidAlvo.grid(row=10, column=2, sticky=W)
NomeDet=Entry(window, width=10, bg="white")
NomeDet.grid(row=11, column=1, sticky=W)
WidDet=Entry(window, width=10, bg="white")
WidDet.grid(row=11, column=2, sticky=W)

	# Botões
Button(window, text="Sair", width= 8, command=close_window) .grid(row=12, column=1,sticky=W)
Button(window, text="Iniciar", width=8, command=desenhar) .grid(row=12, column=0, sticky=W)

window.mainloop()
