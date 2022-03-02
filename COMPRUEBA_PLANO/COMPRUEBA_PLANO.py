
import os

import plano

pieza= input("introduce número plano: ")

ruta = "C:\\activa\\PKS\\" + pieza +".dxf"

resultado = plano.calcula_area(ruta)

print(resultado)