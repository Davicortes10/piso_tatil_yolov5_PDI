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
        model_path (str): Caminho do modelo TFLite convertido. Default: "yolov5_tf_select.tflite".
        output_dir (str): Diretório onde a imagem resultante será salva. Default: "resultados".
        confidence_threshold (float): Limite de confiança para exibir as detecções. Default: 0.5.

    Returns:
        None. Salva a imagem com as detecções na pasta especificada.
    """
    # Criar diretório de saída se não existir
    os.makedirs(output_dir, exist_ok=True)
    
    # Carregar o modelo TFLite
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    # Obter detalhes das entradas e saídas do modelo
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Garantir que a entrada do modelo é (1, 640, 640, 3)
    input_shape = input_details[0]['shape']
    if len(input_shape) != 4 or input_shape[1] != 640 or input_shape[2] != 640 or input_shape[3] != 3:
        raise ValueError(f"🚨 O modelo espera entrada (1, 640, 640, 3), mas recebeu {input_shape}")

    # Carregar e pré-processar a imagem
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Converter para RGB
    image_resized = cv2.resize(image_rgb, (640, 640))  # Redimensionar para 640x640
    image_input = np.expand_dims(image_resized / 255.0, axis=0).astype(np.float32)  # Normalizar e formatar

    # Definir a entrada do modelo
    interpreter.set_tensor(input_details[0]['index'], image_input)

    # Executar a inferência
    interpreter.invoke()

    # Obter saída do modelo
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # Processar detecções
    def process_detections(output_data, img_shape):
        """Processa os resultados da inferência e retorna as caixas detectadas."""
        height, width, _ = img_shape
        detections = []

        for detection in output_data[0]:
            confidence = detection[4]  # Confiança do objeto detectado
            if confidence > confidence_threshold:
                x_center, y_center, w, h = detection[:4]  # Coordenadas normalizadas
                x1, y1 = int((x_center - w / 2) * width), int((y_center - h / 2) * height)
                x2, y2 = int((x_center + w / 2) * width), int((y_center + h / 2) * height)
                detections.append((x1, y1, x2, y2, confidence))

        return detections

    # Obter detecções
    detections = process_detections(output_data, image.shape)

    # Desenhar as detecções na imagem
    for (x1, y1, x2, y2, conf) in detections:
        cv2.rectangle(image_rgb, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image_rgb, f"Piso Tátil {conf:.2f}", (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Salvar a imagem processada
    output_path = os.path.join(output_dir, os.path.basename(image_path))
    cv2.imwrite(output_path, cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR))
    print(f"✅ Imagem salva em: {output_path}")


# 🟢 Exemplo de uso:
if __name__ == "__main__":
    detect_piso_tatil("/home/davicortes_oliveira1/piso_tatil_yolov5_PDI/datasets/images/train/Frame 95.png")
