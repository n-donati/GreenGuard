import openvino as ov
from openvino.tools import mo
from openvino.runtime import serialize

# Path to your SavedModel directory
saved_model_path = "cucumber_final"

ov_model = mo.convert_model(saved_model_path, 
                            model_name="cucumber_final",
                            framework="tf", input_shape=[1, 224, 224, 3])  

# Specify the output directory and filenames
output_dir = "openvino_model"
xml_filename = "cucumber_model.xml"
bin_filename = "cucumber_model.bin"

# Serialize the model to IR format
serialize(ov_model, xml_filename, bin_filename)

print(f"Model converted and saved to {output_dir}/{xml_filename} and {output_dir}/{bin_filename}")