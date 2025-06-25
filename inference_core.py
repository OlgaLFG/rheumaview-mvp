import torch
from torchvision import transforms
from PIL import Image

# Предобученная модель
model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)
model.eval()

# Названия классов (пример: для анатомических регионов — замените при необходимости)
class_names = [
    "Cervical Spine", "Thoracic Spine", "Lumbar Spine", "Pelvis/SI Joints",
    "Hips", "Knees", "Ankles", "Feet",
    "Shoulders", "Elbows", "Wrists", "Hands"
]

# Преобразования изображения
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# Основная функция предсказания
def predict_region(image: Image.Image):
    img = transform(image).unsqueeze(0)  # Добавляем batch dimension
    with torch.no_grad():
        outputs = model(img)
    predicted_class = outputs.argmax().item()
    predicted_label = class_names[predicted_class % len(class_names)]  # mock-категоризация
    return predicted_label
