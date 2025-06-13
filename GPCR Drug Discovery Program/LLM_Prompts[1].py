import pandas as pd
import openai
import time
import json
from openai import OpenAI
from tqdm import tqdm

input_df = pd.read_csv("cleaned_GPCR_targets.csv")
client = OpenAI(api_key=" ")

def build_prompt(row):
    return f"""
You are a biomedical research assistant helping evaluate GPCR drug targets.

Target details:
- Target Name: {row['Target name']}
- HGNC Symbol: {row['HGNC symbol']}
- HGNC Name: {row['HGNC name']}
- Synonyms: {row['synonyms']}
- Family: {row['Family name']}

Answer the following in JSON format:
{{
    "Target": "{row['Target name']}",
    "Has_Biased_Agonist": "Yes/No + short explanation",
    "Clinical_Potential": "Yes/No + reasoning",
    "Indications": ["List of indications if applicable"],
    "Indication_Needs": {{
        "Indication1": "Yes/No + explanation",
        ...
    }},
    "Suggested_Program": {{
        "Indication1": "Drug discovery approach",
        ...
    }}
}}
Keep it factual, and if data is unknown, say "Not known".
"""
def query_llm(prompt):
    try:
        response =  client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Error:", e)
        return None

output_data = []

for _, row in tqdm(input_df.iterrows(), total=len(input_df)):
    prompt = build_prompt(row)
    llm_response = query_llm(prompt)
    
    if llm_response:
        try:
            parsed = json.loads(llm_response)
            output_data.append({
                "Target name": row["Target name"],
                "HGNC symbol": row["HGNC symbol"],
                "Has_Biased_Agonist": parsed.get("Has_Biased_Agonist", ""),
                "Clinical_Potential": parsed.get("Clinical_Potential", ""),
                "Indications": ", ".join(parsed.get("Indications", [])),
                "Indication_Needs": json.dumps(parsed.get("Indication_Needs", {})),
                "Suggested_Program": json.dumps(parsed.get("Suggested_Program", {}))
            })
        except json.JSONDecodeError:
            print(f"JSON decode error for target {row['Target name']}")
            continue

    time.sleep(2)

output_df = pd.DataFrame(output_data)
output_df.to_csv("gpcr_llm_results.csv", index=False)