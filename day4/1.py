import pandas as pd
from datetime import datetime, timedelta
import random

import os
os.environ["llama_key"] = os.getenv("GROQ_API_KEY", "")

data = []

for i in range(20):
    data.append({
        "table_name": f"table_{i}",
        "description": "Contains customer PII" if i % 3 == 0 else "Contains transactions",
        "columns": "id, name, email" if i % 3 == 0 else "id, amount",
        "last_updated": str(datetime.now() - timedelta(days=random.randint(1, 10)))
    })

df = pd.DataFrame(data)
df.to_csv("catalog.csv", index=False)