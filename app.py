from flask import Flask, request, render_template
import sklearn
import pickle
import pandas as pd
import numpy as np
import datetime

app = Flask(__name__)
model = pickle.load(open("DisputePred_xgb.pkl", "rb"))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/predict", methods = ["GET", "POST"])
def predict():
    if request.method == "POST":

        # Complaint ID
        Complaint_id = int(request.form["Complaint_ID"])
        

        # Complaint Received Date
        Date_Received = pd.to_datetime(request.form["Date_Recived"], format ="%Y-%m-%dT%H:%M")
        Date_Received_year = Date_Received.year
        Date_Received_month = Date_Received.month
        Date_Received_day = Date_Received.day
        
        date = datetime.datetime(Date_Received_year, Date_Received_month, Date_Received_day)
        Date_Received_weekday = date.weekday()
              
        # Date sent to company
        Date_sent = pd.to_datetime(request.form["Date_sent_to_company"], format ="%Y-%m-%dT%H:%M")
        
        # Difference in date sent and received
        Received_Sent_Date_Diff = pd.to_numeric((Date_sent - Date_Received), errors='coerce')

        
        # State
        State = request.form["State"]
        North_east = ['NJ', 'NY', 'PA', 'NH', 'MA', 'CT', 'ME', 'VT', 'RI', 'AE']
        South = ['TX', 'OK', 'VA', 'FL', 'GA', 'NC', 'LA', 'SC', 'KY', 'MD', 'DC', 'TN', 'AL', 'DE', 'MS', 'AR', 'WV', 'AS', 'PR', 'MH', 'GU', 'MP', 'FM', 'VI']
        Mid_West = ['IL', 'IN', 'NE', 'WI', 'MN', 'OH', 'MO', 'MI', 'SD', 'KS', 'IA', 'ND']
        West = ['CA', 'OR', 'WA', 'NV', 'AZ', 'NM', 'UT', 'CO', 'ID', 'AK', 'WY', 'HI', 'MT', 'AP']
        
        if State in North_east:
            State = "North_East"
            State_North_East = 1
            State_South = 0
            State_West = 0
        if State in South:
            State = "South"
            State_North_East = 0
            State_South = 1
            State_West = 0
        if State in Mid_West:
            State = "Mid_West"
            State_North_East = 0
            State_South = 0
            State_West = 0
        if State in West:
            State = "West"
            State_North_East = 0
            State_South = 0
            State_West = 1           
        
        
        # Product
        Product = request.form["Product"]
        if Product == "Mortgage":
            Product_Credit_and_Prepaid_Card = 0
            Product_Credit_reporting = 0
            Product_Debt_collection = 0
            Product_Loan_services = 0
            Product_Mortgage = 1
            Product_Other_financial_service = 0
        if Product == "Debt collection":
            Product_Credit_and_Prepaid_Card = 0
            Product_Credit_reporting = 0
            Product_Debt_collection = 1
            Product_Loan_services = 0
            Product_Mortgage = 0
            Product_Other_financial_service = 0
        if Product == "Credit reporting":
            Product_Credit_and_Prepaid_Card = 0
            Product_Credit_reporting = 1
            Product_Debt_collection = 0
            Product_Loan_services = 0
            Product_Mortgage = 0
            Product_Other_financial_service = 0
        if Product in ["Credit card", "Prepaid card"]:
            Product_Credit_and_Prepaid_Card = 1
            Product_Credit_reporting = 0
            Product_Debt_collection = 0
            Product_Loan_services = 0
            Product_Mortgage = 0
            Product_Other_financial_service = 0
        if Product in ["Money transfers", "Bank account or service"]:
            Product_Credit_and_Prepaid_Card = 0
            Product_Credit_reporting = 0
            Product_Debt_collection = 0
            Product_Loan_services = 0
            Product_Mortgage = 0
            Product_Other_financial_service = 0
        if Product in ["Consumer Loan", "Student loan", "Payday loan"]:
            Product_Credit_and_Prepaid_Card = 0
            Product_Credit_reporting = 0
            Product_Debt_collection = 0
            Product_Loan_services = 1
            Product_Mortgage = 0
            Product_Other_financial_service = 0
        if Product == "Other financial service":
            Product_Credit_and_Prepaid_Card = 0
            Product_Credit_reporting = 0
            Product_Debt_collection = 0
            Product_Loan_services = 0
            Product_Mortgage = 0
            Product_Other_financial_service = 1
            
        
        # Sub Product
        Sub_product = request.form["Sub_Product"]
        if (len(Sub_product) == 0):
            Sub_Product_value = 0
        else:
            Sub_Product_value = 1
        
        # Submitted via
        Submitted_via = request.form["Submitted_via"]
        if Submitted_via == "Web":
            Submitted_via_Fax = 0
            Submitted_via_Phone = 0
            Submitted_via_Postal_mail = 0
            Submitted_via_Referral = 0
            Submitted_via_Web = 1
        if Submitted_via == "Referral":
            Submitted_via_Fax = 0
            Submitted_via_Phone = 0
            Submitted_via_Postal_mail = 0
            Submitted_via_Referral = 1
            Submitted_via_Web = 0
        if Submitted_via == "Phone":
            Submitted_via_Fax = 0
            Submitted_via_Phone = 1
            Submitted_via_Postal_mail = 0
            Submitted_via_Referral = 0
            Submitted_via_Web = 0
        if Submitted_via == "Postal mail":
            Submitted_via_Fax = 0
            Submitted_via_Phone = 0
            Submitted_via_Postal_mail = 1
            Submitted_via_Referral = 0
            Submitted_via_Web = 0
        if Submitted_via == "Fax":
            Submitted_via_Fax = 1
            Submitted_via_Phone = 0
            Submitted_via_Postal_mail = 0
            Submitted_via_Referral = 0
            Submitted_via_Web = 0
        if Submitted_via == "Email":
            Submitted_via_Fax = 0
            Submitted_via_Phone = 0
            Submitted_via_Postal_mail = 0
            Submitted_via_Referral = 0
            Submitted_via_Web = 0
        
        # Issue
        Issue = request.form["Issue"]
        if Issue == "Loan modification,collection,foreclosure":
            Issue_Loan_modification_collection_foreclosure = 1
            Issue_Loan_servicing_payments_escrow_account = 0
            Issue_Account_opening_closing_or_management = 0
            Issue_Deposits_and_withdrawals = 0
            Issue_Application_originator_mortgage_broker = 0
            Issue_Other = 0
            Issue_Problems_caused_by_my_funds_being_low = 0
            Issue_Billing_disputes = 0
            Issue_Settlement_process_and_costs = 0
            Issue_Making_receiving_payments_sending_money = 0
            Issue_Using_a_debit_or_ATM_card = 0
            Issue_Credit_decision_Underwriting = 0
            Issue_Closing_Cancelling_account = 0
            Issue_Identity_theft_Fraud_Embezzlement = 0
            Issue_Contd_attempts_collect_debt_not_owed = 0
        if Issue == "Loan servicing, payments, escrow account":
            Issue_Loan_modification_collection_foreclosure = 0
            Issue_Loan_servicing_payments_escrow_account = 1
            Issue_Account_opening_closing_or_management = 0
            Issue_Deposits_and_withdrawals = 0
            Issue_Application_originator_mortgage_broker = 0
            Issue_Other = 0
            Issue_Problems_caused_by_my_funds_being_low = 0
            Issue_Billing_disputes = 0
            Issue_Settlement_process_and_costs = 0
            Issue_Making_receiving_payments_sending_money = 0
            Issue_Using_a_debit_or_ATM_card = 0
            Issue_Credit_decision_Underwriting = 0
            Issue_Closing_Cancelling_account = 0
            Issue_Identity_theft_Fraud_Embezzlement = 0
            Issue_Contd_attempts_collect_debt_not_owed = 0
        if Issue == "Account opening, closing, or management":
            Issue_Loan_modification_collection_foreclosure = 0
            Issue_Loan_servicing_payments_escrow_account = 0
            Issue_Account_opening_closing_or_management = 1
            Issue_Deposits_and_withdrawals = 0
            Issue_Application_originator_mortgage_broker = 0
            Issue_Other = 0
            Issue_Problems_caused_by_my_funds_being_low = 0
            Issue_Billing_disputes = 0
            Issue_Settlement_process_and_costs = 0
            Issue_Making_receiving_payments_sending_money = 0
            Issue_Using_a_debit_or_ATM_card = 0
            Issue_Credit_decision_Underwriting = 0
            Issue_Closing_Cancelling_account = 0
            Issue_Identity_theft_Fraud_Embezzlement = 0
            Issue_Contd_attempts_collect_debt_not_owed = 0
        if Issue == "Deposits and withdrawals":
            Issue_Loan_modification_collection_foreclosure = 0
            Issue_Loan_servicing_payments_escrow_account = 0
            Issue_Account_opening_closing_or_management = 0
            Issue_Deposits_and_withdrawals = 1
            Issue_Application_originator_mortgage_broker = 0
            Issue_Other = 0
            Issue_Problems_caused_by_my_funds_being_low = 0
            Issue_Billing_disputes = 0
            Issue_Settlement_process_and_costs = 0
            Issue_Making_receiving_payments_sending_money = 0
            Issue_Using_a_debit_or_ATM_card = 0
            Issue_Credit_decision_Underwriting = 0
            Issue_Closing_Cancelling_account = 0
            Issue_Identity_theft_Fraud_Embezzlement = 0
            Issue_Contd_attempts_collect_debt_not_owed = 0
        if Issue == "Application, originator, mortgage broker":
            Issue_Loan_modification_collection_foreclosure = 0
            Issue_Loan_servicing_payments_escrow_account = 0
            Issue_Account_opening_closing_or_management = 0
            Issue_Deposits_and_withdrawals = 0
            Issue_Application_originator_mortgage_broker = 1
            Issue_Other = 0
            Issue_Problems_caused_by_my_funds_being_low = 0
            Issue_Billing_disputes = 0
            Issue_Settlement_process_and_costs = 0
            Issue_Making_receiving_payments_sending_money = 0
            Issue_Using_a_debit_or_ATM_card = 0
            Issue_Credit_decision_Underwriting = 0
            Issue_Closing_Cancelling_account = 0
            Issue_Identity_theft_Fraud_Embezzlement = 0
            Issue_Contd_attempts_collect_debt_not_owed = 0
        if Issue == "Other":
            Issue_Loan_modification_collection_foreclosure = 0
            Issue_Loan_servicing_payments_escrow_account = 0
            Issue_Account_opening_closing_or_management = 0
            Issue_Deposits_and_withdrawals = 0
            Issue_Application_originator_mortgage_broker = 0
            Issue_Other = 1
            Issue_Problems_caused_by_my_funds_being_low = 0
            Issue_Billing_disputes = 0
            Issue_Settlement_process_and_costs = 0
            Issue_Making_receiving_payments_sending_money = 0
            Issue_Using_a_debit_or_ATM_card = 0
            Issue_Credit_decision_Underwriting = 0
            Issue_Closing_Cancelling_account = 0
            Issue_Identity_theft_Fraud_Embezzlement = 0
            Issue_Contd_attempts_collect_debt_not_owed = 0
        if Issue == "Problems caused by my funds being low":
            Issue_Loan_modification_collection_foreclosure = 0
            Issue_Loan_servicing_payments_escrow_account = 0
            Issue_Account_opening_closing_or_management = 0
            Issue_Deposits_and_withdrawals = 0
            Issue_Application_originator_mortgage_broker = 0
            Issue_Other = 0
            Issue_Problems_caused_by_my_funds_being_low = 1
            Issue_Billing_disputes = 0
            Issue_Settlement_process_and_costs = 0
            Issue_Making_receiving_payments_sending_money = 0
            Issue_Using_a_debit_or_ATM_card = 0
            Issue_Credit_decision_Underwriting = 0
            Issue_Closing_Cancelling_account = 0
            Issue_Identity_theft_Fraud_Embezzlement = 0
            Issue_Contd_attempts_collect_debt_not_owed = 0
        if Issue == "Billing disputes":
            Issue_Loan_modification_collection_foreclosure = 0
            Issue_Loan_servicing_payments_escrow_account = 0
            Issue_Account_opening_closing_or_management = 0
            Issue_Deposits_and_withdrawals = 0
            Issue_Application_originator_mortgage_broker = 0
            Issue_Other = 0
            Issue_Problems_caused_by_my_funds_being_low = 0
            Issue_Billing_disputes = 1
            Issue_Settlement_process_and_costs = 0
            Issue_Making_receiving_payments_sending_money = 0
            Issue_Using_a_debit_or_ATM_card = 0
            Issue_Credit_decision_Underwriting = 0
            Issue_Closing_Cancelling_account = 0
            Issue_Identity_theft_Fraud_Embezzlement = 0
            Issue_Contd_attempts_collect_debt_not_owed = 0
        if Issue == "Settlement process and costs":
            Issue_Loan_modification_collection_foreclosure = 0
            Issue_Loan_servicing_payments_escrow_account = 0
            Issue_Account_opening_closing_or_management = 0
            Issue_Deposits_and_withdrawals = 0
            Issue_Application_originator_mortgage_broker = 0
            Issue_Other = 0
            Issue_Problems_caused_by_my_funds_being_low = 0
            Issue_Billing_disputes = 0
            Issue_Settlement_process_and_costs = 1
            Issue_Making_receiving_payments_sending_money = 0
            Issue_Using_a_debit_or_ATM_card = 0
            Issue_Credit_decision_Underwriting = 0
            Issue_Closing_Cancelling_account = 0
            Issue_Identity_theft_Fraud_Embezzlement = 0
            Issue_Contd_attempts_collect_debt_not_owed = 0
        if Issue == "Making/receiving payments, sending money":
            Issue_Loan_modification_collection_foreclosure = 0
            Issue_Loan_servicing_payments_escrow_account = 0
            Issue_Account_opening_closing_or_management = 0
            Issue_Deposits_and_withdrawals = 0
            Issue_Application_originator_mortgage_broker = 0
            Issue_Other = 0
            Issue_Problems_caused_by_my_funds_being_low = 0
            Issue_Billing_disputes = 0
            Issue_Settlement_process_and_costs = 0
            Issue_Making_receiving_payments_sending_money = 1
            Issue_Using_a_debit_or_ATM_card = 0
            Issue_Credit_decision_Underwriting = 0
            Issue_Closing_Cancelling_account = 0
            Issue_Identity_theft_Fraud_Embezzlement = 0
            Issue_Contd_attempts_collect_debt_not_owed = 0
        if Issue == "Using a debit or ATM card":
            Issue_Loan_modification_collection_foreclosure = 0
            Issue_Loan_servicing_payments_escrow_account = 0
            Issue_Account_opening_closing_or_management = 0
            Issue_Deposits_and_withdrawals = 0
            Issue_Application_originator_mortgage_broker = 0
            Issue_Other = 0
            Issue_Problems_caused_by_my_funds_being_low = 0
            Issue_Billing_disputes = 0
            Issue_Settlement_process_and_costs = 0
            Issue_Making_receiving_payments_sending_money = 0
            Issue_Using_a_debit_or_ATM_card = 1
            Issue_Credit_decision_Underwriting = 0
            Issue_Closing_Cancelling_account = 0
            Issue_Identity_theft_Fraud_Embezzlement = 0
            Issue_Contd_attempts_collect_debt_not_owed = 0
        if Issue == "Credit decision / Underwriting":
            Issue_Loan_modification_collection_foreclosure = 0
            Issue_Loan_servicing_payments_escrow_account = 0
            Issue_Account_opening_closing_or_management = 0
            Issue_Deposits_and_withdrawals = 0
            Issue_Application_originator_mortgage_broker = 0
            Issue_Other = 0
            Issue_Problems_caused_by_my_funds_being_low = 0
            Issue_Billing_disputes = 0
            Issue_Settlement_process_and_costs = 0
            Issue_Making_receiving_payments_sending_money = 0
            Issue_Using_a_debit_or_ATM_card = 0
            Issue_Credit_decision_Underwriting = 1
            Issue_Closing_Cancelling_account = 0
            Issue_Identity_theft_Fraud_Embezzlement = 0
            Issue_Contd_attempts_collect_debt_not_owed = 0    
        if Issue == "Closing/Cancelling account":
            Issue_Loan_modification_collection_foreclosure = 0
            Issue_Loan_servicing_payments_escrow_account = 0
            Issue_Account_opening_closing_or_management = 0
            Issue_Deposits_and_withdrawals = 0
            Issue_Application_originator_mortgage_broker = 0
            Issue_Other = 0
            Issue_Problems_caused_by_my_funds_being_low = 0
            Issue_Billing_disputes = 0
            Issue_Settlement_process_and_costs = 0
            Issue_Making_receiving_payments_sending_money = 0
            Issue_Using_a_debit_or_ATM_card = 0
            Issue_Credit_decision_Underwriting = 0
            Issue_Closing_Cancelling_account = 1
            Issue_Identity_theft_Fraud_Embezzlement = 0
            Issue_Contd_attempts_collect_debt_not_owed = 0
        if Issue == "Identity theft / Fraud / Embezzlement":
            Issue_Loan_modification_collection_foreclosure = 0
            Issue_Loan_servicing_payments_escrow_account = 0
            Issue_Account_opening_closing_or_management = 0
            Issue_Deposits_and_withdrawals = 0
            Issue_Application_originator_mortgage_broker = 0
            Issue_Other = 0
            Issue_Problems_caused_by_my_funds_being_low = 0
            Issue_Billing_disputes = 0
            Issue_Settlement_process_and_costs = 0
            Issue_Making_receiving_payments_sending_money = 0
            Issue_Using_a_debit_or_ATM_card = 0
            Issue_Credit_decision_Underwriting = 0
            Issue_Closing_Cancelling_account = 0
            Issue_Identity_theft_Fraud_Embezzlement = 1
            Issue_Contd_attempts_collect_debt_not_owed = 0
        if Issue == "Cont'd attempts collect debt not owed":
            Issue_Loan_modification_collection_foreclosure = 0
            Issue_Loan_servicing_payments_escrow_account = 0
            Issue_Account_opening_closing_or_management = 0
            Issue_Deposits_and_withdrawals = 0
            Issue_Application_originator_mortgage_broker = 0
            Issue_Other = 0
            Issue_Problems_caused_by_my_funds_being_low = 0
            Issue_Billing_disputes = 0
            Issue_Settlement_process_and_costs = 0
            Issue_Making_receiving_payments_sending_money = 0
            Issue_Using_a_debit_or_ATM_card = 0
            Issue_Credit_decision_Underwriting = 0
            Issue_Closing_Cancelling_account = 0
            Issue_Identity_theft_Fraud_Embezzlement = 0
            Issue_Contd_attempts_collect_debt_not_owed = 1
            
            
        # Sub Issue    
        Sub_Issue = request.form["Sub_Issue"]
        if (len(Sub_Issue) == 0):
            Sub_Issue_value = 0
        else:
            Sub_Issue_value = 1
        
        
        # Consumer complaint narrative
        Consumer_complaint_narrative = request.form["Consumer_complaint_narrative"]
        if (len(Consumer_complaint_narrative) == 0):
            Consumer_complaint_narrative_value = 0
        else:
            Consumer_complaint_narrative_value = 1
        
        
        #Company public response
        Company_public_response = request.form["Company_public_response"]
        if (len(Company_public_response) == 0):
            Company_public_response_value = 0
        else:
            Company_public_response_value = 1
        
        
        # Company response to consumer
        Company_response_to_consumer = request.form["Company_response_to_consumer"]
        if Company_response_to_consumer == "Closed with explanation":
            Company_response_to_consumer_Closed_with_explanation = 1
            Company_response_to_consumer_Closed_with_monetary_relief = 0
            Company_response_to_consumer_Closed_with_non_monetary_relief = 0
            Company_response_to_consumer_Closed_with_relief = 0
            Company_response_to_consumer_Closed_without_relief = 0
        if Company_response_to_consumer == "Closed with non-monetary relief":
            Company_response_to_consumer_Closed_with_explanation = 0
            Company_response_to_consumer_Closed_with_monetary_relief = 0
            Company_response_to_consumer_Closed_with_non_monetary_relief = 1
            Company_response_to_consumer_Closed_with_relief = 0
            Company_response_to_consumer_Closed_without_relief = 0
        if Company_response_to_consumer == "Closed with monetary relief":
            Company_response_to_consumer_Closed_with_explanation = 0
            Company_response_to_consumer_Closed_with_monetary_relief = 1
            Company_response_to_consumer_Closed_with_non_monetary_relief = 0
            Company_response_to_consumer_Closed_with_relief = 0
            Company_response_to_consumer_Closed_without_relief = 0
        if Company_response_to_consumer == "Closed without relief":
            Company_response_to_consumer_Closed_with_explanation = 0
            Company_response_to_consumer_Closed_with_monetary_relief = 0
            Company_response_to_consumer_Closed_with_non_monetary_relief = 0
            Company_response_to_consumer_Closed_with_relief = 0
            Company_response_to_consumer_Closed_without_relief = 1
        if Company_response_to_consumer == "Closed":
            Company_response_to_consumer_Closed_with_explanation = 0
            Company_response_to_consumer_Closed_with_monetary_relief = 0
            Company_response_to_consumer_Closed_with_non_monetary_relief = 0
            Company_response_to_consumer_Closed_with_relief = 0
            Company_response_to_consumer_Closed_without_relief = 0
        if Company_response_to_consumer == "Closed with relief":
            Company_response_to_consumer_Closed_with_explanation = 0
            Company_response_to_consumer_Closed_with_monetary_relief = 0
            Company_response_to_consumer_Closed_with_non_monetary_relief = 0
            Company_response_to_consumer_Closed_with_relief = 1
            Company_response_to_consumer_Closed_without_relief = 0
            
        
        # Timely response?
        Timely_response = request.form["Timely_response"]
        if Timely_response == "Yes":
            Timely_response_Yes = 1
        else:
            Timely_response_Yes = 0
         
        
        # Tags
        Tags = request.form["Tags"]
        
        
        # Consumer consent provided?
        Consumer_consent_provided = request.form["Consumer_consent_provided"]
        if (len(Company_public_response) == 0):
            Consumer_consent_provided_value = 0
        else:
            Consumer_consent_provided_value = 1
       

    #    ['State_North_East', 'State_South', 'State_West', 'Timely response?_Yes', 'Company response to consumer_Closed with explanation',
    #    'Company response to consumer_Closed with monetary relief', 'Company response to consumer_Closed with non-monetary relief',
    #    'Company response to consumer_Closed with relief', 'Company response to consumer_Closed without relief', 'Submitted via_Fax',
    #    'Submitted via_Phone', 'Submitted via_Postal mail', 'Submitted via_Referral', 'Submitted via_Web', 
    #    'Product_Credit and Prepaid Card', 'Product_Credit reporting', 'Product_Debt collection', 'Product_Loan services',
    #    'Product_Mortgage', 'Product_Other financial service', 'Consumer disputed?', 'Received Sent Date Diff', 
    #    'Date received year', 'Date received month', 'Date received weekday', 'Issue_Loan_modification_collection_foreclosure',
    #    'Issue_Loan_servicing__payments__escrow_account', 'Issue_Account_opening__closing__or_management',
    #    'Issue_Deposits_and_withdrawals', 'Issue_Application__originator__mortgage_broker', 'Issue_Other', 
    #    'Issue_Problems_caused_by_my_funds_being_low', 'Issue_Billing_disputes', 'Issue_Settlement_process_and_costs',
    #    'Issue_Making/receiving_payments__sending_money', 'Issue_Using_a_debit_or_ATM_card', 'Issue_Credit_decision_/_Underwriting',
    #    'Issue_Closing/Cancelling_account', 'Issue_Identity_theft_/_Fraud_/_Embezzlement',
    #    'Issue_Cont'd_attempts_collect_debt_not_owed', 'Sub_product', 'Sub_issue', 'Consumer_complaint_narrative'
    #    'Consumer_consent_provided']
    
        data = pd.DataFrame([[State_North_East, State_South, State_West, Timely_response_Yes, Company_response_to_consumer_Closed_with_explanation, Company_response_to_consumer_Closed_with_monetary_relief, Company_response_to_consumer_Closed_with_non_monetary_relief, Company_response_to_consumer_Closed_with_relief, Company_response_to_consumer_Closed_without_relief, Submitted_via_Fax, Submitted_via_Phone, Submitted_via_Postal_mail, Submitted_via_Referral, Submitted_via_Web, Product_Credit_and_Prepaid_Card, Product_Credit_reporting, Product_Debt_collection, Product_Loan_services, Product_Mortgage, Product_Other_financial_service, Received_Sent_Date_Diff, Date_Received_year, Date_Received_month, Date_Received_weekday, Issue_Loan_modification_collection_foreclosure, Issue_Loan_servicing_payments_escrow_account, Issue_Account_opening_closing_or_management, Issue_Deposits_and_withdrawals, Issue_Application_originator_mortgage_broker, Issue_Other, Issue_Problems_caused_by_my_funds_being_low, Issue_Billing_disputes, Issue_Settlement_process_and_costs, Issue_Making_receiving_payments_sending_money, Issue_Using_a_debit_or_ATM_card, Issue_Credit_decision_Underwriting, Issue_Closing_Cancelling_account, Issue_Identity_theft_Fraud_Embezzlement, Issue_Contd_attempts_collect_debt_not_owed, Sub_Product_value, Sub_Issue_value, Consumer_complaint_narrative_value, Consumer_consent_provided_value]], columns= ['State_North_East', 'State_South', 'State_West', 'Timely response?_Yes', 'Company response to consumer_Closed with explanation', 'Company response to consumer_Closed with monetary relief', 'Company response to consumer_Closed with non-monetary relief', 'Company response to consumer_Closed with relief', 'Company response to consumer_Closed without relief', 'Submitted via_Fax', 'Submitted via_Phone', 'Submitted via_Postal mail', 'Submitted via_Referral', 'Submitted via_Web', 'Product_Credit and Prepaid Card', 'Product_Credit reporting', 'Product_Debt collection', 'Product_Loan services', 'Product_Mortgage', 'Product_Other financial service', 'Received Sent Date Diff', 'Date received year', 'Date received month', 'Date received weekday', 'Issue_Loan_modification_collection_foreclosure', 'Issue_Loan_servicing__payments__escrow_account', 'Issue_Account_opening__closing__or_management', 'Issue_Deposits_and_withdrawals', 'Issue_Application__originator__mortgage_broker', 'Issue_Other', 'Issue_Problems_caused_by_my_funds_being_low', 'Issue_Billing_disputes', 'Issue_Settlement_process_and_costs', 'Issue_Making/receiving_payments__sending_money', 'Issue_Using_a_debit_or_ATM_card', 'Issue_Credit_decision_/_Underwriting', 'Issue_Closing/Cancelling_account', 'Issue_Identity_theft_/_Fraud_/_Embezzlement', "Issue_Cont'd_attempts_collect_debt_not_owed", 'Sub_product', 'Sub_issue', 'Consumer_complaint_narrative', 'Consumer_consent_provided'])
        
        prediction=model.predict(data)
        
        if prediction == 0:
            return render_template('home.html',prediction_text="The customer is likely not to dispute.")
        elif prediction == 1:
            return render_template('home.html',prediction_text="The customer is likely to dispute.")
        else:
            return render_template('home.html',prediction_text="The output is invalid. Check the app. The model predicted {}".format(prediction))

    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)