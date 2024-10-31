import pickle

# Passo 1: Carregar o modelo
model_filename = './src/models/Iris.pkl'  # Substitua pelo caminho do seu arquivo .pkl

with open(model_filename, 'rb') as file:
    model = pickle.load(file)

# Passo 2: Obter os rótulos
# A forma de acessar os rótulos pode variar dependendo do tipo de modelo.
# Aqui estão alguns exemplos comuns:

if hasattr(model, 'classes_'):
    # Para modelos de classificação que têm o atributo 'classes_'
    labels = model.classes_
    print("Rótulos do modelo:", labels)
elif hasattr(model, 'label_binarizer_'):
    # Para modelos que usam binarização
    labels = model.label_binarizer_.classes_
    print("Rótulos do modelo:", labels)
else:
    print("O modelo não contém informações sobre rótulos.")