# English version 🇱🇷 - [(Go to Brazilian version 🇧🇷)](https://github.com/GuiCintra27/anti-fraud/blob/main/readme-pt.md)

<div align="center">
  <img src="./banner.png" width="90%"/>
  <br/>
  <br/>
  <a href="https://docs.google.com/spreadsheets/d/16Jc8QNSbyZGZLPcl4qIiG32g1b6XNB1tnHzivA0zNcw/edit?usp=sharing" target=”_blank”><strong>SpreadSheet Link »</strong></a>
  <br/>
  <br/>
</div>
<div align="center">
  <a href="#presentation">Presentation</a> •
  <a href="#about">About</a> •
  <a href="#technologies">Technologies</a> •
  <a href="#run">How to run?</a>
</div>

## <span id="presentation">Presentation Video</span>

[Click here](https://www.canva.com/design/DAGAhaA6DBo/K9HKVKbYnA7qgY4CCg8B3Q/view?utm_content=DAGAhaA6DBo&utm_campaign=designshare&utm_medium=link&utm_source=editor)

## <span id="about">🌐 About the project</span>

This project aims to build anti-fraud software. The data is obtained from a csv file (data.csv), which contains the data displayed in the [following spreadsheet](https://gist.github.com/cloudwalk-tests/76993838e65d7e0f988f40f1b1909c97#file-transactional-sample-csv).

The data obtained is being considered as an analysis of a previous day, for example, instead of a real-time analysis of the purchase, given that it is already known that chargebacks are fraud.

For this project, the knowledge obtained in the previous questions was used to create a score-based anti-fraud tool.

The results are located [in this spreadsheet](https://docs.google.com/spreadsheets/d/1CM6NSg6NEwNbMz39hOothevtAs1B9aM9W5-CfDMAupc/edit?usp=sharing).

## <span id="technologies">🛠 Technologies</span>

Below are the technologies used in the project: <br/>

<div style="display: inline_block"> 
  <img alt="Google cloud" height="30" src="https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white">
  <img alt="Google Sheets" height="30" src="https://img.shields.io/badge/Google%20Sheets-34A853?style=for-the-badge&logo=google-sheets&logoColor=white">
  <img alt="Python" height="30" src="https://img.shields.io/badge/Python-0b0b0b?style=for-the-badge&logo=python&logoColor=blue">
</div>

## <span id="run">⚙️ How to run</span>

1. Clone this repository (make sure you have python installed on your machine)

2. Install the project libraries ([library documentation](https://developers.google.com/sheets/api/quickstart/python))

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

3. Run the application with

```bash
python3 main.py
```

4. Connect to the registered email (informed in the project delivery email)

5. Done! Analyze data from all users in an easy way, in the data spreadsheet. Analyze suspicious user and card activity in their respective spreadsheets
