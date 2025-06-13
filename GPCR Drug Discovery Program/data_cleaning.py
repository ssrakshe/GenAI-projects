import pandas as pd

# Load the uploaded CSV file
file_path = r"C:\Users\lenovo\OneDrive\Desktop\IIT Chicago\RA\GPCR_AI_RAG task\data\GPCRTargets.csv"
df = pd.read_csv(file_path)
df_cleaned = pd.read_csv(file_path, skiprows=1)
df_cleaned.columns.tolist(), df_cleaned.head()
df_cleaned["Target name"] = df_cleaned["Target name"].str.replace(r"<.*?>", "", regex=True)
df_selected = df_cleaned[[
    "Target name",
    "HGNC symbol",
    "HGNC name",
    "synonyms",
    "Family name"
]].dropna(subset=["Target name", "HGNC symbol"])
output_path = "./cleaned_GPCR_targets.csv"
df_selected.to_csv(output_path, index=False)

print(df_selected.head())
