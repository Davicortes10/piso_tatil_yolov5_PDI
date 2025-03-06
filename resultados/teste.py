import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# Lista de classes do modelo YOLOv5 (ajuste conforme necessário)
CLASS_NAMES = ["frente", "parar", "direita", "placa_faltante", "esquerda"
]  # Modifique conforme o seu modelo

def detect_piso_tatil(image_path, model_path="yolov5_tf_select.tflite", confidence_threshold=0.5):
    """
    Detecta piso tátil em uma imagem usando um modelo YOLOv5 convertido para TensorFlow Lite.

    Args:
        image_path (str): Caminho da imagem a ser processada.
        model_path (str): Caminho do modelo TFLite convertido.
        confidence_threshold (float): Limite de confiança para exibir as detecções.

    Returns:
        None. Exibe a imagem com as detecções e imprime as classes detectadas.
    """
    # 🚀 Carregar o modelo TFLite
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    # 📏 Obter detalhes da entrada e saída do modelo
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # 📐 Formato esperado pelo modelo (1, 3, 640, 640)
    input_shape = input_details[0]['shape']
    _, model_channels, model_height, model_width = input_shape

    print(f"📏 Modelo espera: {input_shape}")

    # 📸 Carregar a imagem original
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"❌ Erro: Imagem não encontrada: {image_path}")

    original_height, original_width, _ = image.shape  # Tamanho original da imagem

    # 📏 Redimensionar a imagem para o tamanho esperado pelo modelo
    image_resized = cv2.resize(image, (model_width, model_height))
    image_rgb = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)  # Converter para RGB

    # 🔄 **Converter a imagem para o formato do modelo** (1, 3, 640, 640)
    image_input = np.transpose(image_rgb, (2, 0, 1))  # De (640, 640, 3) -> (3, 640, 640)
    image_input = np.expand_dims(image_input, axis=0).astype(np.float32) / 255.0  # Normalizar e expandir dimensão

    # 🔍 Validar entrada antes de passar para o modelo
    print(f"📏 Formato da entrada da imagem: {image_input.shape}")

    # 🚀 Definir entrada do modelo corretamente
    interpreter.set_tensor(input_details[0]['index'], image_input)

    # ⚡ Executar a inferência
    interpreter.invoke()

    # 📌 Obter saída do modelo (YOLOv5 pode ter múltiplas saídas)
    output_data = interpreter.get_tensor(output_details[0]['index'])

    print(f"📊 Saída bruta do modelo: {output_data.shape}")

    # 🛠️ Processar detecções
    def process_detections(output_data, model_width, model_height, original_width, original_height):
        """ Processa os resultados da inferência e retorna as caixas detectadas e as classes. """
        detections = []
        detected_classes = set()  # Armazena as classes detectadas

        for detection in output_data[0]:
            confidence = detection[4]  # Confiança do objeto detectado
            if confidence > confidence_threshold:
                x_center, y_center, w, h = detection[:4]  # Coordenadas normalizadas (0 a 1)

                # Identificar a classe detectada
                class_id = int(np.argmax(detection[5:]))  # Pega a classe com maior score
                class_name = CLASS_NAMES[class_id] if class_id < len(CLASS_NAMES) else f"ID-{class_id}"
                detected_classes.add(class_name)

                # Converter para coordenadas no modelo (640x640)
                x_center *= model_width
                y_center *= model_height
                w *= model_width
                h *= model_height

                # Converter para coordenadas na imagem original
                x1 = int((x_center - w / 2) * (original_width / model_width))
                y1 = int((y_center - h / 2) * (original_height / model_height))
                x2 = int((x_center + w / 2) * (original_width / model_width))
                y2 = int((y_center + h / 2) * (original_height / model_height))

                detections.append((x1, y1, x2, y2, confidence, class_name))

        return detections, detected_classes

    # 📌 Obter detecções corrigidas e classes detectadas
    detections, detected_classes = process_detections(output_data, model_width, model_height, original_width, original_height)

    print(f"✅ Número de detecções: {len(detections)}")
    if len(detections) > 0:
        print(f"📋 Primeira detecção: {detections[0]}")  # Depuração

    # 🏷️ Exibir classes detectadas
    print(f"🎯 Classes detectadas: {', '.join(detected_classes) if detected_classes else 'Nenhuma'}")

    # 📸 Exibir a imagem com as detecções
    for (x1, y1, x2, y2, conf, class_name) in detections:
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, f"{class_name} {conf:.2f}", (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 🖼️ Mostrar a imagem resultante
    plt.figure(figsize=(8, 6))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.title("Detecção de Piso Tátil")
    plt.show()

# 🛠️ Testar a função com a imagem corrigida
detect_piso_tatil("datasets/images/train/Frame 562.png")
