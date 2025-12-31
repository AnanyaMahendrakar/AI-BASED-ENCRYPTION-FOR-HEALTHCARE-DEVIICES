try:
    import pandas as pd  # type: ignore
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
    import pandas as pd  # type: ignore
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("ai_algorithm_training_data.csv")

X = df[['role', 'file_type', 'sensitivity', 'file_size_kb', 'access_frequency']]
y = df['algorithm_id']

model = RandomForestClassifier(n_estimators=150, random_state=42)
model.fit(X, y)

joblib.dump(model, "ai_algorithm_selector.pkl")
print("✅ AI Algorithm Selector Model trained & saved.")