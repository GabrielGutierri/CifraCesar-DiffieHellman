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
serverName = "10.1.70.6"
serverPort = 1300

# Conecta ao servidor
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Troca de chaves Diffie-Hellman (gera a chave secreta compartilhada)
p, g, private_key, public_key = diffie_hellman_exchange()

# Envia a chave pública para o servidor
clientSocket.send(bytes(str(public_key), "utf-8"))

# Recebe a chave pública do servidor
server_public_key = int(clientSocket.recv(1024).decode())

# Gera a chave secreta compartilhada (usando a chave pública do servidor)
shared_key = generate_shared_key(server_public_key, private_key, p)

# Mostra a chave compartilhada gerada
print("Chave compartilhada gerada: ", shared_key)

# Solicita a entrada do usuário
sentence = input("Input sentence: ")  # Pode ser qualquer string, não precisa ser apenas minúscula

# Realiza a criptografia com a cifra de César usando a chave compartilhada (como deslocamento)
encrypted_sentence = cifra_de_cesar(sentence, shared_key)

# Envia a sentença criptografada
clientSocket.send(bytes(encrypted_sentence, "utf-8"))

#ADICIONAR UMA NOVA TROCA DE CHAVE AQUI!!!
# Recebe a chave pública do servidor
server_public_key = int(clientSocket.recv(1024).decode())

# Troca de chaves Diffie-Hellman (gera a chave secreta compartilhada)
p, g, private_key, public_key = diffie_hellman_exchange()

# Envia a chave pública para o servidor
clientSocket.send(bytes(str(public_key), "utf-8"))

# Gera a chave secreta compartilhada (usando a chave pública do servidor)
shared_key = generate_shared_key(server_public_key, private_key, p)
print("Nova shared key:", shared_key)

# Recebe a resposta do servidor
modifiedSentence = clientSocket.recv(65000)
text = str(modifiedSentence, "utf-8")

# Descriptografa a mensagem recebida usando a chave compartilhada
decrypted_text = descriptografar_cifra_de_cesar(text, shared_key)

# Exibe a resposta do servidor após a descriptografia
print("Received from server (decrypted): ", decrypted_text)

# Fecha o socket
clientSocket.close()
