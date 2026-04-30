import os 
from config import *
from markitdown import MarkItDown 


def markdonw_converter(): 
    if not os.path.isdir(DATA_INPUT_PATH):
        print("invalid input directory")
        return 0
    os.makedirs(DATA_OUTPUT_PATH , exist_ok=True)
    md = MarkItDown()
    for file in os.listdir(DATA_INPUT_PATH) : 
        input_path = os.path.join(DATA_INPUT_PATH,file)
        if not os.path.isfile(input_path):
            continue 
        if file.endswith(".md"):
            continue
        if not file.lower().endswith((".txt" , ".pdf" , ".docx")) : 
            continue
        try:
            result = md.convert(input_path)
            name , ext = os.path.splitext(file)
            new_file = f"{name}_md.md"
            output_path = os.path.join(DATA_OUTPUT_PATH , new_file)

            with open(output_path , "w" , encoding="utf-8") as f : 
                f.write(result.markdown)
            print(f"{file} has been converted sucessfully as {new_file}")
        except Exception as e:
            print(f"{file} has been skipped : {e}")


markdonw_converter()
