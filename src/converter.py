import os
from config import *
from markitdown import MarkItDown
from PIL import Image, ImageOps
import pytesseract


def image_to_markdown(image_path):
    img = Image.open(image_path)
    img = ImageOps.grayscale(img)
    text = pytesseract.image_to_string(img, lang="fra+eng")
    return text
def markdonw_converter():
    if not os.path.isdir(DATA_INPUT_PATH):
        print("invalid input directory")
        return 0
    os.makedirs(DATA_OUTPUT_PATH, exist_ok=True)
    md = MarkItDown()
    for file in os.listdir(DATA_INPUT_PATH):
        input_path = os.path.join(DATA_INPUT_PATH, file)
        if not os.path.isfile(input_path):
            continue
        if file.endswith(".md"):
            continue
        if not file.lower().endswith(
            (".txt", ".pdf", ".docx", ".jpg", ".jpeg", ".png")
        ):
            continue
        try:
            name, ext = os.path.splitext(file)
            new_file = f"{name}_md.md"
            output_path = os.path.join(DATA_OUTPUT_PATH, new_file)
            if ext.lower() in [".jpg", ".jpeg", ".png"]:
                markdown_content = image_to_markdown(input_path)
            else:
                result = md.convert(input_path)
                markdown_content = result.markdown
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            print(f"{file} has been converted successfully as {new_file}")
        except Exception as e:
            print(f"{file} has been skipped : {e}")
markdonw_converter()
