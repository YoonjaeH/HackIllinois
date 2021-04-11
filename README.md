# Discrimination_Prediction

## Motivation
With the emergence of the [novel coronavirus](https://www.who.int/csr/don/31-december-2020-sars-cov2-variants/en/), our society has witnessed soar in racial discrimination and hate crime since last year. Despite the governmental authority's continued effort to enforce [the Fourteenth Amendment](https://constitutioncenter.org/interactive-constitution/amendment/amendment-xiv), the law enforcement force is often inefficiently distributed and thus its efficiency in hate crime prevention is diminished. Thus, we propose a model to predict occurences of hate crimes to contribute to the efficient prevention of the hate crimes.

## Project Description
We first collect racial discrimination-related event instances with [New York Times API](https://developer.nytimes.com), especially the date, location and the respective occurences of the crimes. Based on the data collected, we train a deep learning model to predict occurences and locations of future possible discrimanation-related events. Our interactive dashboard enable users to instinctively compare the predicted number of crimes and the actual occurences.

## Authors
- Soohyuck Cho
- Yoonjae Hwang
- Jongwoo Jeon
- Jihoon Kang
- Eunsun Lee
- Jinpyo Lee

## Technology and Skills
- Front-end, Back-end: Javascipt with [React](https://reactjs.org)
- Data Organization / Extraction / Classification :  
    * Articles filtering based on keywords
        - Collected press agencies: [New York Times](https://www.nytimes.com), [AP](https://apnews.com), [Reuters](https://www.reuters.com)
    * Extract Article data including publish date and incident location
- Deep Learning:
    * Implemented [PyTorch](https://pytorch.org) to create [Gated Recurrent Unit](https://arxiv.org/pdf/1412.3555.pdf?ref=hackernoon.com) model that predicts the number of hate crime occurences in each states.