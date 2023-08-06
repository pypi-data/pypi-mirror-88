import os 
from imutils import paths
import shutil
import tqdm
import urllib.request

from pathlib import Path

# ML
import torchvision.transforms as transforms
import torch

# Show Images
from PIL import Image
from skimage import color
import io
import numpy as np

#------------Download weights--------------------------------------

weights = str(Path.home())+f"{os.sep}.deep-motilidad{os.sep}models{os.sep}"+ "resnet50Motility.pth"


url = "https://www.dropbox.com/s/4nh5m0qmenvnjv5/resnet50Motility.pth?dl=1"
if  not os.path.exists(weights):
    os.makedirs(os.path.dirname(weights), exist_ok=True)
    urllib.request.urlretrieve(url, filename=weights)


model = torch.jit.load(weights)
model = model.cpu()
model.eval()

device="cpu"
def transform_image(image):
    my_transforms = transforms.Compose([transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image_aux = image
    return my_transforms(image_aux).unsqueeze(0).to(device)


def inference(model, input):
    model = model.to(device)

    with torch.no_grad():
        outputs = model(input)

    outputs = torch.argmax(outputs,1)

    # Moving to CPU
    model = model.cpu()
    
    return outputs


def predict_classification(input_folder, output_folder):
    
    os.makedirs(output_folder+"/complete",exist_ok=True)
    os.makedirs(output_folder+"/incomplete",exist_ok=True)
    
    for img in os.listdir(input_folder):
        input_path = input_folder+img
        image = Image.open(input_folder+img)
        image_np = np.array(image)
        if image_np.shape[0] != 3:
            if input_path.lower().endswith(".tiff") or input_path.lower().endswith(".tif"):
                image_np = exposure.rescale_intensity(image_np)
            image_np = color.gray2rgb(image_np)
            image = Image.fromarray(image_np)

        width, height = image.size

        image = transforms.Resize((512,512))(image)
        tensor = transform_image(image=image)
        prediction=inference(model,tensor)[0]
        if(prediction.numpy()==0):
            shutil.copy(input_folder+img,output_folder+"/complete/"+img)
        else:
            shutil.copy(input_folder+img,output_folder+"/incomplete/"+img)


