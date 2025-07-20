import socket
import select

HOST = "0.0.0.0"
PORT = 5000
ENCODING = "utf-8"


def inicializar_servidor():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[+] Servidor escuchando en {HOST}:{PORT}")
    return server_socket


def recibir_mensaje(cliente_socket):
    try:
        mensaje = cliente_socket.recv(1024)
        if not mensaje:
            return None
        return mensaje.decode(ENCODING).strip()
    except:
        return None


def cerrar_conexion(cliente_socket, sockets_list, clientes):
    print(
        f"[-] Cliente {clientes[cliente_socket]['direccion']} ({clientes[cliente_socket]['nombre']}) desconectado."
    )
    sockets_list.remove(cliente_socket)
    del clientes[cliente_socket]
    cliente_socket.close()


def main():
    server_socket = inicializar_servidor()
    sockets_list = [server_socket]
    clientes = {}

    while True:
        try:
            read_sockets, _, exception_sockets = select.select(
                sockets_list, [], sockets_list
            )

            for notified_socket in read_sockets:
                if notified_socket == server_socket:
                    client_socket, client_address = server_socket.accept()
                    sockets_list.append(client_socket)

                    client_socket.send("Escribe tu nombre: ".encode(ENCODING))
                    nombre = recibir_mensaje(client_socket)
                    if not nombre:
                        sockets_list.remove(client_socket)
                        client_socket.close()
                        continue

                    clientes[client_socket] = {
                        "direccion": client_address,
                        "nombre": nombre,
                    }
                    print(f"[+] Nueva conexión de {client_address} como {nombre}")
                    client_socket.send(
                        f"Bienvenido al chat, {nombre}\n".encode(ENCODING)
                    )

                else:
                    mensaje = recibir_mensaje(notified_socket)
                    if mensaje is None:
                        cerrar_conexion(notified_socket, sockets_list, clientes)
                        continue

                    nombre = clientes[notified_socket]["nombre"]

                    for client in clientes:
                        if client != notified_socket:
                            try:
                                client.send(f"{nombre}: {mensaje}\n".encode(ENCODING))
                            except:
                                pass
            for notified_socket in exception_sockets:
                cerrar_conexion(notified_socket, sockets_list, clientes)

        except KeyboardInterrupt:
            print("\n[!] Servidor apagado por el usuario.")
            break

    server_socket.close()


if __name__ == "__main__":
    main()
