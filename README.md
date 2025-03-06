```md
# 🦯 Detecção de Piso Tátil - Processamento de Imagens

Este projeto realiza a **detecção de pisos táteis** utilizando o **modelo YOLOv5 treinado**, integrado com **Django** e publicado na **internet** via **ngrok**, permitindo acesso remoto e análise em tempo real.

## 🎯 Objetivo

O projeto visa desenvolver um **sistema de detecção de pisos táteis** para auxiliar **pessoas com deficiência visual**, fornecendo **feedback auditivo** sobre a presença e o tipo de piso tátil detectado.

---

## 🛠 Tecnologias Utilizadas

🔹 **Python 3.8**  
🔹 **Django** - Framework para o servidor  
🔹 **OpenCV** - Processamento de imagens  
🔹 **NumPy** - Manipulação de matrizes e vetores  
🔹 **TensorFlow Lite (TFLite)** - Execução do modelo YOLOv5 otimizado  
🔹 **JavaScript (Frontend)** - Captura de imagens em tempo real  
🔹 **HTML + CSS** - Interface Web responsiva  
🔹 **ngrok** - Publicação do servidor Django na internet  

---

## 📦 Pré-requisitos

Certifique-se de ter instalado:

✔️ **Python 3.8**  
✔️ **pip** (gerenciador de pacotes do Python)  
✔️ **Virtualenv** (opcional, mas recomendado)  

Para instalar os pacotes necessários:

```bash
pip install -r requirements.txt
```

---

## 🚀 Instalação e Execução

### 🔻 Clone este repositório:

```bash
git clone https://github.com/Davicortes10/piso_tatil_yolov5_PDI.git
cd piso_tatil_yolov5_PDI
```

### ⚙️ Crie e ative um ambiente virtual (opcional):

```bash
# Criando o ambiente virtual
python -m venv venv

# Ativando no Windows
venv\Scripts\activate

# Ativando no macOS/Linux
source venv/bin/activate
```

### 📌 Instale as dependências:

```bash
pip install -r requirements.txt
```

### 🏃‍♂️ Execute o Servidor Django:

```bash
python manage.py runserver
```

### 🌍 Exponha o servidor na internet via **ngrok**:

```bash
ngrok http 8000
```

Isso fornecerá um **link público** para acessar remotamente a interface do projeto.

---

## 📥 Download do Modelo YOLOv5

O modelo treinado pode ser baixado aqui:  

📥 **[Baixar Modelo YOLOv5 TF Lite](https://drive.google.com/drive/folders/1xfCjnz_-DI-Dmx6VINQ0C1wICcehhtJg?usp=sharing)**  

Após baixar, coloque o arquivo **`yolov5_tf_select.tflite`** na pasta:

```
piso_tatil_yolov5_PDI/piso_tatil/media/
```

---

## ⚡ Como Funciona?

1️⃣ O usuário acessa a **interface web** e ativa a **câmera**  
2️⃣ O sistema captura **imagens em tempo real**  
3️⃣ As imagens são enviadas para a **API Django**  
4️⃣ O modelo **YOLOv5** analisa e **detecta** o piso tátil  
5️⃣ O resultado é exibido e **uma voz orienta o usuário**  

---

## 🔊 Retornos da API e Feedback Auditivo

| 🔎 **Detecção**       | 🔊 **Mensagem de Voz**                       |
|----------------------|-------------------------------------------|
| **frente**          | "Siga em frente"                          |
| **direita**         | "Piso Tátil Direito detectado"            |
| **esquerda**        | "Piso Tátil Esquerdo detectado"           |
| **parar**           | "Atenção, piso Parar detectado"           |
| **placa_faltante**  | "Placa Faltante detectada à frente"       |
| **placa_not**       | "Atenção, nenhuma placa detectada!"       |

---

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. **Fork** este repositório  
2. **Crie uma branch** para sua funcionalidade:  
   ```bash
   git checkout -b minha-feature
   ```
3. **Commit suas alterações**:  
   ```bash
   git commit -m 'Adicionando nova funcionalidade'
   ```
4. **Envie para análise**:  
   ```bash
   git push origin minha-feature
   ```
5. **Abra um Pull Request** 🚀  

---

## 📚 Informações Acadêmicas

📌 **Disciplina:** **Processamento de Imagens**  
📌 **Professor:** 👨‍🏫 **Professor Doutor Haroldo Gomes Barroso Filho**  
📌 **Curso:** **Engenharia da Computação - UFMA**  
📌 **Aluno:** 👨‍💻 **Davi Oliveira Cortes - MAT: 2020034190**  

---

## 📞 Contato

📧 **Email:** davi.cortes@discente.ufma.br  
🔗 **GitHub:** [Meu GitHub](https://github.com/Davicortes10)  

---

## 📜 Licença

📝 Este projeto está licenciado sob a **Licença MIT**.  
🔗 Para mais informações, acesse: [Licença MIT](https://opensource.org/licenses/MIT)  

---

🚀 **Projeto desenvolvido para a disciplina de Processamento de Imagens - Engenharia da Computação - UFMA**  
```

---

