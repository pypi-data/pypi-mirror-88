quikml
==============================

Built on top of sklearn and keras, the quikml library is used to easily train, test, visualize, and assess the performance of your machine learning classification models. Whether you are beginner or advanced, this module will let you do more without the coding hassle of other machine learning modules.

With this module, you will be able to do all classical machine learning assessments with ease.

Project Organization
------------
    ├── cross_validation
    │   └── cross_validation <- contains functions for easy model cross-validation
    ├── models
    │   └── models        <- contains model types that you can train and presents code for assessing models
    ├── transformers
    │   └── transformers  <- contains transformers for text data
    └──

Current Models Supported
------------
Multilayer Perceptron, Multinomial Naive Bayes, Logistic Regression, Random Forest Classifer, XGBoost, Gradient Boosting Classifier, Histogram-based Gradient Boosting Classifier, Support Vector Classifier as well as Blending, Stacking

Transformers Supported
------------
Bag of Words, Latent Semantic Indexing, TFIDF, Latent Dirichlet Allocation

Assessment Tools Supported
------------
calibration curve, precision, recall, model loss, ROC AUC curves, Probability Distributions, 2-Dimensional PCA Assessment

--------

HOW TO USE - Basic Use
--------

### pip installation
```
pip install quikml
```

### basic import
```python
from quikml.models import LR, MLP, RFC
from quikml.transformers import BagOfWords, TFIDF, LSI
from quikml.cross_validation import downsample, cross_validation
```

### basic transformer use
```python
transformer = BagOfWords(bow_params)
transformer.fit(X_train)
X_vectorized_train = transformer.transform(X_train)
X_vectorized_test  = transformer.transform(X_test)
```

### basic model use
```python
rfc = RFC(classification_threshold=0.40)
rfc.train(X_vectorized_train, y_train, rf_params) ## or rfc.grid_search_train(X_vectorized_train, y_train, rf_params, scorer='precision')
rfc.performance_metrics(X_vectorized_test, y_test) 
rfc.visualize(X_vectorized_test, np.array(y_test).reshape(-1)) 
```

### basic cross validation use
```python
cross_validation(X, y, 
                model=RFC(classification_threshold = 0.5), 
                model_params=rf_params, 
                transformer=LSI(lsi_params), 
                fold=5)
```

