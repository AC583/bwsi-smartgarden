import PIL.Image
import google.generativeai as genai
genai.configure(api_key="AIzaSyAxhU6n6FWwQbcR6bvPcLBQX_S5YdpLYHY")

def classify_image(image_path):
    img = PIL.Image.open(image_path)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(img)
    print(response.text)
    return response.text

