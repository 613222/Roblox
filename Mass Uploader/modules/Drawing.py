from PIL import ImageDraw
from PIL import Image as PILImage
import requests
import random
import numpy as np
import cv2
from io import BytesIO
import io

# Remove my functions and replace it with your working
# Manipulation tactic.

colours = [
    cv2.COLOR_BGR2GRAY, cv2.COLOR_RGB2BGR, cv2.COLOR_RGB2BGRA,
    cv2.COLOR_RGB2HSV, cv2.COLOR_RGB2LUV, cv2.COLOR_RGB2HLS,
    cv2.COLOR_RGB2XYZ, cv2.COLOR_RGBA2GRAY, cv2.COLOR_RGB2YUV
]

def manipulateDotting(imageContent, format):
    image = cv2.imdecode(np.frombuffer(imageContent, np.uint8), cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(image, random.choice(colours))
    orb = cv2.ORB_create()
    keypoints = orb.detect(gray, None)
    dot_layer = np.zeros_like(image, dtype=np.uint8)
    for kp in keypoints:
        if random.randint(1, 2) == 1:
            x, y = kp.pt
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Alpha set to 25
            cv2.circle(dot_layer, (int(x), int(y)), 3, color, -1)

    result = cv2.addWeighted(image, 1, dot_layer, random.uniform(0.025, 0.075), 0)
    _, buffer = cv2.imencode(format, result)
    return buffer.tobytes()

class Image:
    def __init__(self):
        self.PackageCreator = "BitsProxy"
        self.PackageLastUpdated = "May 26th, 2024."
        self.AvailableAlgorithms = self.DetectAvailableAlgorithms()

    def RandomizeDot(self, imageContent, format='PNG'):
        img = PILImage.open(BytesIO(imageContent)).convert('RGBA')
        width, height = img.size
        dot_size = random.uniform(0.1, 0.45)
        dot_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(1,10))
        random_x = random.randint(0, width - 1)
        random_y = random.randint(0, height - 1)
        dot = PILImage.new('RGBA', img.size, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 0))
        dot_draw = ImageDraw.Draw(dot)
        dot_draw.ellipse((random_x - dot_size, random_y - dot_size, random_x + dot_size, random_y + dot_size), fill=dot_color)
        modified_image = PILImage.alpha_composite(img, dot)
        modified_image_content = BytesIO()
        modified_image.save(modified_image_content, format="PNG")
        if format == "JPEG":
            img2 = PILImage.open(BytesIO(modified_image_content.getvalue())).convert('RGB')
            zk = BytesIO()
            img2.save(zk, format="JPEG")
            return zk.getvalue()
        return modified_image_content.getvalue()

    def RandomizeScale(self, imageContent, format='PNG'):
        img = PILImage.open(BytesIO(imageContent))
        old_width, old_height = img.size
        new_width = int(old_width * random.uniform(0.75, 1.25))
        new_height = int(old_height * random.uniform(0.75, 1.25))
        img = img.resize((new_width, new_height))
        output = BytesIO()
        img.save(output, format=format)
        return output.getvalue()
    
    def RandomizeOpacity(self, imageContent, format='PNG'):
        img = PILImage.open(BytesIO(imageContent))
        width, height = img.size
        new_img = PILImage.new("RGBA", (width, height))
        for x in range(width):
            for y in range(height):
                r, g, b = img.getpixel((x, y))
                new_alpha = random.randint(250, 255)
                new_img.putpixel((x, y), (r, g, b, new_alpha))
        output = BytesIO()
        new_img.save(output, format=format)
        return output.getvalue()
    
    def RandomizeEdgeDetection(self, imageContent, format='PNG'):
        img = cv2.imdecode(np.frombuffer(imageContent, np.uint8), cv2.IMREAD_UNCHANGED)
        if img.shape[2] == 4:
            b, g, r, a = cv2.split(img)
            gray = cv2.cvtColor(cv2.merge((b, g, r)), cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            randomized_low_threshold = random.randint(25, 75) + random.randint(-15, 15)
            randomized_high_threshold = random.randint(120, 175) + random.randint(-15, 15)
            edges = cv2.Canny(blurred, randomized_low_threshold, randomized_high_threshold)
            edges_rgb = cv2.cvtColor(cv2.merge((edges, edges, edges)), cv2.COLOR_BGR2RGBA)
            result = cv2.bitwise_and(img, edges_rgb)
            _, encoded_image = cv2.imencode(".png", result)
            return encoded_image.tobytes()
        elif img.shape[2] == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            randomized_low_threshold = random.randint(25, 75) + random.randint(-15, 15)
            randomized_high_threshold = random.randint(120, 175) + random.randint(-15, 15)
            edges = cv2.Canny(blurred, randomized_low_threshold, randomized_high_threshold)
            edges_rgb = cv2.cvtColor(cv2.merge((edges, edges, edges)), cv2.COLOR_BGR2RGB)
            result = cv2.bitwise_and(img, edges_rgb)
            _, encoded_image = cv2.imencode(".png", result)
            return encoded_image.tobytes()
        else:
            raise ValueError("Unsupported image format. Expected RGB or RGBA.")
        
    def RandomizeGeometry(self, imageContent, format='PNG'):
        img = PILImage.open(BytesIO(imageContent))
        transformation = random.choice(['rotate', 'scale', 'translate'])
        if transformation == 'rotate':
            angle = random.uniform(-30, 30)
            transformed_img = img.rotate(angle, expand=True)
        elif transformation == 'scale':
            scale_factor_x = random.uniform(0.5, 2.0)
            scale_factor_y = random.uniform(0.5, 2.0)
            transformed_img = img.resize((int(img.width * scale_factor_x), int(img.height * scale_factor_y)))
        elif transformation == 'translate':
            translate_x = random.randint(-50, 50)
            translate_y = random.randint(-50, 50)
            transformed_img = img.transform(img.size, PILImage.AFFINE, (1, 0, translate_x, 0, 1, translate_y))
        output = BytesIO()
        transformed_img.save(output, format=format)
        return output.getvalue()
    
    def ShowOrbExtractionDetections(self, imageContent, format='PNG'):
        img = cv2.imdecode(np.frombuffer(imageContent, np.uint8), cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        orb = cv2.ORB_create()
        keypoints, descriptors = orb.detectAndCompute(gray, None)
        img_with_keypoints = cv2.drawKeypoints(img, keypoints, None, color=(0,255,0), flags=0)
        _, encoded_image = cv2.imencode(".png", img_with_keypoints)
        return encoded_image.tobytes()
    
    def ShowSIFTExtractionDetections(self, imageContent, format='PNG'):
        img = cv2.imdecode(np.frombuffer(imageContent, np.uint8), cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        sift = cv2.SIFT_create()
        keypoints, descriptors = sift.detectAndCompute(gray, None)
        img_with_keypoints = cv2.drawKeypoints(img, keypoints, None, color=(0,255,0), flags=0)
        _, encoded_image = cv2.imencode(".png", img_with_keypoints)
        return encoded_image.tobytes()
    
    def DetectAvailableAlgorithms(self):
        available_algorithms = []
        if hasattr(cv2, 'ORB_create'):
            available_algorithms.append('ORB')
        if hasattr(cv2, 'SIFT_create'):
            available_algorithms.append('SIFT')
        if hasattr(cv2, 'AKAZE_create'):
            available_algorithms.append('AKAZE')
        if hasattr(cv2, 'KAZE_create'):
            available_algorithms.append('KAZE')
        return available_algorithms
    
    def DetectRandomAlgorithms(self, imageContent, format='PNG'):
        if not self.AvailableAlgorithms:
            raise ValueError("No algorithm detection available.")
        img = cv2.imdecode(np.frombuffer(imageContent, np.uint8), cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        selected_algorithm = random.choice(self.AvailableAlgorithms)
        print("Selected feature detection algorithm:", selected_algorithm)
        if selected_algorithm == 'ORB':
            detector = cv2.ORB_create()
        elif selected_algorithm == 'SIFT':
            detector = cv2.SIFT_create()
        elif selected_algorithm == 'AKAZE':
            detector = cv2.AKAZE_create()
        elif selected_algorithm == 'KAZE':
            detector = cv2.KAZE_create()
        keypoints, descriptors = detector.detectAndCompute(gray, None)
        img_with_keypoints = cv2.drawKeypoints(img, keypoints, None, color=(0,255,0), flags=0)
        _, encoded_image = cv2.imencode(".png", img_with_keypoints)
        return encoded_image.tobytes()

    def AddRandomPositionWatermark(self, imageContent, markContent, format='PNG'):
        main_img = PILImage.open(BytesIO(imageContent))
        watermark_img = PILImage.open(BytesIO(markContent))
        watermark_img = watermark_img.convert("RGBA")
        if watermark_img.size[0] > main_img.size[0] or watermark_img.size[1] > watermark_img.size[1]:
            watermark_img = watermark_img.resize((main_img.size[0] // 2, main_img.size[1] // 2), PILImage.ANTIALIAS)
        position = (random.randint(0, main_img.width - watermark_img.width), main_img.height - watermark_img.height)
        layer = PILImage.new("RGBA", main_img.size, (0,0,0,0))
        layer.paste(watermark_img, position, mask=watermark_img)
        watermark_img = PILImage.alpha_composite(main_img.convert("RGBA"), layer)
        watermark_img = watermark_img.convert("RGB")
        output = BytesIO()
        watermark_img.save(output, format=format)
        return output.getvalue()

    def PreviewBytesImage(self, imageContent):
        img = PILImage.open(BytesIO(imageContent))
        img.show()

image = Image()

def ManipulatePNGImage(ImageContent):
    ran = random.randint(1, 3)
    if ran == 1:
        modified_image_content = manipulateDotting(ImageContent, ".png")
    elif ran == 2:
        modified_image_content = image.RandomizeScale(ImageContent, "PNG")
    elif ran == 3:
        modified_image_content = image.RandomizeDot(ImageContent, "PNG")
    return modified_image_content

def ManipulateJPGImage(ImageContent):
    ran = random.randint(1, 3)
    if ran == 1:
        modified_image_content = manipulateDotting(ImageContent, ".jpg")
    elif ran == 2:
        modified_image_content = image.RandomizeScale(ImageContent, "JPEG")
    elif ran == 3:
        modified_image_content = image.RandomizeDot(ImageContent, "JPEG")
    return modified_image_content

def GetImageContentFromURL(Url):
    try:
        response = requests.get(Url)
        return response.content
    except Exception as e:
        print(f"Error: {e}")
        return None

def ConvertFileToExtension(ImageContent, FileType="PNG"):
    original_image = PILImage.open(io.BytesIO(ImageContent)).convert('RGBA')
    if FileType.lower() not in ['png', 'gif', 'bmp', 'tiff']:
        original_image = original_image.convert('RGB')
    modified_image_content = io.BytesIO()
    original_image.save(modified_image_content, format=FileType.upper())
    return modified_image_content.getvalue()

def ReadFileByFilePath(filePath):
    filePath = filePath.replace('"', '').replace('/', '\\')
    with open(filePath, 'rb') as file:
        content = file.read()
    return content
