import json
from dotenv import load_dotenv
import openai
import os
import tiktoken

load_dotenv()
openai.organization = os.getenv("openai_org")
openai.api_key = os.getenv("openai_secret")


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0613":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            # every message follows <im_start>{role/name}\n{content}<im_end>\n
            num_tokens += 4
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")


def summarize(headline):
    # allow 3 retries for a valid response
    for i in range(3):
        try:
            return _summarize(headline)
        except:
            pass


def _summarize(article):

    body = "sammanfatta artikeln nedan till cirka 100-200 ord i 1-3 stycken. Texten ska vara lättläst, opartisk och professionell. Använd ny rad när lämpligt så texten blir luftig. Ignorera länkar till samt information om poddar, nyhetspodd, premium tidningar Du ska också lägga till ett fält med hur viktig den här artikeln är för läsaren att klicka på, en siffra från 1-5. Du ska svara i JSON format med fälten title och body: som följande: {\"title\": \"...\", \"body\": \"...\", \"importance\": ...}."
    data = json.dumps(article)

    while num_tokens_from_messages([
        {"role": "system", "content": body},
        {"role": "assistant", "content": data},
    ]) > 4000:
        data = data[0:-100]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": body},
            {"role": "assistant", "content": data},
        ]
    )
    message = response["choices"][0]["message"]["content"]
    summary = json.loads(message)
    return summary


def group_headlines(headline):
    # allow 3 retries for a valid response
    for i in range(3):
        try:
            return _group_headlines(headline)
        except:
            pass


def _group_headlines(headlines):
    body = "Gruppera de mest intressanta titlar i 3 grupper. Svara i JSON format med nyhetens namn som nyckel och en array av ID till artiklarna som ingår i den kategorin. Exempel: {\"Här riskeras människoliv\": [...],  \"Brott och olyckor\": [...]}. JSON strängen måste vara komplett. Namnen till kategorierna ska vara max några ord men spännande och reflektera kopplingen mellan artiklarna. Varje artikel får vara med i mest en grupp, och grupperna får innehålla max 5 artiklar."

    data = json.dumps(headlines).replace("}", "").replace("{", "")

    while num_tokens_from_messages([
        {"role": "system", "content": body},
        {"role": "assistant", "content": data},
    ]) > 4000:
        data = data[0:-100]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": body},
            {"role": "assistant", "content": data},
        ]
    )
    message = response["choices"][0]["message"]["content"]

    groups = json.loads(message)
    return groups


def pick_headline_topic(headline):
    # allow 3 retries for a valid response
    for i in range(3):
        try:
            return _pick_headline_topic(headline)
        except:
            pass


def _pick_headline_topic(headline):
    topics = "Nyheter, Inrikes, Utrikes, Ekonomi, Politik, Opinion, Sport, Nöje & kultur, Tech"
    body = f"Vilken kategori passar bäst för denna titel: {headline}? Svara med en av följande kategorier: {topics} i JSON format med fältet category: som följande: {{\"category\": \"...\"}}."

    data = json.dumps(headline)
    while num_tokens_from_messages([
        {"role": "system", "content": body},
        {"role": "assistant", "content": data},
    ]) > 4000:
        data = data[0:-100]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": body},
            {"role": "assistant", "content": data},
        ]
    )
    message = response["choices"][0]["message"]["content"]
    category = json.loads(message)["category"]
    return category
