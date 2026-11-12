import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Step 1: Load dataset
data = pd.read_csv("intent_dataset.csv")
data = data.dropna(subset=["text", "intent"])

X = data["text"]
y = data["intent"]

# Step 2: Split dataset into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Step 3: Create NLP model
model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("classifier", LogisticRegression(max_iter=1000))
])

# Step 4: Train model
model.fit(X_train, y_train)

# Step 5: Test model
predictions = model.predict(X_test)

print("Classification Report:")
print(classification_report(y_test, predictions, zero_division=0))

# Step 6: Save trained model
joblib.dump(model, "intent_model.joblib")

print("Model trained and saved successfully!")