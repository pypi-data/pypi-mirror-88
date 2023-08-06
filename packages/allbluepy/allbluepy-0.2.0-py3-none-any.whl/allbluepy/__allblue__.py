# -*- coding: utf-8 -*- 
"""
Allblue retorna informações oceânicas referente a
região mais próxima as cordenadas de entrada.

Entrada:
x: Longitude (graus e decimais do grau);
y: Latitude (graus e decimais do grau);
z: Informações:
	0: Regiões oceânicas;
	1: Ecorregiões e zonas oceânicas;
        2: Zonas econômicas;
	3: Províncias;
	4: todas informações;

Saída:
	Código província 
	Ecorregião Marinha
	Província
	Região
	Soberano
	Território
	Zona
	Zona econômica
	x: Longitude mais próxima
	y: Latitude mais próxima'

Ex.:
	import allbluepy
	exem = allbluepy.Allblue()
	exem.buscar(-70, 45, 3)

	Código província                                      NWCS
	Província           Coastal - NW Atlantic Shelves Province
	x                                                      -70 <-coord mais próxima encontrada
	y                                                       44 <-coord mais próxima encontrada
     """
    
import pandas as pd
import os
import allbluepy

class Allblue():
    
    def buscar(self,x, y, z):
        cont = [0,1,2,3]
        if x > 180 or x < -180 or y > 90 or y < -90:
            raise ValueError('x dever estar entre -180 a 180 e y entre -90 a 90')
        elif z not in cont and z != 4:
            raise ValueError('z dever estar entre 0 a 4')
        else:
            lista = []
            if z == 4:
                for item in cont:
                    lista.append(self.__minimo__(x, y, item))
                lista = pd.concat(lista)
                return lista
            else: 
                return self.__minimo__(x, y, z)
        
    def __escolha_tab__(self, n):
        caminho = os.path.dirname(allbluepy.__file__) + '/'
        tabs = ['região', 'ecorregião', 'zona_economica', 'província']
        tab = pd.read_csv(caminho + tabs[n] + '.csv')
        return tab

    def __minimo__(self, long, lat, tab):
        tabela = self.__escolha_tab__(tab)
        resu = (abs(long - tabela['x']) + abs(lat - tabela['y'])).sort_values().head(1).index[0]
        return self.__columns__(resu, tab)

    def __columns__(self, i, t):
        tabela = self.__escolha_tab__(t)
        return tabela.loc[i]
