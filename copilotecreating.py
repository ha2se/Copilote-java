from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Path to your local model directory
model_path = r"C:\Users\readf\OneDrive\Desktop\fine tuning project\javamodel"  

# Load the model and tokenizer from the local directory
model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Sample Java code input
sample_input = "public class HelloWorld { public static void main(String[] args) { System.out.println(\"Hello, World!\"); } }"

# Tokenize the input
inputs = tokenizer(sample_input, return_tensors="pt")

# Generate output without gradients
with torch.no_grad():
    outputs = model.generate(**inputs, max_length=100, num_return_sequences=1)

# Decode the generated tokens to text
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

# Print the generated text
print(generated_text)
