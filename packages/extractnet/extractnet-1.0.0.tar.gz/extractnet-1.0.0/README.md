
ExtractNet
=======

Based on the popular content extraction package [Dragnet](https://github.com/dragnet-org/dragnet/), ExtractNet extend the machine learning approach to extract other attributes such as date, author and keywords from news article. 

## Why don't just use existing rule-base extraction method:

We discover some webpage doesn't provide the real author name but simply populate the author tag with a default value.

For example [ltn.com.tw](https://news.ltn.com.tw) always populate the same author value for each news article while the real author is within the content first paragraph.

```
<meta property="dable:author" content="自由時報"> <-- incorrect author name
...
<p>〔記者錢利忠／台北報導〕台北地檢署偵辦勞動基金炒股案，今發動第3波行動，兵分5路搜索證券商復華投信，約談復華投信投資長邱明強、研究員劉建賢、先前以證人請回的寶佳資產執行長唐楚烈、已獲30萬元交保的寶佳投資主管邱裕元等4人；又以唐楚烈今天被約談後，已從證人改列被告，最受矚目。</p> <-- the correct author name should be 錢利忠
```

ExtractNet use machine learning approach to extract these relevant data through visible section of the webpage just like a human.


## What ExtractNet is and isn't

* ExtractNet is a platform to extract any interesting attributes from any webpage, not just limited to content based article.

* ExtractNet aims to convert unstructured webpage to structured data without relying hand crafted rules

* ExtractNet do not convert webpage into simplified html

# Performance

Results of the initial evaluation:

We use the same body extraction benchmark from [article-extraction-benchmark](https://github.com/scrapinghub/article-extraction-benchmark) 


| Model  | Precision  | Recall  | F1  | Accuracy  |
|---|---|---|---|---|
| AutoExtract |  0.984 ± 0.003 | 0.956 ± 0.010  | 0.970 ± 0.005  | 0.470 ± 0.037   |
| Diffbot  | 0.958 ± 0.009  | 0.944 ± 0.013  | 0.951 ± 0.010  |  0.348 ± 0.035  |
| boilerpipe  | 0.850 ± 0.016  |  0.870 ± 0.020 | 0.860 ± 0.016  | 0.006 ± 0.006   |
| dragnet  |  0.925 ± 0.012 | 0.889 ± 0.018  | 0.907 ± 0.014  | 0.221 ± 0.030   |
| **ExtractNet**  | 0.922 ± 0.011  |  0.933 ± 0.013 | 0.927 ± 0.010  | 0.160 ± 0.027  |
| html-text  | 0.500 ± 0.017  | 0.994 ± 0.001  | 0.665 ± 0.015  |  0.000 ± 0.000  |
| newspaper  |  0.917 ± 0.013 | 0.906 ± 0.017  | 0.912 ± 0.014  | 0.260 ± 0.032   |
| readability  | 0.913 ± 0.014   | 0.931 ± 0.015  | 0.922 ± 0.013  | 0.315 ± 0.034   |
| trafilatura  | 0.930 ± 0.010  | 0.967 ± 0.009  | 0.948 ± 0.008   | 0.243 ± 0.031   |

## List of changes from Dragnet

* Underlying classifier is replaced by [Catboost](https://catboost.ai/) instead of [Decision Tree](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html) for all attributes extraction for consistency and performance boost.

* Updated CSS features, added text+css latent feature 

* Includes a CRF model that extract names from author block text.


## GETTING STARTED

```
git clone https://github.com/currentsapi/extractnet
cd extractnet 
python setup.py install
```

Code
```
from extractnet.extractor import CascadeExtractor
import requests
import joblib

auth_clf = joblib.load('extractnet/models/author_extractor.pkl.gz')
date_clf = joblib.load('extractnet/models/datePublishedRaw_extractor.pkl.gz')
cascade_clf = CascadeExtractor('extractnet/models/final_extractor.pkl.gz', 
                                auth_clf, date_clf)
raw_html = requests.get('https://apnews.com/article/6e58b5742b36e3de53298cf73fbfdf48').text
results = cascade_clf.extract(raw_html, encoding='utf-8', as_blocks=False, extract_target=[1], debug=False)
for key, value in results.items():
    print(key)
    print(value)
    print('------------')
```

## Installing

Coming soon

# Contributing

We love contributions! Open an issue, or fork/create a pull
request.

# More details about the code structure

Coming soon

## Evaluating content extraction models

Coming soon