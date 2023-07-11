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
