import socket
import threading

HOST = "127.0.0.1"
PORT = 5000
ENCODING = "utf-8"

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    cliente.connect((HOST, PORT))
except Exception as e:
    print(f"[!] No se pudo conectar al servidor: {e}")
    exit()

nombre_enviado = False


def recibir():
    global nombre_enviado
    while True:
        try:
            mensaje = cliente.recv(1024)
            if not mensaje:
                print("[!] Conexión cerrada por el servidor.")
                cliente.close()
                break

            texto = mensaje.decode(ENCODING).strip()
            print(texto)

            if texto.lower().startswith("Escribe tu nombre") and not nombre_enviado:
                nombre = input("Tu nombre: ").strip()
                cliente.send(nombre.encode(ENCODING))

        except:
            print("[!] Error al recibir datos.")
            cliente.close()
            break


def enviar():
    while True:
        try:
            mensaje = input()
            cliente.send(mensaje.encode(ENCODING))
        except:
            print("[!] Error al enviar mensaje.")
            cliente.close()
            break


# Iniciamos los hilos
threading.Thread(target=recibir, daemon=True).start()
enviar()
