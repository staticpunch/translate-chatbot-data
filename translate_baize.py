import json 
import glob
from tqdm import tqdm 
from nltk.tokenize import sent_tokenize
from deep_translator import GoogleTranslator
import sys
import re 

proxies = {
    "https": "http://10.30.153.169:3128",
    "http": "http://10.30.153.169:3128"
}
translator = GoogleTranslator(source="en", target="vi", proxies=proxies)

def group_chunks(text, max_length=4999):
    sentences = sent_tokenize(text)
    
    chunks = [sentences[0]]
    for string in sentences[1:]:
        current_length = len(chunks[-1])
        if current_length + len(string) > max_length: 
            chunks.append(string[:max_length])
        else:
            chunks[-1] += " " + string

    return chunks

def translate_long(text, max_length=4999):
    human, ai = "[|A|]", "[|B|]"
    chunks = group_chunks(text, max_length)

    translated_chunks = translator.translate_batch(chunks)
    text = " ".join(translated_chunks)
    text = text.replace(human, f"\n{human}").replace(ai, f"\n{ai}")
    text = re.sub(r"\n+", "\n", text).strip()
    return text


def format_for_translate(input_text):
    system_prompt = "The conversation between human and AI assistant."
    text = input_text.strip(system_prompt).strip()
    text = text.replace("[|Human|]", "[|A|]").replace("[|AI|]", "[|B|]")
    return text

if __name__ == "__main__":
    chat_file = glob.glob("data/*chat_data*")[0]
    save_file = chat_file.split("chat_data")[0] + "translated.json"
    chat_data = json.load(open(chat_file))
    print(f">>> Total: {len(chat_data)} samples")
    for i, chat in enumerate(chat_data):
        chat["id"] = i
        chat["input"] = format_for_translate(chat["input"])

    try:
        with open(save_file, "r") as file: 
            continue_from = 0
            for line in file: 
                continue_from += 1
            chat_data = chat_data[continue_from:]
            print(f">>> Continue translating from sample {continue_from}")
    except:
        pass 

    with open(save_file, "a+") as file:
        for sample in tqdm(chat_data):
            sample["translation"] = translate_long(sample["input"])
            file.write(json.dumps(sample, ensure_ascii=False) + "\n")
            
{'loss': 1.2812, 'learning_rate': 0.00019908842297174112, 'epoch': 0.09}
{'loss': 1.2778, 'learning_rate': 0.00019817684594348222, 'epoch': 0.09}
{'loss': 1.2844, 'learning_rate': 0.00019726526891522336, 'epoch': 0.1}
{'loss': 1.2634, 'learning_rate': 0.00019635369188696446, 'epoch': 0.1}
{'loss': 1.2645, 'learning_rate': 0.00019544211485870557, 'epoch': 0.1}
{'loss': 1.2745, 'learning_rate': 0.00019453053783044668, 'epoch': 0.11}
{'loss': 1.263, 'learning_rate': 0.00019361896080218779, 'epoch': 0.11}
{'loss': 1.2701, 'learning_rate': 0.0001927073837739289, 'epoch': 0.12}
{'loss': 1.2916, 'learning_rate': 0.00019179580674567003, 'epoch': 0.12}
{'loss': 1.2925, 'learning_rate': 0.00019088422971741113, 'epoch': 0.13}
{'loss': 1.3061, 'learning_rate': 0.00018997265268915224, 'epoch': 0.13}
{'loss': 1.3237, 'learning_rate': 0.00018906107566089335, 'epoch': 0.13}
{'loss': 34023.7906, 'learning_rate': 0.00018814949863263448, 'epoch': 0.14}
{'loss': 0.0, 'learning_rate': 0.0001872379216043756, 'epoch': 0.14}
