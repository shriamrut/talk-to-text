# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("openai-community/gpt2", 
                                          trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("openai-community/gpt2",
                                            trust_remote_code=True)
