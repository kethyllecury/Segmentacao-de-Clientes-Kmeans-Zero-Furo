import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from yellowbrick.cluster import KElbowVisualizer
from sklearn.metrics import silhouette_score

file_path = r'C:\Users\sigab\OneDrive\Área de Trabalho\machine\kmeans\vendas.xlsx'
df = pd.read_excel(file_path)

df['codigo'] = pd.factorize(df['codigo'])[0]  
df['categoria.id'] = pd.factorize(df['categoria.id'])[0] 

df_cliente = df.groupby('contato.id').agg(
    total_quantidade=('quantidade', 'sum'),
    total_valor=('valor', 'sum'),
    num_produtos=('codigo', 'nunique')
).reset_index()

df_cliente = df_cliente.fillna(0)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_cliente[['total_quantidade', 'total_valor', 'num_produtos']])

model = KMeans(n_init=10)
visualizer = KElbowVisualizer(model, k=(2, 10))  
visualizer.fit(X_scaled)


k = visualizer.elbow_value_

kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
df_cliente['cluster'] = kmeans.fit_predict(X_scaled)

plt.figure(figsize=(8, 5))
sns.scatterplot(x=df_cliente['total_quantidade'], y=df_cliente['total_valor'], hue=df_cliente['cluster'], palette='viridis')
plt.xlabel("Total de Quantidade Comprada")
plt.ylabel("Total de Valor Gasto")
plt.title("Segmentação de Clientes")
plt.legend(title="Cluster")
plt.show()

score = silhouette_score(X_scaled, df_cliente['cluster'])
print(f'Silhouette Score: {score}')