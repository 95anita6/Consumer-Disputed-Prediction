# Consumer-Disputed-Prediction
Consumer complaints resolution, feedback and satisfaction is highly important to any business. This project aims to predict if the consumer disputed with the resolution given the complaint details. If the company can identify these customers, who are likely to dispute a conclusion can be given more attention as to how weel the complaints can be handeled as well as how persuasively the resolutions can convey them. This helps the company to retain the existing custmers as well as increase their customers.

# Data Collection:
The dataset was part of project from a course.

# Data Exploration and analysis:
The given dataset has more than 4 lakh observations for customers from different banks across US. The given data set has below features:

 - Date received : When was the complaint registered.
 - Product : For which product did the customer file the complaint
 - Sub-product : For which sub-product was the issue related to
 - Issue : In which category the issue falls in
 - Sub-issue : In wchich category the sub-issue falls in
 - Consumer complaint narrative : The narrative given by the consumer for the complaint
 - Company : For which company was the issue related to
 - State : Geographical information of the customer
 - ZIP code : Zip Code for the state
 - Tags : Under what category the customer falls in Older 'American', 'Older American, Servicemember' or 'Servicemember'
 - Consumer consent provided? - Consumer consent was provided or not
 - Submitted via : How did the consumer submit the complaint
 - Date sent to company : Date when the complaint was sent to the comapny
 - Company response to consumer : The response from company in order to resolve the issue
 - Timely response? : Was timely response given
 - Consumer disputed? : Target variable
 - Complaint ID : The Complaint ID

The companies that had most number of complaints were : Bank of America, Wells Fargo & Company, JPMorgan Chase & Co.

An analysis done on the issues and the narratives provided by the consumer using worcloud indicates that ost of the issues are related to the Loan modification, collection, foreclosure, Incorrect information on credit report, Loan servicing, payments etc. The ferequently used words in the complaints are payment, account, loan.

The highest number of complaints were registered for Mortgage, Debt collection and Credit reporting products and were submitted via web.

In most of the cases, the company did not choose to provide any public response or responsed that they have acted appropriately and would not like to provide any public response. Most of the issue were closed with explanation or non-monetary relief or monetary relief from the company's end. 

Given the company response to consumer, the customer disputed in the case where the complaint was closed with either non-monetary relief or with some explanation indicating that the customer was not satisfied with the explanation. The customers disputed most for products Mortgage, Debt collection and Credit reporting given the response from the company among which most of the complaints had timely response from the company.

The analysis on the given dataset was also performed using Tableau. Please find the link for Customer Complaint Analysis Dashboard : 

# Feature Engineering, Feature Selection and Model Building:
For model building purpose the data for Bank of America was considered.

The given dataset was split into train and test using train_test_split in 80:20 ratio.

The columns ZIP code, Complaint ID and Company were dropped. Date received and Date sent to company were converted to datetime and the difference between the dates was calculated. Year, month and weekday was extracted from the received date. The original date receievd and sent columns were dropped then. The different product catgorical values were clubbed together like student loan, consumer loan and payday loan were taken together under loan categorical value to reduce the feature size. Top 15 issues were taken into considertaion for model building. The column company public response was dropped as this feature had lot of null values and updating them with the mode value would mean that almost for every complaint there was no public response which does not provide any significant information. There were few null values in the state column which were dropped. Using this column the states were divided into four categories : North East, South, Mid West and West giving information about the which region is the customer from. The categorical features Product, Submitted via, Company response to consumer, Timely response and state were used to create dummies in order to provide inputs to the training model. The columns Sub-product, Sub-issue, Consumer Complaint narrative, Tags and Consumer consent provided had lot of null values. They were feature engineered to have 0 in place of a null value and 1 if not null.

The target variable was enoded with 0 and 1 in place of No and Yes.

StandarScaler from sklearn was used for standardization.

In the first training attempt, different models were trained and hyper parameter tuned with cyclic features extracted from month and week day to depict their cyclic nature and categorical embeddings created ffrom state column. In the second attempt, TFIDF vectorizer was used in the issues column and performed training and hyper paratmeter tunning on different models. Then the final model traings and hyper parameter tunning was performed using the above feature engineering. XGB model performed better than Logistic Regression, Decision Trees, Random Forest Classifier. The accuracy score on the validation dataset was obtained as 0.61. The accuracy score of the test dataset was increased from 0.51 to 0.63.

# Application:
The XGB model was saved as pickle file to be used in the application for prediction. The application allows the user to enter the complaint details and predicts if the consumer is likely to dispute or not. The application was deployed in Microsoft Azure.

