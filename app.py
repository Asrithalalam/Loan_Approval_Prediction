import streamlit as st
import pickle
import numpy as np
import pandas as pd

#Page Configuration
st.set_page_config(page_title="Loan Approval Prediction",
                   page_icon="🏦",
                   layout="wide")

# Load trained model
@st.cache_resource                            #Load the model only once and store it in memory
def load_model_and_scaler():
    model = pickle.load(open("loan_model.pkl", "rb"))
    scaler = pickle.load(open("scaler.pkl", "rb"))
    return model, scaler

model, scaler = load_model_and_scaler()      #the model is trained logistic regression model

st.title("Loan Approval Prediction System")

st.write("Enter applicant details to check loan approval prediction")

# User inputs
st.sidebar.header("Applicant Information")

no_of_dependents = st.sidebar.number_input("Number of Dependents",min_value=0)

education = st.sidebar.selectbox("Education",["Graduate","Not Graduate"])

self_employed = st.sidebar.selectbox("Self Employed",["Yes","No"])

income_annum = st.sidebar.number_input("Annual Income",min_value=0,max_value=100000000)

loan_amount = st.sidebar.number_input("Loan Amount",min_value=0)

loan_term = st.number_input(
    "Loan Term (Months)",
    min_value=6,
    max_value=120,
    step=6,
    help="Enter the loan repayment period in months")

cibil_score = st.sidebar.number_input("CIBIL Score",min_value=300,max_value=900)

residential_assets_value = st.sidebar.number_input("Residential Assets Value",min_value=0)
commercial_assets_value = st.sidebar.number_input("Commercial Assets Value",min_value=0)
luxury_assets_value = st.sidebar.number_input("Luxury Assets Value",min_value=0)
bank_asset_value = st.sidebar.number_input("Bank Asset Value",min_value=0)

# convert categorical values
education = 0 if education=="Graduate" else 1
self_employed = 1 if self_employed=="Yes" else 0

#model prediction
if st.button("Predict Loan Status"):

  # Create input array
    input_data = np.array([[
       no_of_dependents ,
        education,
        self_employed,
        income_annum,
        loan_amount,
        loan_term,
        cibil_score,
        residential_assets_value,
        commercial_assets_value,
        luxury_assets_value,
        bank_asset_value]])
    

    #Scale input
    input_data_scaled = scaler.transform(input_data)
    
    #predict
    prediction = model.predict(input_data_scaled)
    
    probability = model.predict_proba(input_data_scaled)      #calculates the confidence of the prediction
    approval_probability = probability[0][0] * 100
    rejection_probability = probability[0][1] * 100
    
    
    st.subheader("Prediction Result")
    
    if prediction[0] == 0:
        st.success(" ✅Loan Approved ")
    else:
        st.error(" ❌ Loan Rejected ")
    
    #Metrics
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Loan Amount", loan_amount)               

    with col2:
        st.metric("Approval Probability", f"{approval_probability:.2f}%")

        
    # Show input values/ Applicant details
    st.subheader("Applicant Details")
    
    columns = [
        "Dependents",
        "Education",
        "Self Employed",
        "Income Annum",
        "Loan Amount",
        "Loan Term (Months)",
        "CIBIL Score",
        "Residential Assets",
        "Commercial Assets",
        "Luxury Assets",
        "Bank Assets"
    ]

    input_df = pd.DataFrame(input_data, columns=columns)

   # Convert encoded values back to labels
    input_df["Education"] = input_df["Education"].map({0: "Graduate", 1: "Not Graduate"})
    input_df["Self Employed"] = input_df["Self Employed"].map({0: "No", 1: "Yes"})

   # Display table
    st.dataframe(input_df, hide_index=True)

st.write("---")
st.write("Model Used: Logistic Regression")
st.write("Machine Learning Deployment using Streamlit")  