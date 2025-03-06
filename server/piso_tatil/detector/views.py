from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
import os
import tensorflow.lite as tflite
import numpy as np
import cv2
from django.core.files.storage import default_storage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# Carregar o modelo YOLOv5 treinado
model_path = os.path.abspath(os.path.join(settings.BASE_DIR, "piso_tatil", "media", "yolov5_tf_select.tflite"))

try:
    interpreter = tflite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    print("✅ Modelo carregado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao carregar modelo: {e}")

LABELS = ["frente", "parar", "direita", "placa_faltante", "esquerda"]

# Página principal com index.html
def home(request):
    return render(request, "detector/index.html")

# API para processar imagem
@csrf_exempt
@api_view(['POST'])
def detect_piso_tatil(request):
    try:
        print("📸 Recebendo imagem...")

        if 'image' not in request.FILES:
            print("❌ Nenhuma imagem enviada!")
            return JsonResponse({"error": "Nenhuma imagem enviada"}, status=400)

        # Salvar imagem temporariamente
        image_file = request.FILES['image']
        image_path = os.path.join(settings.MEDIA_ROOT, "temp_image.jpg")

        with open(image_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        # Verificar se a imagem foi salva corretamente
        if not os.path.exists(image_path):
            print("❌ Erro ao salvar imagem!")
            return JsonResponse({"error": "Erro ao salvar imagem"}, status=500)

        # Carregar imagem com OpenCV
        print(f"📂 Abrindo imagem {image_path}...")
        image = cv2.imread(image_path)
        if image is None:
            print("❌ Erro ao abrir a imagem!")
            return JsonResponse({"error": "Erro ao abrir a imagem"}, status=500)

        print("📏 Redimensionando e convertendo imagem...")
        image = cv2.resize(image, (640, 640))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Converter de BGR para RGB

        # Verificar a forma da imagem
        print("Shape after conversion:", image.shape)  # Deve ser (640, 640, 3)

        # Expande dimensão para (1, 640, 640, 3) e ajusta para (1, 3, 640, 640)
        image = np.expand_dims(image, axis=0).astype(np.float32) / 255.0
        image = np.transpose(image, (0, 3, 1, 2))  # Transforma para (1, 3, 640, 640)

        print("🧠 Rodando inferência no modelo...")
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        # Verificar a forma esperada pelo modelo
        print("Input details:", input_details)

        # Definir o tensor de entrada
        interpreter.set_tensor(input_details[0]['index'], image)
        interpreter.invoke()

        # Obter a saída do modelo
        output_data = interpreter.get_tensor(output_details[0]['index'])
        print("Output data shape:", output_data.shape)


        if output_data is None or output_data.shape[1] == 0:
            print("⚠️ Nenhuma detecção válida encontrada!")
            return JsonResponse({"classe_detectada": "placa_not"}, status=200)


        ''' # Processar a saída do modelo
            if output_data is None or len(output_data) == 0:
                print("❌ Nenhum resultado detectado!")
                return JsonResponse({"error": "Nenhuma saída detectada pelo modelo"}, status=500)'''

        # Supondo que a saída seja (1, n, 5 + num_classes)
        # Onde n é o número de detecções e 5 + num_classes contém [x, y, w, h, conf, class_probs...]
        detections = output_data[0]  # Remove a dimensão do batch

        # Limiar de confiança
        confidence_threshold = 0.5

        # Filtrar detecções com base no limiar de confiança
        valid_detections = []
        for detection in detections:
            confidence = detection[4]  # Confiança da detecção
            if confidence >= confidence_threshold:
                valid_detections.append(detection)
        
        if not valid_detections:
            print("⚠️ Nenhuma detecção válida encontrada!")
            return JsonResponse({"classe_detectada": "placa_not"}, status=200)


        # Selecionar a detecção com a maior confiança
        best_detection = max(valid_detections, key=lambda x: x[4])
        class_probs = best_detection[5:]  # Probabilidades das classes
        class_index = np.argmax(class_probs)  # Índice da classe com maior probabilidade

        if class_index >= len(LABELS):
            print("❌ Índice da classe fora do intervalo!")
            return JsonResponse({"classe_detectada": "placa_not"}, status=200)

        detected_class = LABELS[class_index]

        print(f"✅ Classe detectada: {detected_class}")
        return JsonResponse({"classe_detectada": detected_class})

    except Exception as e:
        print(f"❌ Erro interno: {e}")
        return JsonResponse({"error": f"Erro interno: {str(e)}"}, status=500)