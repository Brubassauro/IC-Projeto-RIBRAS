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
	print('Para 1 solenoide:[1]. Para 2 solenoides: [Absroverdor] [Espessura]')
	Abs=input()
	print()
	print('Entre com: [Alvo Primário] [Espessura em cm]')
	Alvo1=input()
	print('Entre com: [Alvo secundário] [Espessura em cm]')
	Alvo2=input()
	print()
	print('Entre com: [Detector DE] [Espessura em cm]')
	Detector=input()
	print('Entre com: [Detector D] [Espessura em cm]')
	D=input()
	print()
	print('Entre com: [Reacão de produção] [Energia] [Estado de carga feixe primario] [Estado de carga do feixe de interesse]')
	Feixe=input()
	print()
	arquivo.write(N+'\n'+AngD+'\n'+Abs+'\n'+Alvo1+'\n'+Alvo2+'\n'+Detector+'\n'+D+'\n'+Feixe+'\n')
	a='0'
	cont=1
	Contaminantes=[]
	while a!='':
		print('[Contaminante %s] [Estado de carga]:' %(cont))
		a=input()
		print()
		if a!='': arquivo.write(a+'\n')
		cont+=1
	arquivo.close()
		

def entrada():
	arquivo=open('Entrada.txt','r')
	contador=0
	Proj=[]
	Detector=[]
	Alvo=[]
	inc=0.5
	for linha in arquivo:
		linha=linha.replace('\n','')
		contador+=1
		if contador==1:N=int(linha)
		elif contador==2:
			AngD=int(linha)
		elif contador==3:
			if linha=='1': Abs=1
			else:
				Abs=linha.split(' ')
				Abs[1]=float(Abs[1])
		elif contador==4 or contador==5:
			A=linha.split(' ')
			A[1]=float(A[1])
			Alvo+=[A]
		elif contador==6 or contador==7:
			D=linha.split(' ')
			D[1]=float(D[1])
			Detector+=[D]
		elif contador==8:
			react=linha.split(' ')
			react[1]=float(react[1])
			E=react[0].split(')')
			E=E[0].split(',')
			E=[E[1],0,inc,int(react[3])]
			Proj+=[E]
		elif linha=='': break
		elif contador>=9:
			E=linha.split(' ')
			Proj+=[[E[0],0,inc,int(E[1])]]
	main(N,Proj,Alvo,Detector,AngD,react,Abs)

# ====================================================================================================== #
# IDENTIFICA A PARTICULA E A CARGA

def particula(Elemento):
	q=Elemento[3]
	c=0
	m=Elemento[0]
	for i in range(len(m)):
		if 'A'>m[i]: c+=1
		else: break
	return int(m[:c]),q

# ====================================================================================================== #
# FAZ O CALCULO PARA O BP DAS PARTICULAS E PARA CORRENTE NO SOLENOIDE

def bp(Proj):
	m,q=particula(Proj[0])
	bp2=2*m*Proj[0][1]/(q**2)
	for i in range(len(Proj)-1):
		m,q=particula(Proj[1+i])
		Proj[1+i][1]=bp2*(q**2)/(2*m)
	return Proj

def corrente1(Proj):
	m,q=particula(Proj[0])
	bp=np.sqrt(2*m*Proj[0][1])/q
	I=round(5.09103*bp,1)
	return str(I)

def corrente2(Proj):
	m,q=particula(Proj[0])
	bp=np.sqrt(2*m*Proj[0][1])/q
	I=round(4.39528*bp,1)
	return str(I)

def Vterm(react):
	Vterm=round(float(react[1])/(float(react[2])+1),1)
	return str(Vterm)

# ====================================================================================================== #
# COLOCA INDICES NAS MASSAS ATOMICAS DOS ELEMETOS

def elemento(elemento):
	s=''
	for i in range(len(elemento)):
		if elemento[i]=='1':s+='¹'
		elif elemento[i]=='2':s+='²'
		elif elemento[i]=='3':s+='³'
		elif elemento[i]=='4':s+='⁴'
		elif elemento[i]=='5':s+='⁵'
		elif elemento[i]=='6':s+='⁶'
		elif elemento[i]=='7':s+='⁷'
		elif elemento[i]=='8':s+='⁸'
		elif elemento[i]=='9':s+='⁹'
		else: s+=elemento[i]
	return s

def elemento_latex(elemento):
	s='$^{'
	c=0
	for i in range(len(elemento)):
		if elemento[i]=='1':s+='1'
		elif elemento[i]=='2':s+='2'
		elif elemento[i]=='3':s+='3'
		elif elemento[i]=='4':s+='4'
		elif elemento[i]=='5':s+='5'
		elif elemento[i]=='6':s+='6'
		elif elemento[i]=='7':s+='7'
		elif elemento[i]=='8':s+='8'
		elif elemento[i]=='9':s+='9'
		else: break
		c+=1
	s+='}$'+elemento[c:]
	return s


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

def input_kineq(Elemento,Absb,Energia,Angulo,react):
	arquivo=open('kineq_in.txt','w')
	if react==0: arquivo.write('%s(%s,%s)\nfuna %s,%s,%s,1\ngos\nend\n' %(Absb,Elemento,Elemento,Energia,Angulo,Angulo))
	else:arquivo.write('%s\nfuna %s,%s,%s,1\ngos\nend\n' %(react[0],Energia,Angulo,Angulo))
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
	x=int(Ang+0.5*np.random.randn(1)[0])
	return x

# ====================================================================================================== #
# GERADOR DE PDF


def gera_pdf(N,Proj,Alvo,Detector,AngD,react,Abs):
	
	arq=open('Relatorio.tex','w')


	arq.write(r'\d'+'ocumentclass{article}\n'+r'\u'+'sepackage{graphicx}\n'+r'\u'+'sepackage{amsmath}\n'+r'\u'+'sepackage{geometry}\n')
	arq.write(r'\t'+'itle{'+r'\v'+'space{-3cm}Planejamento do experimento '+elemento_latex(Proj[0][0])+'+'+elemento_latex(Alvo[1][0])+'}\n')
	arq.write(r'\a'+'uthor{}\n'+r'\d'+'ate{}\n'+r'\b'+'egin{document}\n'+r'\hoffset=0cm'+'\n'+r'\m'+'aketitle\n'+r'\s'+r'ection*{Informa\c{c}\~oes de entrada}\ '+'\n'+r'\begin{itemize}'+'\n')
	nome=react[0].split('(')[1].split(',')[0]
	arq.write(r'\item Feixe prim'+r'\''+'ario: '+elemento_latex(nome)+' $E_{lab}='+str(react[1])+'MeV$\n\n')
	arq.write(r'\item Rea\c{c}\~ao de produ\c{c}\~ao: '+elemento_latex(Alvo[0][0])+'('+elemento_latex(nome)+','+elemento_latex(Proj[0][0])+')\n\n')
	arq.write(r'\item Feixe de interesse: '+elemento_latex(Proj[0][0])+' $E_{lab}='+str(round(Proj[0][1],1))+'MeV$\n\n')
	arq.write(r'\item Contaminantes: ')
	texto=''
	for i in range(len(Proj)-1):
		texto+=elemento_latex(Proj[1+i][0])+' $E_{lab} = '+str(round(Proj[1+i][1],1))+'MeV$  |  '
	texto=texto[:len(texto)-len('  |  ')]
	arq.write(texto+'\n\n')
	arq.write(r'\item Alvo prim\'ario: '+elemento_latex(Alvo[0][0])+' $'+str(round(10000*Alvo[0][1],1))+r'\mu$$m$  |  Alvo secund\'ario '+elemento_latex(Alvo[1][0])+' $'+str(round(10000*Alvo[1][1],1))+'\mu$$m$\n\n')
	arq.write('\item Detector dE: '+elemento_latex(Detector[0][0])+' '+str(round(10000*Detector[0][1],0))+'$\mu$$m$  |  Detector E: '+elemento_latex(Detector[1][0])+' $'+str(round(10000*Detector[1][1],0))+'\mu$$m$\n\n')
	if Abs==1:arq.write('\item Corrente no solenoide: $'+corrente1(Proj)+'A$\n\n')
	else:arq.write('\item Corrente no solenoide 1: $'+corrente1(Proj)+'A$  |  Corrente no solenoide 2: $'+corrente2(Proj)+'A$\n\n')
	arq.write(r'\item Tens\~ao no terminal: '+Vterm(react)+'MV  |  '+'Absorvedor: '+elemento_latex(Abs[0])+' $'+str(round(10000*Abs[1],1))+'\mu$$m$\n\n'+r'\end{itemize}'+'\n\n')


	arq.write(r'\section*{Gr\'afico biparam\'etrico}\ '+'\n'+r'\begin{itemize}'+'\n'+r'\item N\'umero de itera\c{c}\~oes: '+str(N)+'\n\n')
	arq.write(r'\item \^Angulo do detector: '+str(AngD)+r'$^\circ$'+'\n'+r'\end{itemize}'+'\n')
	arq.write(r'\begin{figure}[h!]'+'\n'+r'\centering'+'\n'+r'\vspace{-.4cm}'+'\n'+r'\includegraphics[scale=0.7]{Biparamétrico.png}'+'\n'+r'\end{figure}'+'\n\n')
	arq.write(r'\newpage'+'\n\n')


	arq.write(r'\section*{Perdas de energia por \^angulo '+elemento_latex(Proj[0][0])+'+'+elemento_latex(Alvo[1][0])+r'}'+'\n')
	arq.write(r'\begin{table}[hp]'+'\n'+r'\center'+'\n'+r'\begin{tabular}{|l|l|l|l|l|l|l|}'+'\n'+r'\hline'+'\n')
	arq.write(r'\multicolumn{5}{|c|}{Alvo secund\'ario '+elemento_latex(Alvo[1][0])+' $'+str(round(10000*Alvo[1][1],1))+r'\mu$$m$} & \multicolumn{2}{c|}{Detectores} \\ \hline'+'\n')
	arq.write(r'E$_{entrada}$ & E$_{meio}$ & Theta & E$_{reac\tilde{a}o}$ & E$_{sa\acute{i}da}$ & dE  & E             \\ \hline'+'\n')
	tab=table(N,Proj,Alvo,Detector,AngD,react,Abs)
	for i in range(len(tab)):
		arq.write(tab[i][0]+'	&	'+tab[i][1]+'	&	'+tab[i][2]+'	&	'+tab[i][3]+'	&	'+tab[i][4]+'	&	'+tab[i][5]+'	&	'+tab[i][6]+r'	\\ \hline'+'\n')

	arq.write(r'\end{tabular}'+'\n'+r'\end{table}'+'\n'+r'\end{document}')
	arq.close()
	s=open('s.txt','w')
	s.write('s')
	s.close()
	os.system('pdflatex Relatorio.tex < s.txt >s.txt')
	os.system('xdg-open Relatorio.pdf')


# ====================================================================================================== #
# TABELA DE PERDAS DE ENERGIA POR ÂNGULO

def table(N,Proj,Alvo,Detector,AngD,react,Abs):

	E=Proj[0][1]
	linha=[]
	# ALVO
	# Stopx
	Pos=float(Alvo[1][1])/2
	input_stopx(Proj[0][0],E,Alvo[1][0],Pos)
	os.system('stopx < stopx_in.txt > stopx_out.txt')
	Ei=output_stopx()
	linha+=[[str(E),str(Ei)]]

	# Kineq
	for i in range(30):
		Ang=3*(1+i)
		input_kineq(Proj[0][0],Alvo[1][0],E,Ang,0)
		os.system('kineq < kineq_in.txt > kineq_out.txt')
		Ei=output_kineq()

		# Stopx
		Pos=(Alvo[1][1]/2)/np.cos(Ang*np.pi/180)
		input_stopx(Proj[0][0],Ei,Alvo[1][0],Pos)
		os.system('stopx < stopx_in.txt > stopx_out.txt')
		Ef=output_stopx()

		# DETECTOR
		# Stopx
		Pos=float(Detector[0][1])
		input_stopx(Proj[0][0],Ef,Detector[0][0],Pos)
		os.system('stopx < stopx_in.txt > stopx_out.txt')
		ED=output_stopx()
		EDE= Ef-ED
		if i==0: linha[0]+=[str(Ang)+r'$^\circ$',str(round(Ei,2)),str(round(Ef,2)),str(round(EDE,2)),str(round(ED,2))]
		else: linha+=[[' ',' ',str(Ang)+r'$^\circ$',str(round(Ei,2)),str(round(Ef,2)),str(round(EDE,2)),str(round(ED,2))]]
	
	for i in range(len(linha)):
		for j in range(3,7):
			if round(float(linha[i][j]),1)==0:linha[i][j]='0'
	return linha


# ====================================================================================================== #
# FUNÇÃO MAIN

def main(N,Proj,Alvo,Detector,AngD,react,Abs):
	# Proj=[E1,E2,....,En] , Ei=[Nome do elemento i, energia de i, incerteza da energia] para cada feixe i
	# Alvo/Detector=[[Nome do elemento, expessura],[Nome do elemento, expessura]]
	# N=número de partículas
	#react=[Reacao de produção, energia feixe primário, elemento de carga do feixe de interesse]

#ALVO PRIMÁRIO
	# Stopx
	Pos=float(Alvo[0][1])/2
	nome=react[0].split('(')[1].split(',')[0]
	input_stopx(nome,react[1],Alvo[0][0],Pos)
	os.system('stopx < stopx_in.txt > stopx_out.txt')
	E=output_stopx()

	# Kineq
	Ang=4
	input_kineq(nome,Alvo[0][0],E,Ang,react)
	os.system('kineq < kineq_in.txt > kineq_out.txt')
	E=output_kineq()

	# Stopx
	Pos=(Alvo[0][1]-Pos)/np.cos(Ang*np.pi/180)
	input_stopx(Proj[0][0],E,Alvo[0][0],Pos)
	os.system('stopx < stopx_in.txt > stopx_out.txt')
	E=output_stopx()


# ABSORVERDOR NO CASO DE 2 SOLENOIDES
	if Abs!=1:
		# Stopx
		Pos=float(Abs[1])/2
		input_stopx(Proj[0][0],E,Abs[0],Pos)
		os.system('stopx < stopx_in.txt > stopx_out.txt')
		E=output_stopx()

		# Kineq
		Ang=4
		input_kineq(Proj[0][0],Abs[0],E,Ang,0)
		os.system('kineq < kineq_in.txt > kineq_out.txt')
		E=output_kineq()

		# Stopx
		Pos=(Abs[1]-Pos)/np.cos(Ang*np.pi/180)
		input_stopx(Proj[0][0],E,Abs[0],Pos)
		os.system('stopx < stopx_in.txt > stopx_out.txt')
		E=output_stopx()



# ALVO SECUNDÁRIO
	Proj[0][1]=float(E)-0.2
	Proj=bp(Proj)
	Xplot=[0]*len(Proj)
	Yplot=[0]*len(Proj)
	for j in range(len(Proj)):
		X=[0]*N
		Y=[0]*N
		E_lista=Proj[j][1]+np.random.randn(N)*Proj[j][2]
		for n in range(N):

			# Stopx
			Pos=prob_posicao(Alvo[1][1])
			input_stopx(Proj[j][0],E_lista[n],Alvo[1][0],Pos)
			os.system('stopx < stopx_in.txt > stopx_out.txt')
			E=output_stopx()
			# Kineq
			Ang=prob_angulo(AngD)
			input_kineq(Proj[j][0],Alvo[1][0],E,Ang,0)
			os.system('kineq < kineq_in.txt > kineq_out.txt')
			E=output_kineq()
			# Stopx
			Pos=(Alvo[1][1]-Pos)/np.cos(Ang*np.pi/180)
			input_stopx(Proj[j][0],E,Alvo[1][0],Pos)
			os.system('stopx < stopx_in.txt > stopx_out.txt')
			E=output_stopx()

			# DETECTOR
			# Stopx
			Pos=2*prob_posicao(Detector[0][1])
			input_stopx(Proj[j][0],E,Detector[0][0],Pos)
			os.system('stopx < stopx_in.txt > stopx_out.txt')
			Ef=output_stopx()
			# Kineq
			#Ang=prob_angulo(AngD)
			#input_kineq(Proj[j][0],Detector[0],Ef,Ang,0)
			#os.system('kineq < kineq_in.txt > kineq_out.txt')
			#Ef=output_kineq()
			# Stopx
			#Pos=(Detector[1]-Pos)/np.cos(Ang*np.pi/180)
			#input_stopx(Proj[j][0],Ef,Detector[0],Pos)
			#os.system('stopx < stopx_in.txt > stopx_out.txt')
			#Ef=output_stopx()
			DE= E-Ef
			Incerteza=np.random.randn(1)[0]*2*DE/100
			Y[n]=DE+Incerteza
			X[n]=E+Incerteza

		contador=0
		while contador<len(X):
			if X[contador]==Y[contador]:
				X.pop(contador)
				Y.pop(contador)
			else: contador+=1
				
		plt.scatter(X,Y,s=3,label=elemento(Proj[j][0]))
		Xplot[j]=X
		Yplot[j]=Y

	title='Gráfico Biparamétrico | Theta='+str(AngD)+'° | '+str(N)+' Iterações'
	#plt.title(title)
	plt.xlabel('E+DE (MeV)')
	plt.ylabel('DE (MeV)')
	plt.legend()
	plt.xlim(0)
	plt.ylim(0)
	plt.grid()
	plt.savefig('Biparamétrico.png')
	#plt.show()
	plt.close()
	gera_pdf(N,Proj,Alvo,Detector,AngD,react,Abs)
	open('Relatório.pdf')

Open()
