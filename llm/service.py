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
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
    
    def query(self, relevant_texts, query, max_new_tokens = 500, temperature = 0.7, do_sample = True):
        context = "[" + ",".join(relevant_texts) + "]" 
        prompt = self._get_prompt(context, query)
        logging.debug(f"Prompt: {prompt}")
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
        output = self.model.generate(input_ids, do_sample=do_sample, temperature=temperature, max_new_tokens=max_new_tokens)
        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return generated_text

    def _get_prompt(self, context, query):
        prompt = f'You are a Large Language Chat Model. User: context: {context} \n query: {query} \n Constraint: Please answer the prompt based on the context provided. And if the answer is not present in the context, then answer only if you are sure. \n Model: '
        return prompt
