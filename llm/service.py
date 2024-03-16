from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
import os

class LLMService:
    def __init__(self, model_name, hf_token = None, device = 'cpu'):
        hf_token = os.environ['HF_TOKEN']
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, token = hf_token)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, token = hf_token).to(device)
    
    def query(self, relevant_texts, query, max_new_tokens = 500, temperature = 0.7, do_sample = True):
        context = "[" + ",".join(relevant_texts) + "]" 
        prompt = self._get_prompt(context, query)
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
        streamer = TextStreamer(self.tokenizer)
        outputs = self.model.generate(input_ids, do_sample=do_sample, temperature=temperature, streamer=streamer, max_new_tokens=max_new_tokens)
        generated_text = self.tokenizer.batch_decode(outputs, skip_special_tokens = True)
        return generated_text

    def _get_prompt(self, context, query):
        prompt = f'You are a Large Language Chat Model. User: context: {context} \n query: {query} \n Constraint: Please answer the prompt based on the context provided. And if the answer is not present in the context, then answer only if you are sure. \n Model: '
        return prompt
