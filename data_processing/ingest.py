import pandas as pd
from .document import Document

def load_csv(file_path):
    df = pd.read_csv(file_path)
    docs = []
    for _, row in df.iterrows():
        doc = Document(content=row['description'], metadata=row.to_dict())
        docs.append(doc)
    return docs
