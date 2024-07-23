import re
import time

import requests
from bs4 import BeautifulSoup

WEBSITE_URL: str = "https://www.stubbenedge.com/"
LLM_TEMPERATURE = 0.0

website_response = requests.get(WEBSITE_URL)
soup = BeautifulSoup(website_response.text, "html.parser")
# remove script elements #
for element in soup(["style", "script"]):
    element.decompose()
# remove non-visible elements #
for element in soup.select('[style*="display:none"], [style*="visibility:hidden"]'):
    element.decompose()
text = soup.get_text(separator="\n-----\n", strip=True)
elements = text.split("\n-----\n")
clean_elements = [re.sub(r"\s+", " ", x).strip() for x in elements]
website_text = "\n".join(clean_elements)

print(f"website user-facing text contains {len(website_text.split()):,} words")

time_taken_per_question_nsecs: list[float] = []
for user_prompt in (
    '<|im_start|>user\nWhat is the name of the company whose website this is?<|im_end|>\n<|im_start|>assistant\nThe name of the company is "',
    '<|im_start|>user\nPlease describe the nature of business of the company whose website this is, in a single sentence.<|im_end|>\n<|im_start|>assistant\nHere is a summary of the nature of business of the company: "',
    "<|im_start|>user\nIs there a phone number on this website? If there is, please return it to me.<|im_end|>\nassistant\n",
    "<|im_start|>user\nWhich country is the company whose website this is based in?<|im_end|>\nassistant\n",
    "<|im_start|>user\nPlease return 10 keywords which summarise the content of this website.<|im_end|>\nassistant\n",
):
    full_prompt = f"""
<|im_start|>system
You are a helpful analyst<|im_end|>
<|im_start|>user
--START OF WEBSITE TEXT--
__website_text_here__
--END OF WEBSITE TEXT--<|im_end|>
{user_prompt}"""
    start_time = time.perf_counter()
    llm_response = requests.post(
        url="http://localhost:8080/completion",
        json={
            "prompt": full_prompt.replace("__website_text_here__", website_text),
            "n_predict": 100,
            "temp": LLM_TEMPERATURE,
        },
    ).json()["content"]
    end_time = time.perf_counter()
    print(f"query time: {(end_time-start_time):,.2f}")
    time_taken_per_question_nsecs.append(end_time - start_time)
    print(full_prompt, llm_response, sep="")

for idx, query_time in enumerate(time_taken_per_question_nsecs):
    print(f"query {idx+1}: {query_time:,.2f} seconds")
