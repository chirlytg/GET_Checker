# Extensión "GET Checker"
[![Version](https://img.shields.io/badge/Version-v1.0-green.svg)]()
[![Language](https://img.shields.io/badge/Language-Python-orange.svg)](https://www.python.org/)

Una extensión para Burp que para cada request que tenga parámetros por POST envia un segundo request GET con los
mismos parámetros en el body de la petición e informando en los logs de la extensipon en caso que el
resultado del POST sea código HTTP 20X.

Esta extensión solo se aplica para peticiones cuyo Content-Type sea _**application/x-www-form-urlencoded**_

# Instalación

## Manual

1. Descargue [2.GET_Checker.py](2.GET_Checker.py) en la máquina a ejecutar
2. Vaya a la pestaña _**Extender > Extensions**_, luego haga click en el botón _**Add**_ button. En la ventana emergente navege hasta la ubicación de **2.GET_Checker.py** y haga click en el botón _**Next**_.

## Como usar

Navegue al sitio que desea analizar y en la salida de logs de la extensión en caso de detectar una salida con código HTTP 20X se muestra la petición y la respuesta.

![Scanner PII](/images/get_checker.png)