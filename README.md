# Text-Classification-using-BERT
Masters of Quantitative Economics at University of Pittsburgh, capstone project


This project is using machine learning methods to create work order tickets to address banking complaints so that our client, PNC can address customer problems effeciecently. 

## Demo User Interface
https://replit.com/@ShivMakh1/PNC-Text-Classification

Go to this website and click run. It may take a minute to load. Please by patient. 
You will be able to submit your complaint, and if you go to the files tab. There are two CSV files that shows that the complaints and the department assoicated are stored. This can be extrapolated to use Databases, or into subsequent projects as well.

## Use Case

Everyone uses products that at some point that doesn't work as desired. What do you do when your product doesnt work? Toss it, buy another, or call customer service. There are two perspectives to calling customer service to address a complaint. The company side and the customer side. For a company to address a complaint, they need a work order ticket that two main components, the complaint and the department that can address the complaint. The other side of this is the consumer perspective. Calling customer service to fix the problem is incredibly fustrating. You first spend 10 minutes on hold, and then have to transfer 5 more times trying to explain the probelm. Next thing you know, its been two hours, and no one has actually created the work order ticket. 

PNC wants to make this process easier for their customers. 

## Data Cleaning
Preparing a text classification model has 2 main steps, preparing the data, then training the model on the data. To get the best results from training, certain steps are taken with pre-processsing the data. The data used was the national complaints database for financial institutions. The first step was removing repeat and null observations; after starting with around 2 million data points, this left us with about 500,000. Each observation had the textual complaint as well as what department it belonged to. To improve model accuracy, punctuation was removed, all letters were put in lowercase, special characters and symbols were removed, and redacted information replaced with 'XXXX...' were removed. These changes help due to fundamental properties of BERT.

## Model Training
For this project, we used BERT natural language processing (NLP). BERT is pretrained on large datasets of text, and this pretraining can be done in a variety of ways. With a small sacrifice to accuracy and a large save on time, we used distilBERT to train our model. DistilBERT has already been pretrained and understands text, so we  fine tuned its capabilities on our dataset so it could correctly identify what department complaints should be sent to. We trained the model multiple times, with minor tweaks to achieve the highest f1 score, with our final model achieving a score of 88.

#GUI
