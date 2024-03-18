# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("Felladrin/Sheared-Pythia-160m-WebGLM-QA", 
                                          trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("Felladrin/Sheared-Pythia-160m-WebGLM-QA",
                                            trust_remote_code=True)
#TODO Add code to download chroma model for embedding- /root/.cache/chroma/onnx_models/all-MiniLM-L6-v2/onnx.tar.gz
