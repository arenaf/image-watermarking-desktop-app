# Image Watermarking Desktop App

![banner-watermark](https://github.com/arenaf/image-watermarking-desktop-app/assets/169451601/83b740f3-767f-48b2-bbaf-4292f8a0ed7b)

## Descripción

Aplicación que permite cargar una imagen y poner una marca de agua sobre ella.

La aplicación se desarrolló con ***Python***. Se utilizó ***Tkinter*** para el entorno gráfico, la librería ***PIL*** para la carga de imágenes y la librería ***matplotlib*** para obtener las fuentes.

## Manejo de la aplicación
### Carga de la imagen
Inicia con un frame vacío que será ocupado por la imagen seleccionada. Para añadir la imagen, se debe pulsar sobre
**Load image** y seleccionar un archivo con extensión válida (jpg, png, bmp, gif).

![load-watermark](https://github.com/arenaf/image-watermarking-desktop-app/assets/169451601/3605f832-153b-4246-9261-5fb8d7ad8dea)


### Mostrar marca de agua

Debajo del botón de carga **Load image**, se encuentra un recuadro de entrada correspondiente a la marca de agua **Watermark** dónde se debe escribir el texto que se quiere mostrar y, a continuación, pulsar **Show**.
Aparecerá en pantalla y sobre la imagen el texto que hemos escrito.

![show-watermark](https://github.com/arenaf/image-watermarking-desktop-app/assets/169451601/34e6b829-4de6-46e8-852b-9f41ae61e416)

### Modificar la marca de agua
Los siguientes botones permiten ajustar la marca de agua:
- **Color**: permite cambiar el color de la fuente.
- **Opacity**: se puede cambiar la opacidad, haciéndola más transparente o más opaca.
- **Font**: permite seleccionar un tipo de fuente diferente, por defecto es *arial*.
- **Size**: cambia el tamaño de la fuente.

![color-watermark](https://github.com/arenaf/image-watermarking-desktop-app/assets/169451601/2e9baefb-7cf4-4849-98b5-cc8a1006972f)

### Ajustar posición
Las flechas izquierda, derecha, arriba y abajo permiten mover la marca de agua por la imagen.

Las flechas de rotación, rotan la marca de agua y pone el texto en diagonal.

![rotated-watermark](https://github.com/arenaf/image-watermarking-desktop-app/assets/169451601/fd468eb2-c18a-4064-9926-8e8392b4f571)

### Guardar la  imagen
El botón **Save** guarda una nueva imagen con la marca de agua generada. No sobreescribe la imagen original.

![save-watermark](https://github.com/arenaf/image-watermarking-desktop-app/assets/169451601/7c768d49-212b-48f9-8d71-3240a03306d2)


## Requerimientos
Librerías requeridas:
- pillow
- matplotlib
- customtkinter

