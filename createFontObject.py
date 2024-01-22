import sys
import os
import glob

# Mapping of font file names to their corresponding FontWeight in Kotlin
font_weight_mapping = {
    "thin": "FontWeight.Thin",
    "extralight": "FontWeight.ExtraLight",
    "light": "FontWeight.Light",
    "regular": "FontWeight.Normal",
    "medium": "FontWeight.Medium",
    "semibold": "FontWeight.SemiBold",
    "bold": "FontWeight.Bold",
    "extrabold": "FontWeight.ExtraBold",
    "black": "FontWeight.Black",
}

font_style_mapping = {
    "italic": "FontStyle.Italic"
}

def generate_font_kotlin_object(font_files):
    kotlin_object = "object Fonts {\n"
    kotlin_object += "    val fontFamily = FontFamily(\n"
    
    for font_file in font_files:
        normalized_name = os.path.basename(font_file).lower().replace(".ttf", "")
        weight = "FontWeight.Normal"
        style = ""
        
        for key, value in font_weight_mapping.items():
            if key in normalized_name:
                weight = value
                break
        
        for key, value in font_style_mapping.items():
            if key in normalized_name:
                style = f", style = {value}"
                break
            
        resource_name = normalized_name.replace("-", "_")
        
        kotlin_object += f"        Font(\n"
        kotlin_object += f"            R.font.{resource_name},\n"
        kotlin_object += f"            {weight}{style}\n"
        kotlin_object += f"        ),\n"
    
    kotlin_object = kotlin_object.rstrip(',\n') + "\n"
    kotlin_object += "    )\n"
    kotlin_object += "}\n\n"
    kotlin_object += "val fontFamily = Fonts.fontFamily"
    
    return kotlin_object

# Check for command-line arguments for folder path or use the current directory
folder_path = sys.argv[1] if len(sys.argv) > 1 else "."

# List all .ttf files in the specified folder
font_files = glob.glob(os.path.join(folder_path, "*.ttf"))

# Generate the Kotlin object
kotlin_code = generate_font_kotlin_object(font_files)

# Create the .kt file named after the font, assuming all fonts have the same base name
if font_files:
    font_base_name = os.path.basename(font_files[0]).lower().split('_')[0]
    kt_file_name = f"{font_base_name.capitalize()}Fonts.kt"
    kt_file_path = os.path.join(folder_path, kt_file_name)

    with open(kt_file_path, 'w') as kt_file:
        kt_file.write(kotlin_code)

    print(f"Kotlin file created: {kt_file_path}")
else:
    print("No .ttf font files found in the specified directory.")
