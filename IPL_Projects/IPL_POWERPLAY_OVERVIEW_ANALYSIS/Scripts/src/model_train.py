from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from pre_process import create_pp_model
from data_loader import deliveries,matches


pp_model=create_pp_model(deliveries,matches)
##split
X=pp_model.drop(columns=['total_runs','team1','team2'])
Y=pp_model['total_runs']

##test
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=42)

from sklearn.linear_model import LinearRegression

# train 
model=LinearRegression()
model.fit(X_train,Y_train)
Y_pred=model.predict(X_test)

#outputing the predicted value
import matplotlib.pyplot as plt

plt.scatter(Y_test,Y_pred)
plt.xlabel("Actual runs")
plt.ylabel("Predicted runs")
plt.title("Actual vs predicted")
plt.show()

print(Y_pred[:10])
import pandas as pd
comparison=pd.DataFrame({
    "Actual":Y_test.values,
    "Predicted":Y_pred
})
comparison.sort_values(by="Actual").head(30)

