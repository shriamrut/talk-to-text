from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
import os
import torch
import logging

class LLMService:
    def __init__(self):
        model_name = os.environ["HF_MODEL"]
        tokenizer_model_name = os.environ["HF_TOKENIZER_MODEL"]
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.device = device
        self.logger = logging.getLogger(__name__)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
    
    def query(self, relevant_texts, query, max_new_tokens = 500, temperature = 0.7, do_sample = True):
        prompt = self._form_prompt(relevant_texts=relevant_texts, query = query)
        self.logger.debug(f"Prompt: {prompt}")
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
        output = self.model.generate(input_ids, do_sample=do_sample, temperature=temperature, max_new_tokens=max_new_tokens)
        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return generated_text

    def _form_prompt(self, relevant_texts, query):
        context = "<|references|> \n"
        for i, relevant_text in enumerate(relevant_texts):
            context += f"[{i+1}] {relevant_text}\n" 
        context += "</s>"
        context += f"<|question|> {query} </s>\n"
        context += "<|answer|> "
        return context
