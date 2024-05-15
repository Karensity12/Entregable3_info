import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import pydicom

def contar(ruta):
    img = cv2.imread(ruta)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_noise = cv2.GaussianBlur(img_gray, (5, 5), 0) #Reducir el ruido, (5,5)---> tamaño del kernel

    
    #Prueba 
    cv2.namedWindow('Ventana', 0)   #Crear ventana
    cv2.imshow('Ventana',img_noise)       #Mostrar la imagen en la ventana creada
    cv2.waitKey(0)                  #Dejar la ventana abierta hasta el siguiente enter
    cv2.destroyAllWindows()   

    #Binarización
    _, image_bin = cv2.threshold(img_noise, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    #Operaciones morfologicas
    kernel = np.ones((3, 3), np.uint8)
    imgOp = cv2.morphologyEx(image_bin, cv2.MORPH_OPEN, kernel, iterations=1) #Apertura: erosion + dolatacion 

    #Closing
    imgC = cv2.morphologyEx(imgOp, cv2.MORPH_CLOSE, kernel, iterations=1)

    #Encontrar contornos (externos)
    contours, _ = cv2.findContours(imgC, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    """cv2.imshow('aqui',imgC)
    cv2.waitKey(0)                  
    cv2.destroyAllWindows()"""


    min_area = 20  
    max_area = 31  
    filtered_contours = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if min_area < area < max_area:
            filtered_contours.append(cnt)

    cell_count = len(filtered_contours)
    print(f"Number of cells: {cell_count}")
    return cell_count

def cargar_dc(ruta):
    dicoms= []
    archivos = os.listdir(ruta)
    archivos_dicom = sorted([archivo for archivo in archivos if archivo.endswith('.dcm')])
    for archivo in archivos_dicom:
        ruta_dicoms = os.path.join(ruta, archivo)
        ds = pydicom.dcmread(ruta_dicoms) 
        dicoms.append(ds)
    print("Archivos cargados")
    return dicoms


def mostrar_ds(dicoms):
    fig = plt.figure()
    repeticiones = int(input("Ingrese la cantidad de veces que desea ver las imagenes: ")) 
    for i in range(repeticiones):
        for x in dicoms:
            plt.imshow(x.pixel_array, cmap = plt.cm.gray)
            plt.title("imagen dicom")
            plt.axis('off')
            plt.pause(0.05)
            plt.clf()
        for x in dicoms[::-1]:
            plt.imshow(x.pixel_array, cmap = plt.cm.gray)
            plt.title("Imagen dicom")
            plt.axis('off')
            plt.pause(0.05)
            plt.clf()
    plt.close()
    
        

def main():
    x = ''
    while True:
        print("""Opciones
            \r1-Contar celulas 
            \r2-Cargar archivos dicom✅
            \r3-Mostrar archivos dicom✅
            \r4-Salir✅""")
        opcion = int(input("Ingrese la opcion deseada: "))
        if opcion == 1:
            ruta = input("Ingrese la ruta de la imagen con las celulas a contar: ") 
            contar(ruta)
            continue
        elif opcion == 2:
            ruta = input("Ingrese la ruta de la carpeta con los archivos dicom: ")
            x = cargar_dc(ruta)
            continue
        elif opcion == 3:
            if x == '':
                print("Aun no ha ingresado archivos, porfavor dirijase a la opcion 2")
                continue
            else:
                mostrar_ds(x)
                continue
        elif opcion == 4:
            print("Ha terminado")
            break

main()


