import os
import matplotlib.pyplot as plt
import numpy as np

# ====================================================================================================== #
# LE O ARQUIVO DE ENTRADA E CHAMA A MAIN COM ESSAS INFORMAÇÕES

def Open():
	print('Escolha a opção de entrada:')
	print('1. Arquivo de texto "Entrada.txt"')
	print('2. Input pelo Terminal')
	print('3. Sair')
	Resp=input()
	print()
	if Resp=='1':
		entrada()
		return
	elif Resp=='2':
		input_terminal()
		entrada()
		return
	elif Resp=='3': return
	print('Entrada inválida. Entre com "1", "2" ou "3"')
	print()
	Open()

def input_terminal():
	arquivo=open('Entrada.txt','w')
	print('Número de iterações:')
	N=input()
	print()
	print('Angulo do detector em graus:')
	AngD=input()
	print()
	print('Entre com: [Alvo secundário] [Espessura em cm]')
	Alvo=input()
	print()
	print('Entre com: [Detector] [Espessura em cm]')
	Detector=input()
	print()
	print('Entre com: [Feixe de interesse] [Energia] [Incerteza E]')
	Feixe=input()
	print()
	arquivo.write(N+'\n'+AngD+'\n'+Alvo+'\n'+Detector+'\n'+Feixe+'\n')
	a='0'
	cont=1
	Contaminantes=[]
	while a!='':
		print('Contaminante %s:' %(cont))
		a=input()
		print()
		if a!='': arquivo.write(a+'\n')
		cont+=1
	arquivo.close()
		

def entrada():
	arquivo=open('Entrada.txt','r')
	contador=0
	Proj=[]
	for linha in arquivo:
		linha=linha.replace('\n','')
		contador+=1
		if contador==1:N=int(linha)
		elif contador==2:
			AngD=int(linha)
		elif contador==3:
			Alvo=linha.split(' ')
			Alvo[1]=float(Alvo[1])
		elif contador==4:
			Detector=linha.split(' ')
			Detector[1]=float(Detector[1])
		elif contador>=5 and linha!='':
			E=linha.split(' ')
			E[1]=float(E[1])
			E[2]=float(E[2])
			Proj+=[E]
	main(N,Proj,Alvo,Detector,AngD)

# ====================================================================================================== #
# GERA O ARQUIVO INPUT PARA O STOPX stopx_in.txt

def input_stopx(Nome,E,NomeAb,WidAb):
    arquivo=open('stopx_in.txt','w')
    arquivo.write('proj %s\nea %s\nabsb\n%s -%s\n\nelos\nend\n' %(Nome,E,NomeAb,WidAb))
    arquivo.close()

# ====================================================================================================== #
# LE O OUTPUT DO STOPX stopx_out.txt E RETORNA A ENERGIA 

def output_stopx():
    arquivo=open('stopx_out.txt','r')
    contador=0
    Linha=[]
    for linha in arquivo:
        if contador==21:
            Linha=linha
            Linha=Linha.replace('\n','')
            Linha=Linha.split(' ')
        contador+=1
    contador=0
    while contador<len(Linha):
        if Linha[contador]=='': Linha.pop(contador)
        else: contador+=1
    for i in range(len(Linha)):
        Linha[i]=float(Linha[i])
    if Linha==[]: return 0
    return Linha[2]

# ====================================================================================================== #
# GERA O ARQUIVO INPUT PARA O KINEQ kineq_in.txt

def input_kineq(Elemento,Absb,Energia,Angulo):
    arquivo=open('kineq_in.txt','w')
    arquivo.write('%s(%s,%s)\nfuna %s,%s,%s,1\ngos\nend\n' %(Absb,Elemento,Elemento,Energia,Angulo,Angulo))
    arquivo.close()

# ====================================================================================================== #
# LE O OUTPUT DO KINEQ kineq_out.txt E RETORNA A ENERGIA

def output_kineq():
    arquivo=open('kineq_out.txt','r')
    contador=0
    Linha=[]
    for linha in arquivo:
        if contador==24:
            Linha=linha
            Linha=Linha.replace('\n','')
            Linha=Linha.split(' ')
        contador+=1
    contador=0
    while contador<len(Linha):
        if Linha[contador]=='': Linha.pop(contador)
        else: contador+=1
    for i in range(len(Linha)):
        Linha[i]=float(Linha[i])
    if Linha==[]: return 0
    else: return Linha[3]

# ====================================================================================================== #
# FUNÇÃO PROBABILIDADE PARA O LOCAL DE REAÇÃO

def prob_posicao(Expessura):
	x=Expessura*(0.5) #+0.6*np.random.rand(1)[0])
	return x

# ====================================================================================================== #
# FUNÇÃO PROBABILIDADE PARA O ANGULO DE ESPALHAMENTO

def prob_angulo(Ang):
	x=Ang#int(Ang+1*np.random.randn(1)[0])
	return x

# ====================================================================================================== #
# FUNÇÃO MAIN

def main(N,Proj,Alvo,Detector,AngD):
# Proj=[E1,E2,....,En] , Ei=[Nome do elemento i, energia de i, incerteza da energia] para cada feixe i
# Alvo/Detector=[Nome do elemento, expessura]
# N=número de partículas
	Xplot=[0]*len(Proj)
	Yplot=[0]*len(Proj)

	for j in range(len(Proj)):
		X=[0]*N
		Y=[0]*N
		E_lista=Proj[j][1]+np.random.randn(N)*Proj[j][2]
		for n in range(N):
			# ALVO
			# Stopx
			Pos=prob_posicao(Alvo[1])
			input_stopx(Proj[j][0],E_lista[n],Alvo[0],Pos)
			os.system('stopx < stopx_in.txt > stopx_out.txt')
			E=output_stopx()
			# Kineq
			Ang=4
			input_kineq(Proj[j][0],Alvo[0],E,Ang)
			os.system('kineq < kineq_in.txt > kineq_out.txt')
			E=output_kineq()
			# Stopx
			Pos=(Alvo[1]-Pos)/np.cos(Ang*np.pi/180)
			input_stopx(Proj[j][0],E,Alvo[0],Pos)
			os.system('stopx < stopx_in.txt > stopx_out.txt')
			E=output_stopx()

			# DETECTOR
			# Stopx
			Pos=prob_posicao(Detector[1])
			input_stopx(Proj[j][0],E,Detector[0],Pos)
			os.system('stopx < stopx_in.txt > stopx_out.txt')
			Ef=output_stopx()
			# Kineq
			Ang=prob_angulo(AngD)
			input_kineq(Proj[j][0],Detector[0],Ef,Ang)
			os.system('kineq < kineq_in.txt > kineq_out.txt')
			Ef=output_kineq()
			# Stopx
			Pos=(Detector[1]-Pos)/np.cos(Ang*np.pi/180)
			input_stopx(Proj[j][0],Ef,Detector[0],Pos)
			os.system('stopx < stopx_in.txt > stopx_out.txt')
			Ef=output_stopx()
			DE= E-Ef
			Incerteza=0#np.random.randn(1)[0]*2*DE/100
			Y[n]=DE+Incerteza
			X[n]=E+Incerteza

		contador=0
		while contador<len(X):
			if X[contador]==Y[contador]:
				X.pop(contador)
				Y.pop(contador)
			else: contador+=1
				
		plt.scatter(X,Y,s=3,label=Proj[j][0])
		Xplot[j]=X
		Yplot[j]=Y

	plt.title('Gráfico Biparamétrico')
	plt.xlabel('E+DE (MeV)')
	plt.ylabel('DE (MeV)')
	plt.legend()
	plt.xlim(0)
	plt.ylim(0)
	plt.grid()
	plt.show()

Open()
