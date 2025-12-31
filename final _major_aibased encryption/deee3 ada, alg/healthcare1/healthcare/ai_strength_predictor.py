try:
    import pandas as pd  # type: ignore
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
    import pandas as pd  # type: ignore
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("ai_strength_training_data.csv")

X = df[['role', 'sensitivity', 'file_size_kb']]
y = df['strength']

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

joblib.dump(model, "ai_strength_predictor.pkl")
print("✅ AI Strength Predictor Model trained & saved.")