
import ezdxf
import math
from ezdxf import bbox
from ezdxf import groupby
import sys


def calcula_area(referencia_plano):
    try:
        doc = ezdxf.readfile(referencia_plano)
    except IOError:
        print(f"Not a DXF file or a generic I/O error.")
        sys.exit(1)
    except ezdxf.DXFStructureError:
        print(f"Invalid or corrupted DXF file.")
        sys.exit(2)
    #print(doc.header['$ACADVER'])
    #oc.header['$ACADVER']='AC1018'
    #doc.save(encoding='utf-8')
    #version_dxf=doc.header['$ACADVER']

    try:
        doc = ezdxf.readfile(referencia_plano)
    except IOError:
        print(f"Not a DXF file or a generic I/O error.")
        sys.exit(1)
    except ezdxf.DXFStructureError:
        print(f"Invalid or corrupted DXF file.")
        sys.exit(2)




    msp = doc.modelspace()

    def distancia(punto_1, punto_2):
        if type(punto_1) == tuple and type(punto_2) == tuple:
            c = tuple(map(lambda x, y: round(y - x, 3), punto_1, punto_2))
        elif type(punto_1) == tuple:
            c = tuple(map(lambda x, y: round(y - x, 3), punto_1, punto_2.format('xyz')))
        elif type(punto_2) == tuple:
            c = tuple(map(lambda x, y: round(y - x, 3), punto_1.format('xyz'), punto_2))
        else:
            c = tuple(map(lambda x, y: round(y - x, 3), punto_1, punto_2))


        """if punto_1.dxftype()=='VERTEX':
            c = tuple(map(lambda x, y: round(y - x, 3), punto_1.format('xyz'), punto_2))
        else:
            c = tuple(map(lambda x, y: round(y - x, 3), punto_1, punto_2))"""

        separacion = math.sqrt(pow(c[0],2) + pow(c[1],2))
        return separacion 

    def area_recuadro():
        extents = bbox.extents(msp)

        resultado=list(extents)

        origen= resultado[0]
        final = resultado[1]

        c = tuple(map(lambda x, y: round(y - x, 1), origen, final))
        #print(c)
        eje_x = c[0]
        eje_y = c[1]

        area_total = eje_x * eje_y
        #print(area_total)
        return area_total

    def area_poli(polilinea):
        area_dibujo = ezdxf.math.area(polilinea.points())
        #print (area_dibujo)
        return area_dibujo




    # iterate over all entities in modelspace
    msp = doc.modelspace()
    i=0
    z=0
    elementos = len(msp)
    lista_area = []
    lista_elementos=[]
    diccionario_elementos={}
    lista_capas=("GREEN", "BLACK", "YELLOW", "RED")

    """for layer in doc.layers:
        if layer.dxf.name in lista_capas:
            layer.off()
            #doc.layers.remove(layer.dxf.name)"""


    while len(msp)>len(lista_elementos):
        for e in msp:
            if e.dxf.handle not in lista_elementos:
                print(e.dxf.color)
                if e.dxf.layer in lista_capas:
                    msp.delete_entity(e)
                    break
                elif e.dxf.color !=256:
                    msp.delete_entity(e)
                    break
                else:
                     lista_elementos.append(e.dxf.handle)

    while msp.query("ARC"):
        for e in msp.query("ARC"):
            print(e.dxf.radius)
            print(e.start_point)
            print(e.end_point)
            if e.dxf.radius>4 and distancia(e.start_point, e.end_point)>1:
        
                for inicio_segmento in e.flattening(1):
                    #print(rrr)
                    if ezdxf.math.is_close_points(inicio_segmento, e.start_point,0.01):
                        p1=inicio_segmento
                
                    else:
                        msp.add_line(p1, inicio_segmento)
                        p1=inicio_segmento
                msp.delete_entity(e)
            else :
                msp.add_line(e.start_point, e.end_point)
                msp.delete_entity(e)
            doc.saveas("new_name.dxf")

    while len(msp)>=len(diccionario_elementos):
        z+=1
        if z>4000: 
            break
        for e in msp:
            if i == 0 and not e.dxf.handle in diccionario_elementos:
                if e.dxftype() == "CIRCLE":
                    print(e)
                    diccionario_elementos[e.dxf.handle]=math.pi*pow(e.dxf.radius,2)

                #if e.dxftype() == "ARC":
                    #print(e)
                    #msp.delete_entity(e)
                    #break
                if e.dxftype() == "LINE":
                    print(e)
                    hola = [e.dxf.start.xyz, e.dxf.end.xyz]
                    poli = msp.add_polyline2d(hola)
                    msp.delete_entity(e)
                    i+=1
                    punto = poli[i]
                    break

           

                    #poli = e
                    #print(e)
                    #i+=1
                    #punto = poli[1] 
                   
            else:
                #if e.dxftype() == "ARC":
                    #print(e)
                    #msp.delete_entity(e)
                    #break

                if e.dxftype() == "LINE":
                    #print(e)
                    inicio = e.dxf.start.xyz+(0,0)
                    final = e.dxf.end.xyz +(0,0)
            
                    if distancia(punto, inicio)< 0.01:
                        poli.append_vertex(e.dxf.end.xyz)
                            #points.extend([final])

                        msp.delete_entity(e)
                        if distancia(final, poli[0])<0.01 and i>1:  
                            poli.close=1
                            i=0
                            diccionario_elementos[poli.dxf.handle]=area_poli(poli)
                        
                        else:
                            i+=1
                            punto = poli[i]
                   
                        break
                    elif distancia(punto, final)< 0.01:
                        poli.append_vertex(e.dxf.start.xyz)
                        msp.delete_entity(e)
                        if distancia(inicio, poli[0])<0.01 and i>1:  
                            poli.close=1
                            i=0
                            diccionario_elementos[poli.dxf.handle]=area_poli(poli)
                            #ezdxf.path.make_path(poli)

                        else:
                            i += 1 
                            punto = poli[i]
                    
                        break
                    else:
                        pass

    for elemento in msp.query("POLYLINE" or "CIRCLE"):
        if elemento.dxf.handle == max(diccionario_elementos, key=diccionario_elementos.get):
            elemento_exterior=elemento
        
            #ruta=ezdxf.path.make_path(elemento_exterior)
            #print (ruta)

    no_relleno=False
    while no_relleno:
        hatch = msp.add_hatch(color=5,
                              dxfattribs={
                "hatch_style": 1,
                # 0 = nested: ezdxf.const.HATCH_STYLE_NESTED
                # 1 = outer: ezdxf.const.HATCH_STYLE_OUTERMOST
                # 2 = ignore: ezdxf.const.HATCH_STYLE_IGNORE
            },
                              )

        path = hatch.paths.add_polyline_path(
            elemento_exterior.get_points(format="xyb"),
             is_closed=elemento_exterior.closed,
             flags=1,
     
             )
        for elemento in msp.query("LWPOLYLINE" or "CIRCLE"):
            if elemento.dxf.handle == max(diccionario_elementos, key=diccionario_elementos.get):
                pass
            else:
                if elemento.dxftype()=="LWPOLYLINE":
                    path_interior= hatch.paths.add_polyline_path(
            elemento.get_points(format="xyb"),
             is_closed=elemento_exterior.closed,
             flags=1,)            

    #print(area_recuadro())
    #print(diccionario_elementos)
    indice_nest=max(diccionario_elementos.values()) / (area_recuadro())
    print(indice_nest)

    return indice_nest



    #doc.saveas("new_name.dxf")