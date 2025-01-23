# Unit Asset Trading Model

n assets: 1
risk: unhedged
---

## Model Construction

### 1. Data Model
#### Design $X_{t}$.

#### 1. Asset Properties 
- Asset Price: $S_t$
- Log Return: $\ln(S_t)$
- Volatility: $\left|d\ln(S_t)\right|$
- Trade count: $\eta_t$
- Volume: $Vol_t$

#### 2. Technical Indicators
- RSI: $RSI_t = 100 - \frac{100}{1+RS_t}$; where $RS_t = \frac{\text{avg gain over }[t-\tau, t]}{\text{avg loss over }[t-\tau, t]}$
- Stochastic Oscilator: $SO_t = \frac{S_t - L_{t-\tau}}{H_{t-\tau} - L_{t-\tau}}\times100$
- R William : $RW_t = \frac{H_{t-\tau} - S_t}{H_{t-\tau} - L_{t-\tau}}\times-100$
- MACD: $MACD_t = EMA_{t-\tau_1}(S_t) - EMA_{t-\tau_2}(S_t)$; $SL = EMA_{t-\tau_3}(MACD_t)$
- PROC: $PRCO_t = \frac{C_{t} - C_{t-n}}{C_{t-n}}$
- OBV: $OBV_t =
\begin{cases} 
OBV_{t - 1} + Vol_t & \text{if } C_t > C_{t - 1}, \\ 
OBV_{t - 1} - Vol_t & \text{if } C_t < C_{t - 1}, \\ 
OBV_{t - 1} & \text{if } C_t = C_{t - 1}.
\end{cases}$

#### Depenedent $y_{t+1}$
- Direction: $y_{t+1} = \text{sign}(S_{t+1} - S_{t})$

### 3. Feature Inspection & Extraction
<!-- [TODO: Provide a strong rationale to why this matters for the RF model] -->
- test for linear seprability: Hull Convex test
- test for autocorrelation
- test for (homo/hetero)skedacity
- Explore covaraince between *design* and *dependent* variables and between *design* variables
- Chi-sq test for feature elimination

### 4. Ensemble Learning
### Random Forest Classifier
#### Quality Metrics:
Decision Tree
- Gini impurity: node split quality
- Shannon Entropy: node split quality w.r.t unpredictablity
- Information Gain: gain in information due node split
Forest
- Strength = $\mathbb{E}_{x,y}[\text{margin}_{RF}(x,y)]$

#### Error Metrics:
- Out-of-bag error

#### Performance Metrics:
- Accuracy
- Bias vs Variance (trade off)
- Precison, Recall and F1 Score
- Reciver Operator Curve

### 5. Trading Asset
- use to Chebyshev’s inequality to optimise trade conditions (i.e optimise when likilihood is high)

Reference: https://arxiv.org/pdf/1605.00003