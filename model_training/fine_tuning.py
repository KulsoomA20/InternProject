from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset
import torch

model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

tokenizer.pad_token = tokenizer.eos_token


# Load your dataset — replace with your own or use huggingface dataset
# For example: using 'empathetic_dialogues'
dataset = load_dataset("empathetic_dialogues", trust_remote_code=True)


# Preprocess data
def tokenize_function(example):
    return tokenizer(example['utterance'], truncation=True, padding="max_length", max_length=128)

# Tokenize dataset
tokenized_datasets = dataset["train"].map(tokenize_function, batched=True)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    #evaluation_strategy="epoch",
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=3,
    save_total_limit=2,
    logging_dir="./logs",
    logging_steps=10,
    fp16=torch.cuda.is_available(),
)

# Trainer setup
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# Start training
trainer.train()

# Save model
model.save_pretrained("./fine_tuned_model")
tokenizer.save_pretrained("./fine_tuned_model")
