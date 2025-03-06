import os
import cv2
import numpy as np
import tensorflow as tf

def detect_piso_tatil(image_path, model_path="/home/davicortes_oliveira1/piso_tatil_yolov5_PDI/yolov5_tf_select.tflite",
                      output_dir="/home/davicortes_oliveira1/piso_tatil_yolov5_PDI/resultados", confidence_threshold=0.5):
    """
    Detecta piso tátil em uma imagem usando um modelo YOLOv5 convertido para TensorFlow Lite e salva o resultado.

    Args:
        image_path (str): Caminho da imagem a ser processada.
        model_path (str): Caminho do modelo TFLite convertido.
        output_dir (str): Diretório onde a imagem resultante será salva.
        confidence_threshold (float): Limite de confiança para exibir as detecções.

    Returns:
        None. Salva a imagem com as detecções na pasta especificada.
    """

    print(f"📂 Carregando modelo TFLite de: {model_path}")
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # 🟡 Verifica o formato esperado de entrada do modelo
    input_shape = input_details[0]['shape']
    print(f"📏 Dimensão esperada do modelo: {input_shape}")

    if list(input_shape) != [1, 3, 640, 640]:
        raise ValueError(f"🚨 O modelo espera entrada (1, 3, 640, 640), mas recebeu {input_shape}")

    # 🟢 Carregar e pré-processar a imagem
    print(f"📷 Carregando imagem: {image_path}")
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"❌ Imagem não encontrada: {image_path}")

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (640, 640))
    image_transposed = np.transpose(image_resized, (2, 0, 1))  # (Altura, Largura, Canais) -> (Canais, Altura, Largura)
    image_input = np.expand_dims(image_transposed / 255.0, axis=0).astype(np.float32)  # Normalização

    print("🟢 Imagem pré-processada com sucesso!")

    # Definir a entrada do modelo
    interpreter.set_tensor(input_details[0]['index'], image_input)

    # Executar a inferência
    print("⏳ Rodando a inferência...")
    interpreter.invoke()

    # Obter saída do modelo
    output_data = interpreter.get_tensor(output_details[0]['index'])
    print(f"📤 Saída bruta do modelo obtida com shape: {output_data.shape}")

    # Processar detecções
    def process_detections(output_data, img_shape):
        """Processa os resultados da inferência e retorna as caixas detectadas."""
        height, width, _ = img_shape
        detections = []

        print("📊 Processando detecções...")
        for detection in output_data[0]:
            confidence = detection[4]
            if confidence > confidence_threshold:
                x_center, y_center, w, h = detection[:4]
                x1, y1 = int((x_center - w / 2) * width), int((y_center - h / 2) * height)
                x2, y2 = int((x_center + w / 2) * width), int((y_center + h / 2) * height)
                detections.append((x1, y1, x2, y2, confidence))
        
        print(f"📸 {len(detections)} objetos detectados acima de {confidence_threshold * 100:.0f}% confiança")
        return detections

    # Obter detecções
    detections = process_detections(output_data, image.shape)

    # Verifica se alguma detecção foi encontrada
    if not detections:
        print("⚠️ Nenhuma detecção encontrada. A imagem será salva sem alterações.")

    # Desenhar as detecções na imagem
    for (x1, y1, x2, y2, conf) in detections:
        cv2.rectangle(image_rgb, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image_rgb, f"Piso Tátil {conf:.2f}", (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Criar diretório de saída se não existir
    os.makedirs(output_dir, exist_ok=True)

    # Salvar a imagem processada
    output_path = os.path.join(output_dir, os.path.basename(image_path))
    cv2.imwrite(output_path, cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR))
    print(f"✅ Imagem com detecções salva em: {output_path}")


# 🟢 **Exemplo de uso**
if __name__ == "__main__":
    detect_piso_tatil("/home/davicortes_oliveira1/piso_tatil_yolov5_PDI/datasets/images/train/Frame 95.png")
