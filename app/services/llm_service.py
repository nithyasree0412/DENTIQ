import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM
)


class LLMService:

    def __init__(
        self,
        model_name="Qwen/Qwen2.5-1.5B-Instruct"
    ):
        self.model_name = model_name

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name
        )

        self.generation_model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16
        ).to("cuda")

        print("Qwen loaded")

    def generate(
        self,
        messages,
        max_new_tokens=300,
        temperature=0.2,
        top_p=0.9
    ):

        formatted_prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(
            formatted_prompt,
            return_tensors="pt"
        ).to(
            self.generation_model.device
        )

        with torch.no_grad():

            outputs = self.generation_model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                do_sample=True,
                top_p=top_p
            )

        generated_tokens = outputs[0][
            inputs["input_ids"].shape[1]:
        ]

        final_answer = self.tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True
        )

        return final_answer