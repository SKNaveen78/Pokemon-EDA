# importing required libraries 
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import FeatureHasher

# reading datasets 
combats=pd.read_csv("C:\\Users\\sknav\\Downloads\\FOA PROJECT\\combats.csv")
pokemon=pd.read_csv("C:\\Users\\sknav\\Downloads\\FOA PROJECT\\pokemon.csv")

# dataprocessesing and converting strings matrices using FeatureHasher
pokemon["Type 2"] = pokemon["Type 2"].fillna("NA")
# Convert "Legendary" column, False is converted to 0 and True is converted to 1.
pokemon["Legendary"] = pokemon["Legendary"].astype(int)
h1 = FeatureHasher(n_features=5, input_type='string')
h2 = FeatureHasher(n_features=5, input_type='string')
d1 = h1.transform(pokemon[["Type 1"]].values.tolist())
d2 = h2.transform(pokemon[["Type 2"]].values.tolist())

# Convert to dataframe
d1 = pd.DataFrame(data=d1.toarray())
d2 = pd.DataFrame(data=d2.toarray())

# Drop Type 1 and Type 2 column from Pokemon dataset and concatenate the above two dataframes.
pokemon = pokemon.drop(columns = ["Type 1", "Type 2"])
pokemon = pd.concat([pokemon, d1, d2], axis=1)

data = []
i = 0
for t in combats.itertuples():
    i += 1
    
    first_pokemon = t[1]
    second_pokemon = t[2]
    winner = t[3]
    
    x = pokemon.loc[pokemon["#"]==first_pokemon].values[:, 2:][0]
    y = pokemon.loc[pokemon["#"]==second_pokemon].values[:, 2:][0]
    diff = (x-y)[:6]
    z = np.concatenate((x,y))
    
    if winner == first_pokemon:
        z = np.append(z, [0])
    else:
        z = np.append(z, [1])
        
    data.append(z)
# loading pokemon stats and who won in form of a list and appending it into data for furthur use

#training the model with the above created list-data
data = np.asarray(data)
X = data[:, :-1].astype(int)
y = data[:, -1].astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
clf = RandomForestClassifier(n_estimators=100)
model = clf.fit(X_train,y_train)
pred = model.predict(X_test)
# print('Accuracy :', accuracy_score(pred, y_test))

# function to predict who will win in a fight
def prediction(nom,nom1):
    nomer = pokemon.loc[pokemon["#"]==nom].values[:, 2:][0]
    nomer1 = pokemon.loc[pokemon["#"]==nom1].values[:, 2:][0]
    nomad = np.concatenate((nomer,nomer1))
    nomad=np.array(nomad).reshape(1,-1)
    result=model.predict(nomad)
    for i in result:
        if i==1:
            dat=pokemon[pokemon['#']==nom1]
            for i in dat['Name']:
                print('\n The Winner is: ',i )
        else:
            dat=pokemon[pokemon['#']==nom]
            for i in dat['Name']:
                print('\n The Winner is: ',i )