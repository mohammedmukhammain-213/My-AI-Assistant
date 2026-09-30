import http.server
import ssl
import os

PORT = 5500

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CERT_FILE = os.path.join(
    BASE_DIR,
    "192.168.29.86+2.pem"
)

KEY_FILE = os.path.join(
    BASE_DIR,
    "192.168.29.86+2-key.pem"
)

WEBSITE_DIR = os.path.join(
    BASE_DIR,
    "website"
)

os.chdir(WEBSITE_DIR)


class ReusableHTTPServer(
    http.server.ThreadingHTTPServer
):
    allow_reuse_address = True


server = ReusableHTTPServer(
    ("0.0.0.0", PORT),
    http.server.SimpleHTTPRequestHandler
)


context = ssl.SSLContext(
    ssl.PROTOCOL_TLS_SERVER
)

context.load_cert_chain(
    CERT_FILE,
    KEY_FILE
)


server.socket = context.wrap_socket(
    server.socket,
    server_side=True
)


print()
print("====================================")
print("AI Assistant HTTPS Website")
print("====================================")
print()
print("Laptop:")
print("https://localhost:5500")
print()
print("Laptop IP:")
print("https://192.168.29.86:5500")
print()
print("Server is running...")
print()


server.serve_forever()