## Discrimination_Prediction

# Project Discription
Collect racial discrimination-related event instances with [Google News API](https://newsapi.org/s/google-news-api) to predict casualty and location of future possible discrimanation-related events. We make a visualization model of past events and forecast predictions.

# Authors
- Soohyuck Cho
- Yoonjae Hwang
- Jongwoo Jeon
- Jihoon Kang
- Eunsun Lee
- Jinpyo Lee

# Project Structure
- Front-end, Back-end: Javascipt with React
- Data Organization / Extraction / Classification :  
    * Filter with keywords in US news 
    * Extract data based with date, number of casualties, and city/state
- Deep Learning:
    * Implemented [PyTorch](https://pytorch.org) to create [Gated Recurrent Unit](https://arxiv.org/pdf/1412.3555.pdf?ref=hackernoon.com) model that predicts the state where future discrimination is most likely to occur.