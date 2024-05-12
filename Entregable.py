import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import pydicom

def C_celulas(ruta):
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

    min_area = 20  
    max_area = 31  
    filtered_contours = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if min_area < area < max_area:
            filtered_contours.append(cnt)

    cell_count = len(filtered_contours)
    print(f"Number of cells: {cell_count}")

#Pruebita :)
ruta = r'C:\Users\Karen\Desktop\Imagenes info\Imagen celula.jpg'  
C_celulas(ruta)



def cargar_dicom(ruta):
    list= []
    archivos = os.listdir(ruta)
    archivos_dicom = sorted([archivo for archivo in archivos if archivo.endswith('.dcm')])
    for archivo in archivos_dicom:
        ruta_c = os.path.join(ruta, archivo)
        ds = pydicom.dcmread(ruta_c) #Objeto tipo DICOM
        list.append(ds)
    return list


ruta = r'C:\Users\Karen\Desktop\Imagenes info\archivosDCM'
imagenes_dicom = cargar_dicom(ruta)


