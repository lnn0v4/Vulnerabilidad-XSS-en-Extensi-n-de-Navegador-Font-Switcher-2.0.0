# Vulnerabilidad-XSS-en-Extensi-n-de-Navegador-Font-Switcher-2.0.0
Este script demuestra la explotación de una vulnerabilidad XSS persistente dentro de una extensión de navegador en un entorno controlado.

🔍 Descripción General

Nombre de la extensión: Font Switcher
Versión: 2.0.0
Tipo: Extensión de Google Chrome
Permisos solicitados: storage, scripting, <all_urls>

La extensión permite al usuario cambiar la fuente tipográfica de las páginas web que visita. Durante su análisis se identificó una vulnerabilidad de tipo Cross-Site Scripting (XSS) causada por la falta de validación y escape de entradas controladas por el usuario.

🚨 Resumen de la Vulnerabilidad

-Tipo: XSS por inyección en plantillas (Template Injection)
-Vector de ataque: Entrada del usuario almacenada en chrome.storage.sync
-Contexto de ejecución: Content Script
-Persistencia: Sí
-Gravedad: Alta

📂 Componentes Afectados

popup.js

-El valor seleccionado por el usuario se guarda sin validación ni sanitización.

content.js

-El valor almacenado se inserta directamente en el DOM en cada carga de página.















