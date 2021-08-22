# Scrapper-Portal da Queixa

With this scrapper I want to analyse complaints from the different companies. Using some NLP techniques it is possible to have some insights.
This project is divided in two sections:

  1. The Scrapper to save the data in a database
  2. The Streamlit App to do the analysis

## 1. Scrapper
Before start this project you should create your own SQL database. I used MySQL but feel free to use any other database.

### 1.1. Scrapper - Installation

1. BeautifulSoup
2. PyMySQL
3. Textacy

### 1.2. Run

```
$python main.py
```

Ex. - Get complaints from Ikea brand

input: ikea

### 1.3. Possible Errors

1. 403 - To many requests! 
2. some brands have a different name in the link, for example: nowo uses old name: cabovisao


## 2. Analysis -Streamlit App

### 2.1. Streamlit App - Installation

```
pip install -r requirements.txt
```

### 2.2. Run

```
streamlit run main.py
```

### 2.3. Deploy in Google Cloud Run
1. Clone project to Google Cloud and cd to folder <br>

```
cd scrapper-portadaqueixa
```

2. Change the variables from build_and_deplot.sh file and use the bash command to deploy the app.

```
bash build_and_deploy.sh
```
 
