# CifraCesar-DiffieHellman
Algoritmo em Python que envia e recebe informações em um servidor e cliente TCP, trabalhando com a troca de mensagens de Diffie-Hellman e a criptografia de César

# Cifra de César com Diffie-Hellman

Este projeto implementa uma comunicação segura entre um **cliente** e um **servidor** utilizando a **troca de chaves Diffie-Hellman** e a **Cifra de César** para criptografar as mensagens.

## 📌 Descrição

O projeto contém dois arquivos em **Python** que representam:

- **Servidor** (`server.py`)
- **Cliente** (`client.py`)

A comunicação entre eles segue o seguinte fluxo:

1. Cliente e servidor geram os valores R1 e R2 utilizando o **algoritmo de troca de chaves Diffie-Hellman**.
2. A chave secreta compartilhada gerada no processo é utilizada como **deslocamento** para a Cifra de César.
3. As mensagens enviadas entre cliente e servidor são criptografadas e descriptografadas utilizando a chave derivada.

## 🛠️ Tecnologias Utilizadas

- **Python**
- **Sockets para comunicação entre cliente e servidor**
- **Cifra de César para criptografia**
- **Algoritmo Diffie-Hellman para geração da chave secreta compartilhada**