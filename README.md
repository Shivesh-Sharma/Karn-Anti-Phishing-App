
# Karn Anti-Phishing App Database

This repository contains data sets of phishing and not phishing websites that are used to train and test the machine learning model for Karn Anti-Phishing App.

## Dataset Description
The dataset contains two folders:

urldata - This folder contains CSV files of various phishing URLs and their associated features. These features include the domain name, URL length, the presence of symbols, the presence of redirection, etc.

urldata1 - This folder contains CSV files of various legitimate URLs and their associated features.
Each CSV file contains two columns: URL and Label. The URL column lists the URLs, and the Label column indicates whether the URL is phishing (1) or not phishing (0).

## How to Use
To use this database, you can download the CSV files and use them to train and test your own anti-phishing machine learning model.

If you want to contribute to this dataset, you can add more phishing and not phishing URLs to the respective folders in CSV format.

## Credits
The initial dataset was collected from various sources, including online repositories and research papers. We acknowledge the contributions of the original authors in creating these datasets.

## License
This dataset is released under the MIT License. You are free to use, modify, and distribute the dataset, but we are not responsible for any consequences resulting from the use of this dataset.
