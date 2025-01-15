import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import pickle

# Cargar el dataset (asegúrate de tener los datos en un archivo CSV)
df = pd.read_csv("data/correos.csv")  # Ruta al archivo CSV con los correos etiquetados

# Preprocesar el contenido de los correos
X = df['contenido']  # Texto de los correos
y = df['etiqueta']   # Etiquetas: "legítimo" o "malicioso"

# Convertir las etiquetas a números (0 para "legítimo", 1 para "malicioso")
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Convertir el texto de los correos a vectores numéricos usando TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(X)

# Dividir los datos en conjunto de entrenamiento y conjunto de prueba (80% entrenamiento, 20% prueba)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo usando Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Guardar el modelo entrenado y el vectorizador
with open('models/modelo_spam.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

with open('models/vectorizer.pkl', 'wb') as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)

# Imprimir los resultados de la prueba del modelo
print(f'Precisión del modelo en el conjunto de prueba: {model.score(X_test, y_test)}')
