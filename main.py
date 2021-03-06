import streamlit as st 
import numpy as np 
import pandas as pd

import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split

from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score

# Cria o título do app que será escrito na área principal(lado direito da tela)
st.title('Streamlit Example')

# Escreve a string na tela
st.write("""
# Explore different classifier and datasets
Which one is the best?
""")

# Cria uma caixa de interação do tipo selectbox na sidebar(lado esquerdo da tela)
dataset_name = st.sidebar.selectbox(
    'Select Dataset',
    ('Iris', 'Breast Cancer', 'Wine')
)

# Transforma a variavel com o nome do dataset em string e escreve na tela. Escrever # no começo da string dá uma enfase na fonte(Negrito e tamanho)
st.write(f"## {dataset_name} Dataset")

# Selectbox com os classificadores
classifier_name = st.sidebar.selectbox(
    'Select classifier',
    ('KNN', 'SVM', 'Random Forest')
)
# Funçao de carregamento do dataset selecionado, retorna dados, targets e nome das classes
def get_dataset(name):
    data = None
    if name == 'Iris':
        data = datasets.load_iris()
    elif name == 'Wine':
        data = datasets.load_wine()
    else:
        data = datasets.load_breast_cancer()
    X = data.data
    y = data.target
    y_names = data.target_names
    return X, y, y_names

# Escreve algumas caracteristicas do dataset
X, y , y_names= get_dataset(dataset_name)
st.write('Shape of dataset:', X.shape)
st.write('number of classes:', len(np.unique(y)))

# Cria a interface para selecionar os parametros dos classificadores na sidebar utilizando sliders
def add_parameter_ui(clf_name):
    params = dict()
    if clf_name == 'SVM':
        C = st.sidebar.slider('C', 0.01, 10.0)
        params['C'] = C
    elif clf_name == 'KNN':
        K = st.sidebar.slider('K', 1, 15)
        params['K'] = K
    else:
        max_depth = st.sidebar.slider('max_depth', 2, 15)
        params['max_depth'] = max_depth
        n_estimators = st.sidebar.slider('n_estimators', 1, 100)
        params['n_estimators'] = n_estimators
    return params

params = add_parameter_ui(classifier_name)

# Função que cria o classificador com os parametros escolhidos
def get_classifier(clf_name, params):
    clf = None
    if clf_name == 'SVM':
        clf = SVC(C=params['C'])
    elif clf_name == 'KNN':
        clf = KNeighborsClassifier(n_neighbors=params['K'])
    else:
        clf = clf = RandomForestClassifier(n_estimators=params['n_estimators'], 
            max_depth=params['max_depth'], random_state=1234)
    return clf

clf = get_classifier(classifier_name, params)
#### Classificação ####

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1234)

clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

acc = accuracy_score(y_test, y_pred)

st.write(f'Classifier = {classifier_name}')
st.write(f'Accuracy =', acc)

#### PLOT DATASET ####
# Project the data onto the 2 primary principal components
pca = PCA(2)
X_projected = pca.fit_transform(X)

x1 = X_projected[:, 0]
x2 = X_projected[:, 1]

fig = plt.figure()
plt.scatter(x1, x2,
        c=y, alpha=0.8,
        cmap='viridis')

plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.colorbar()

#plt.show()
st.pyplot(fig)

#### Para o dataset iris, cria a interface para o usuario dar a entrada de dados novos para classificação ####
if dataset_name=='Iris':
    # Entradas numericas no sidebar para cada feature do dataset iris
    st.sidebar.write("Input Single Sample")
    sepal_lenght=st.sidebar.number_input('Sepal Lenght')
    sepal_width=st.sidebar.number_input('Sepal Width')
    petal_lenght=st.sidebar.number_input('Petal Lenght')
    petal_width=st.sidebar.number_input('Petal Width')
    
    # Junta as entradas do usuario em um unico array no shape requerido
    x_user_single=np.array([sepal_lenght,sepal_width,petal_lenght,petal_width])
    x_user_single=np.reshape(x_user_single,(1,-1))
    # Previsão da amostra do usuario
    y_pred_user=clf.predict(x_user_single)
    # Obtenção do nome da classe prevista
    user_class=y_names[y_pred_user]
    user_class=user_class[0]
    
    
    st.write('#### Single Sample Predictions')
    st.write(f'Class =', user_class)
    
    st.write('#### Multiple Samples Predictions')
    st.sidebar.write('Input Multiples Samples')
    
    # Cria a interface para o usuario fazer upload de um csv com varias amostras para classificação
    uploaded_file = st.sidebar.file_uploader("Choose a file")
    if uploaded_file is not None:

         # Can be used wherever a "file-like" object is accepted:
         # Utiliza o pandas para obter os dados do csv
         dataframe = pd.read_csv(uploaded_file)
         # Uniformiza o tipo dos dados
         dataframe=dataframe.astype(float)
         # Pandas Dataframe -> Numpy Array
         x_user_multi=dataframe.to_numpy()
         # Previsão
         y_user_multi=clf.predict(x_user_multi)
         user_class_multi=y_names[y_user_multi]
         # Cria uma nova coluna do dataframe com as previsões
         dataframe['Prediction']=user_class_multi
         # Escreve na tela o novo dataframe com as previsões
         st.write(dataframe)
       

    
