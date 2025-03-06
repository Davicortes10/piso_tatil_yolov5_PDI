

```md
# Detecção de Piso Tátil - Processamento de Imagens

Este projeto realiza a **detecção de imagens de piso tátil** utilizando o **modelo YOLOv5 treinado**. O modelo é **hospedado em um servidor Django** e disponibilizado na **internet** via **ngrok**, permitindo acesso remoto.

## 📌 Objetivo

O objetivo deste trabalho é desenvolver um **sistema de detecção de pisos táteis** para auxiliar **pessoas com deficiência visual**, fornecendo feedback auditivo sobre a presença e o tipo de piso tátil encontrado.

## 📌 Tecnologias Utilizadas

O projeto foi desenvolvido utilizando as seguintes tecnologias e bibliotecas:

- **Python 3.8**
- **Django** → Framework para criação do servidor
- **OpenCV** → Processamento de imagens
- **NumPy** → Manipulação de matrizes e vetores
- **TensorFlow Lite (TFLite)** → Execução do modelo YOLOv5 otimizado
- **JavaScript (Frontend)** → Captura de imagens em tempo real
- **HTML + CSS** → Interface Web responsiva
- **ngrok** → Publicação do servidor Django na internet

## 📌 Pré-requisitos

Antes de rodar o projeto, certifique-se de ter instalado:

- **Python 3.8**
- **pip** (gerenciador de pacotes do Python)
- **Virtualenv** (opcional, mas recomendado)

Para instalar os pacotes necessários:

```bash
pip install -r requirements.txt
```

## 📌 Instalação

1️⃣ Clone este repositório:

```bash
git clone https://github.com/Davicortes10/piso_tatil_yolov5_PDI.git
cd piso_tatil_yolov5_PDI
```

2️⃣ Crie e ative um ambiente virtual (recomendado):

```bash
# Criando o ambiente virtual
python -m venv venv

# Ativando no Windows
venv\Scripts\activate

# Ativando no macOS/Linux
source venv/bin/activate
```

3️⃣ Instale as dependências:

```bash
pip install -r requirements.txt
```

## 📌 Execução do Código

Após configurar o ambiente, inicie o servidor Django:

```bash
python manage.py runserver
```

Em seguida, exponha o servidor na internet via **ngrok**:

```bash
ngrok http 8000
```

Isso fornecerá um link público que pode ser acessado de qualquer lugar.

## 📌 Download do Modelo YOLOv5

O modelo **YOLOv5 treinado** pode ser baixado neste link:

📥 **[Baixar Modelo YOLOv5 TF Lite](https://drive.google.com/drive/folders/1xfCjnz_-DI-Dmx6VINQ0C1wICcehhtJg?usp=sharing)**

Após baixar, coloque o arquivo **`yolov5_tf_select.tflite`** na pasta:

```
PisoTatil/piso_tatil/media/
```

## 📌 Como Funciona?

1. O usuário acessa a interface web e ativa a câmera.
2. A câmera captura imagens em **tempo real**.
3. As imagens são enviadas para a API Django.
4. O modelo **YOLOv5** processa a imagem e **detecta o tipo de piso tátil**.
5. O resultado é exibido na tela e um **áudio** informa a detecção.

## 📌 Principais Funcionalidades

✅ **Detecção automática de pisos táteis em tempo real**  
✅ **Feedback por voz sobre a direção do piso tátil**  
✅ **Interface web responsiva para fácil uso**  
✅ **Execução do modelo YOLOv5 via TensorFlow Lite**  

## 📌 Exemplos de Retornos da API

| Detecção          | Mensagem de Voz                 |
|------------------|--------------------------------|
| **frente**       | "Siga em frente"               |
| **direita**      | "Piso Tátil Direito detectado" |
| **esquerda**     | "Piso Tátil Esquerdo detectado"|
| **parar**        | "Atenção, piso Parar detectado"|
| **placa_faltante** | "Placa Faltante detectada"    |
| **placa_not**    | "Atenção, nenhuma placa detectada!" |

## 📌 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. **Fork** este repositório.
2. **Crie uma branch** para sua funcionalidade (`git checkout -b minha-feature`).
3. **Commit suas alterações** (`git commit -m 'Adicionando nova funcionalidade'`).
4. **Envie para análise** (`git push origin minha-feature`).
5. **Abra um Pull Request**.

## 📌 Reconhecimentos e Direitos Autorais

### **Disciplina**  
📚 **Processamento de Imagens**  

### **Professor**  
👨‍🏫 **Professor Doutor Haroldo Gomes Barroso Filho**  

### **Autor**  
👨‍💻 Davi Oliveira Cortes MAT: 2020034190  

### **Contato**  
📧 Email: davi.cortes@discente.ufma.br  
🔗 GitHub: [Meu GitHub](https://github.com/Davicortes10)  

## 📌 Licença

Este projeto está licenciado sob a **Licença MIT**.  
Para mais informações, acesse: [Licença MIT](https://opensource.org/licenses/MIT)  

---

🚀 **Projeto desenvolvido para a disciplina de Processamento de Imagens - Engenharia da Computação - UFMA**  