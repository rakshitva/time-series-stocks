import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from additional import DatasetGenerator
from keras.models import load_model

st.title("Stock Prediction")

user_input = st.text_input("Enter the Stock Symbol","Type Here")
df = pd.read_csv(f'./equities/{user_input}.csv')

st.subheader('Data till 2024')
st.write(df.describe())

model = load_model("model.h5")
ed_date = '2023-06-01'
df["Date"] = pd.to_datetime(df["Date"])
df_Train_X, df_Train_Y, df_Test_X, df_Test_Y,scale = DatasetGenerator.Dataset(df, ed_date)

y_predicted = model.predict(df_Test_X)

y_predicted = y_predicted/scale
df_Test_X = df_Test_X/scale
split_date = '2023'
st.subheader("Prediction vs Original")
fig = plt.figure(figsize=(20,12))
plt.plot(df['Date'][df['Date'] < '2023-06-01'], df['Adj Close'][df['Date'] < '2023-06-01'], label = 'Training')
plt.plot(df['Date'][df['Date'] >= '2023-06-01'], df['Adj Close'][df['Date'] >= '2023-06-01'], label = 'Testing')
plt.plot(df['Date'][df['Date'] >= '2023-06-14'], y_predicted.reshape(-1), label = 'Predictions')
plt.xlim(pd.Timestamp("2020-01-01"),pd.Timestamp("2024-04-30"))
plt.xlabel('Time')
plt.ylabel('Closing Price')
plt.legend(loc = 'best')
st.pyplot(fig)