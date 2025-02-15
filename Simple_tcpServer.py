from socket import *
import random

# Função para criptografar utilizando a cifra de César para toda a tabela ASCII
def cifra_de_cesar(texto, deslocamento):
    resultado = ""
    for char in texto:
        # Aplica o deslocamento a cada caractere ASCII
        novo_char = chr((ord(char) + deslocamento) % 256)  # Modulo 256 para manter dentro da faixa ASCII
        resultado += novo_char
    return resultado

# Função para descriptografar utilizando a cifra de César para toda a tabela ASCII
def descriptografar_cifra_de_cesar(texto, deslocamento):
    return cifra_de_cesar(texto, -deslocamento)  # Inverte o deslocamento para a descriptografia

# Algoritmo Diffie-Hellman para troca de chaves simétricas
def diffie_hellman_exchange():
    # Parâmetros públicos
    p = 9973  # Número primo
    g = 5   # Base

    # Chave privada (aleatória)
    private_key = random.randint(1, p-1)

    # Chave pública (g^private_key mod p)
    public_key = pow(g, private_key, p)

    return p, g, private_key, public_key

def generate_shared_key(public_key_other, private_key, p):
    # Calcula a chave compartilhada (public_key_other^private_key mod p)
    shared_key = pow(public_key_other, private_key, p)
    return shared_key

# Defina o servidor e a porta
serverPort = 1300
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(5)  # Espera até 5 conexões simultâneas

print("TCP Server aguardando conexão...\n")

# Aceita a conexão do cliente
connectionSocket, addr = serverSocket.accept()

# Troca de chaves Diffie-Hellman (gera a chave secreta compartilhada)
p, g, private_key, public_key = diffie_hellman_exchange()

# Envia a chave pública para o cliente
connectionSocket.send(bytes(str(public_key), "utf-8"))

# Recebe a chave pública do cliente
client_public_key = int(connectionSocket.recv(1024).decode())

# Gera a chave secreta compartilhada (usando a chave pública do cliente)
shared_key = generate_shared_key(client_public_key, private_key, p)
print("Chave compartilhada gerada: ", shared_key)

# Recebe a mensagem criptografada do cliente
sentence = connectionSocket.recv(65000)
received_message = str(sentence, "utf-8")
print("Mensagem recebida do cliente (criptografada): ", received_message)

# Descriptografa a mensagem recebida usando a chave compartilhada
decrypted_message = descriptografar_cifra_de_cesar(received_message, shared_key)
print("Mensagem DECRIPTOGRAFADA do cliente: ", decrypted_message)

# Realiza o processamento da mensagem, neste caso, convertendo para maiúsculas
capitalized_sentence = decrypted_message.upper()

# Troca de chaves Diffie-Hellman (gera a chave secreta compartilhada)
p, g, private_key, public_key = diffie_hellman_exchange()

# Envia a chave pública para o cliente
connectionSocket.send(bytes(str(public_key), "utf-8"))

# Recebe a chave pública do cliente
client_public_key = int(connectionSocket.recv(1024).decode())

# Gera a chave secreta compartilhada (usando a chave pública do cliente)
shared_key = generate_shared_key(client_public_key, private_key, p)
print("Chave compartilhada gerada: ", shared_key)

# Criptografa a resposta com a cifra de César usando a chave compartilhada
response_encrypted = cifra_de_cesar(capitalized_sentence, shared_key)

# Envia a resposta criptografada de volta ao cliente
connectionSocket.send(bytes(response_encrypted, "utf-8"))
print("Resposta enviada de volta ao cliente (criptografada): ", response_encrypted)

# Fecha a conexão
connectionSocket.close()
