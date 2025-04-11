Model Evaluation and Deployment: Handling Imbalanced Datasets

**Level-Intermediate**

### **Overview**

Imbalanced datasets are prevalent in real-world machine learning
problems, where one class significantly outnumbers others. Examples
include fraud detection, rare disease diagnosis, and anomaly detection.
When training models on imbalanced datasets, the algorithms often
prioritize the majority class, leading to biased models with poor
predictive performance for the minority class. Addressing this issue
involves understanding the nature of imbalance, employing specific
preprocessing techniques, using appropriate evaluation metrics, and
deploying robust models that can handle imbalance during inference.

### **Learning Objectives**

By the end of this module, you will be able to:

-   Define imbalanced datasets and understand the challenges they
    present.

-   Explore techniques to preprocess and balance datasets effectively.

-   Apply evaluation metrics that provide meaningful insights for
    imbalanced datasets.

-   Implement strategies for handling imbalance in real-world deployment
    scenarios.

### **Prerequisites**

To fully engage with this material, you should have:

-   Familiarity with classification problems and evaluation metrics like
    precision, recall, and F1-score.

-   Basic knowledge of Python programming and machine learning libraries
    (e.g., Scikit-learn, Imbalanced-learn).

-   An understanding of data preprocessing techniques.

### **Key Concepts**

#### **1. Understanding Imbalanced Datasets**

**Definition**:

An imbalanced dataset has unequal representation of classes, where one
or more classes (the majority class) dominate while others (the minority
class) are underrepresented.

**Common Examples**:

-   Fraud detection: Legitimate transactions outnumber fraudulent ones.

-   Medical diagnosis: Positive cases for rare diseases are much fewer
    than negative cases.

-   Churn prediction: Most customers do not churn, leading to a dominant
    majority class.

**Challenges with Imbalanced Datasets**:

1.  **Biased Predictions**:

    a.  Models trained on imbalanced data tend to favor the majority
        class, leading to poor predictive performance for the minority
        class.

    b.  Example: A model predicting 99% of transactions as legitimate
        could still achieve high accuracy but fail to detect fraud
        effectively.

2.  **Misleading Metrics**:

    a.  Accuracy alone may not reflect the true performance of the model
        on minority classes.

    b.  Example: In a dataset with 95% majority class and 5% minority
        class, a model predicting all samples as the majority class
        would achieve 95% accuracy but have 0% recall for the minority
        class.

3.  **Limited Data for Minority Classes**:

    a.  Fewer training samples for the minority class make it harder for
        the model to learn meaningful patterns.

#### **2. Causes of Imbalance**

**Natural Occurrence**:

-   Certain phenomena are inherently rare (e.g., diseases, equipment
    failures).

**Data Collection Bias**:

-   Sampling processes might underrepresent certain groups (e.g.,
    socio-economic data).

**Design Constraints**:

-   Operational focus on majority cases might limit minority data
    collection (e.g., fraud detection systems optimized for speed).

#### **3. Strategies for Handling Imbalanced Datasets**

**1. Resampling Techniques**

**Oversampling the Minority Class**:

-   **Random Oversampling**: Duplicates existing minority class samples
    to increase their representation.

python

Copy code

from imblearn.over_sampling import RandomOverSampler\
ros = RandomOverSampler()\
X_resampled, y_resampled = ros.fit_resample(X, y)

-   **Synthetic Minority Oversampling Technique (SMOTE)**:

Generates synthetic samples by interpolating between existing minority
class samples.

python

Copy code

from imblearn.over_sampling import SMOTE\
smote = SMOTE()\
X_resampled, y_resampled = smote.fit_resample(X, y)

**Undersampling the Majority Class**:

-   Reduces the number of samples in the majority class to balance the
    dataset.

python

Copy code

from imblearn.under_sampling import RandomUnderSampler\
rus = RandomUnderSampler()\
X_resampled, y_resampled = rus.fit_resample(X, y)

**Combination Sampling**:

-   Balances the dataset by combining oversampling and undersampling
    techniques.

**Limitations of Resampling**:

-   Oversampling can lead to overfitting on the minority class.

-   Undersampling may discard valuable information from the majority
    class.

**2. Cost-Sensitive Learning**

-   Modify algorithms to penalize misclassifications of the minority
    class more heavily.

    -   *Weighted Loss Functions*: Assign higher weights to minority
        class errors.

    -   Example: Using Scikit-learn\'s class_weight=\'balanced\' to
        automatically compute weights.

python

Copy code

from sklearn.ensemble import RandomForestClassifier\
model = RandomForestClassifier(class_weight=\'balanced\')\
model.fit(X_train, y_train)

-   Custom weights can also be specified based on the class imbalance
    ratio.

python

Copy code

weights = {0: 1, 1: 10} \# Assigning higher weight to the minority
class\
model = RandomForestClassifier(class_weight=weights)\
model.fit(X_train, y_train)

**3. Advanced Sampling Techniques**

**ADASYN (Adaptive Synthetic Sampling)**:

-   An improvement over SMOTE that focuses on generating synthetic
    samples for harder-to-classify instances.

**Borderline-SMOTE**:

-   Focuses on generating synthetic samples near decision boundaries to
    improve classification.

**4. Choosing Appropriate Metrics**

-   Use metrics that account for class imbalance and focus on the
    performance of the minority class.

    -   **Precision**: Percentage of true positive predictions out of
        all positive predictions.

    -   **Recall (Sensitivity)**: Percentage of true positives detected
        out of all actual positives.

    -   **F1-Score**: Harmonic mean of precision and recall, balancing
        both metrics.

    -   **ROC-AUC**: Measures the trade-off between true positive rate
        and false positive rate.

python

Copy code

from sklearn.metrics import roc_auc_score\
print(roc_auc_score(y_test, y_pred_proba))

-   **Confusion Matrix**: Provides a detailed breakdown of true
    positives, true negatives, false positives, and false negatives.

python

Copy code

from sklearn.metrics import confusion_matrix\
print(confusion_matrix(y_test, y_pred))

#### **4. Handling Imbalanced Data During Deployment**

**Real-Time Considerations**:

-   Monitor incoming data streams for class imbalance during inference.

**Threshold Adjustment**:

-   Optimize the classification threshold to balance precision and
    recall.

python

Copy code

from sklearn.metrics import precision_recall_curve\
precision, recall, thresholds = precision_recall_curve(y_test,
y_pred_proba)

**Continuous Retraining**:

-   Periodically retrain models with updated data to reflect real-world
    changes.

**Integrated Pipelines**:

-   Incorporate resampling, cost-sensitive learning, and evaluation into
    deployment pipelines.

### **Hands-On Practice**

1.  **Exercise 1 (Easy)**: Visualize the class distribution in an
    imbalanced dataset.

python

Copy code

import matplotlib.pyplot as plt\
df\[\'target\'\].value_counts().plot(kind=\'bar\', title=\"Class
Distribution\")\
plt.show()

2.  **Exercise 2 (Moderate)**: Apply SMOTE to balance a dataset and
    train a classifier.

python

Copy code

from imblearn.over_sampling import SMOTE\
from sklearn.ensemble import RandomForestClassifier\
\
smote = SMOTE()\
X_resampled, y_resampled = smote.fit_resample(X, y)\
model = RandomForestClassifier()\
model.fit(X_resampled, y_resampled)

3.  **Exercise 3 (Challenging)**: Implement a cost-sensitive logistic
    regression model and evaluate performance.

python

Copy code

from sklearn.linear_model import LogisticRegression\
from sklearn.metrics import classification_report\
\
model = LogisticRegression(class_weight=\'balanced\')\
model.fit(X_train, y_train)\
predictions = model.predict(X_test)\
print(classification_report(y_test, predictions))

4.  **Exercise 4 (Challenging)**: Combine SMOTE with threshold
    optimization to improve recall.

### **Quiz: Test Your Understanding**

1.  **Which technique generates synthetic samples for the minority
    class?**

    a.  a\) Undersampling

    b.  b\) SMOTE

    c.  c\) Cost-sensitive learning

    d.  d\) ADASYN

2.  **True or False**: Accuracy is a reliable metric for imbalanced
    datasets.

3.  **What does the F1-Score measure?**

    a.  a\) Trade-off between sensitivity and specificity

    b.  b\) Average precision and recall

    c.  c\) Harmonic mean of precision and recall

    d.  d\) Overall accuracy

4.  **Which of the following handles class imbalance during training by
    weighting errors?**

    a.  a\) Resampling

    b.  b\) Cost-sensitive learning

    c.  c\) Threshold optimization

    d.  d\) Data augmentation

### **Quiz Answers**

1.  **b) SMOTE**

2.  **False**

3.  **c) Harmonic mean of precision and recall**

4.  **b) Cost-sensitive learning**

### **Additional Learning Paths**

-   **Ensemble Techniques for Imbalance**: Study bagging, boosting, and
    hybrid approaches for imbalanced datasets.

-   
