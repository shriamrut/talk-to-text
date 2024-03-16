# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

tokenizer = AutoTokenizer.from_pretrained(os.environ["HF_TOKENIZER_MODEL"], 
                                          trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(os.environ["HF_MODEL"],
                                            trust_remote_code=True)
