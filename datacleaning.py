import csv 
import json
import dataset
from pprint import pprint
import pandas as pd 

df=pd.read_csv('data1.csv')
print(len(df))
df.head()
training_data=df[['Title','Body']]
print(training_data)
training_data.to_json('datajsontrinng.json',index=False)
def convert(csv_file_path,json_file_path):
  with open(csv_file_path,'r') as csv_file:
    csv_reader=csv.DictReader(csv_file)
    data=[]
    for row in csv_reader:
       data.append(row)
  json_data=json.dumps(data)
  with open(json_file_path,'w') as jsonfile:
    jsonfile.write(json_data)
  return(jsonfile)
csv_file="data1.csv"
json_file_path='jsondata.json'
#iporting a pretrained model 
from transformers import GPTNeoXForCausalLM, AutoTokenizer

model = GPTNeoXForCausalLM.from_pretrained(
  "EleutherAI/pythia-70m-deduped",
  revision="step3000",
  cache_dir="./pythia-70m-deduped/step3000",
)

tokenizer = AutoTokenizer.from_pretrained(
  "EleutherAI/pythia-70m-deduped",
  revision="step3000",
  cache_dir="./pythia-70m-deduped/step3000",
)
text="hi ,how are you?"
encoded_text=tokenizer.decode(text)["input_ids"]
#prepare instruction dataset
file_name="datajsontrinng.json"
instruction_dataset_df=pd.read_json(file_name,lines=True)
examples=instruction_dataset_df.to_dict()
if "Title" in examples and "Body" in examples:
  text=examples["Title"][0] + examples["Body"][0]
elif"instruction"  in examples and "response" in examples:
  text=examples["instruction"][0] + examples["response"][0]
elif "Title" in examples and "body" in examples:
  text=examples["Title"][0] + examples["body"][0]
else:
  text=examples["text"][0]    
prompt_template = """### Question:
{question}

### Answer:"""
num_examples =len(examples["Title"])
finetuning_dataset=[]
for i in range (num_examples):
  question=examples["Title"][i]
  answear=examples["Body"][i]
  text_with_prompt_template=prompt_template.format(question=question)
  finetuning_dataset.append({"question":text_with_prompt_template,"answear":answear})
  pprint("one data point in the finetuning dataset:")
  pprint(finetuning_dataset[0])
