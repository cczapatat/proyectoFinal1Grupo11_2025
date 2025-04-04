# MISW4402-SmartStock-Mobile

# SmartStock_Movil_UX
Repositorio para la entrega final del Proyecto MISW-4402-2025 Version Movil

## Integrantes:

| Nombre             |   Correo                      |
|--------------------|-------------------------------|
| Jhon Edinson Muñoz | je.munozr1@uniandes.edu.co    |
| Juan Carlos Torres | jc.torresm1@uniandes.edu.co    |
| Cristian Parada    | c.paradac@uniandes.edu.co    |
| Cristian Zapata    | c.zapatat@uniandes.edu.co    |

## Tabla de contenido
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Diferencias con MockUps](#diferencias-con-mockups)
- [Pasos para hacer Build](#pasos-para-hacer-build)
- [Pasos para Generar APK](#pasos-para-generar-apk)
- [Pasos para Ejecutar en Dispositvo Fisico de Pruebas](#pasos-para-ejecutar-en-dispositivo-fisico-de-pruebas)
- [Pasos para Ejecutar en Dispositivo Emulado de Pruebas](#pasos-para-ejecutar-en-dispositivo-emulado-de-pruebas)



### Estructura del Proyecto



### Pasos para hacer Build
1. En Android Studio con el proyecto abierto, hacer click en el boton del martillo, que aparecera en la parte superior derecha:

2. Esperar una salida de la consola similar a la siguiente imagen:


### Pasos para Generar APK
1. En Android Studio con el proyecto abierto, hacer click en Build -> Build Bundle(s)/APK(s) -> Build APK(s)

2. Esperar hasta que Android Studio avise que termine la generacion y hacer click en "Locate":

3. Te dirigirá a la ubicacion donde se genero al APK:
"Ruta Local proyecto"\app\build\outputs\apk\debug

### Pasos para Ejecutar en Dispositivo Fisico de Pruebas
1. Conecte un dispositivo Android mediante cable USB

2. En Android Studio con el proyecto abierto y el dispositvo a usar conectado (con la opcion de desarrollador activada):

3. Hacer click en la flecha verde(icono play verde) del menu superior derecho:

4. Esperar a que en la terminal aparezca el siguiente mensaje:
install successfully finished en la barra inferior de Run.

### Pasos para Ejecutar en Dispositivo Emulado de Pruebas
#### Crear Dispositivo Virual
1. Ir al menu Tool seleccione la opción Device Manager del menu lateral derecho

2. Seleccione la Opción Virtual y luego dar click en el botón "Create Device"

3. Seleccione el Tipo de dispositivo, Modelo y tamaño de pantalla, luego dar click en Next.

4. Seleccione la imagen del sistema Operativo a usar en el dispositivo virtual y dar click en Next.

5. Seleccione la orientación del dispositivo y dar click en Finish.

6. En la pantalla se muestran los dispositivos virtuales creados.

7. En la Barra de herramientas seleccione el proyecto, seleccione el dispositivo a usar y dar click en el boton compilar.

8. Iniciara el despliegue de la aplicación en el dispositivo seleccionado y estara listo para la prueba.
