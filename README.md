# Human Development Index (HDI) Prediction System

## 🎯 Project Overview

This project implements a machine learning web application for predicting Human Development Index values based on socioeconomic indicators. The system uses Flask for the web interface and scikit-learn for machine learning predictions.

---

## ✨ Recent Improvements

### 1. **Enhanced CSS Styling** 🎨

**What's New:**
- Modern gradient backgrounds with smooth animations
- Improved hover effects with scale transitions
- Focus states for form inputs with glow effects
- Responsive design for mobile/tablet/desktop
- Smooth fade-in animations for page elements
- Professional color scheme with better contrast
- Added smooth scrolling behavior
- Enhanced navbar with underline animation effect

**Key Features:**
- `fadeIn` and `slideInDown` animations for smooth page loads
- `pulse` animation for result display
- Linear gradient buttons with hover transformations
- Glass-morphism effect (backdrop blur) for modern look
- Mobile-first responsive design (480px, 768px breakpoints)
- Better accessibility with improved contrast ratios

### 2. **Improved Code Accuracy** 🔬

#### **Backend (Flask) Improvements:**

**Input Validation:**
- Comprehensive validation for all input parameters
- Range checking for each feature:
  - Life Expectancy: 50-89 years
  - Mean Years of Schooling: 1-15 years
  - GNI per Capita: 400-140,000
  - Internet Users: 0-100%
- Detailed error messages displayed to users
- Try-catch error handling with logging

**Enhanced Classification:**
- Improved HDI thresholds based on international standards:
  - Low HDI: < 0.55
  - Medium HDI: 0.55-0.70
  - High HDI: 0.70-0.80
  - Very High HDI: ≥ 0.80
- Color-coded results with emoji indicators
- Descriptive explanations for each category
- Improved prediction precision (4 decimal places)

**Data Processing:**
- Fixed feature extraction logic
- Proper DataFrame construction with column names
- Better error handling and logging
- Support for consistent model input format

#### **Frontend (HTML) Improvements:**

**home.html:**
- Fixed CSS path (now correctly references `styles.css`)
- Added viewport meta tag for mobile responsiveness
- Better semantic HTML structure
- Improved typography and layout
- Added descriptive text about the application

**indexnew.html:**
- Proper form labels with better organization
- Input type="number" for better validation on client side
- Step attributes for reasonable increments
- Better placeholder text with examples
- Error message container for validation feedback
- Fixed navbar structure

**resultnew.html:**
- Complete navbar with navigation
- Safe rendering of HTML content (`| safe` filter)
- Better result display formatting
- Consistent styling with other pages

### 3. **Advanced Machine Learning Training Script** 🤖

**New Training Pipeline** (`Training/HumDevIndex.py`):

**Data Preprocessing:**
- Automatic loading of CSV data
- Missing value handling with median imputation
- Data exploration and summary statistics

**Feature Engineering:**
- Interaction features (life × GNI, schooling × GNI)
- Ratio features (life/schooling ratio)
- Polynomial features for non-linear relationships
- Normalized feature scaling for better model performance

**Multiple Model Training:**
1. **Linear Regression** - Baseline model
2. **Random Forest** - Ensemble method with 100 trees
3. **Gradient Boosting** - Advanced ensemble with learning rate optimization

**Model Evaluation Metrics:**
- R² Score (coefficient of determination)
- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)
- Cross-validation scores (k-fold, default k=5)

**Feature Importance Analysis:**
- Automatic analysis of which features contribute most to predictions
- Helps understand model decision-making

**Model Selection:**
- Automatically selects best model based on R² score
- Saves the best model as `HDI.pkl`

---

## 📁 Project Structure

```
project/
├── DataSet/
│   └── Human Development Index and Components.csv
├── Flask/
│   ├── app.py                    # Main Flask application
│   ├── d/
│   │   └── styles.css           # Enhanced CSS styling
│   └── templates/
│       ├── home.html            # Home page
│       ├── indexnew.html        # Prediction form
│       └── resultnew.html       # Results display
└── Training/
    └── HumDevIndex.py           # ML training pipeline
```

---

## 🚀 Usage Guide

### 1. **Install Dependencies**

```bash
pip install flask scikit-learn pandas numpy
```

### 2. **Train the Model**

```bash
cd Training
python HumDevIndex.py
```

This will:
- Load the CSV data
- Perform feature engineering
- Train multiple models
- Display accuracy metrics
- Save the best model as `HDI.pkl`

### 3. **Run the Flask Application**

```bash
cd Flask
python app.py
```

The application will start at `http://localhost:5000`

### 4. **Using the Web Interface**

1. **Home Page**: Overview of the HDI prediction system
2. **Predict Page**: Fill in the form with:
   - Country (select from dropdown)
   - Life Expectancy (50-89 years)
   - Mean Years of Schooling (1-15)
   - GNI per Capita (400-140,000)
   - Internet Users (0-100%)
3. **Results**: View the predicted HDI value with classification

---

### 🚀 Deployed Link 
🔗 [predict-human-development-index.vercel.app](https://predict-human-development-index.vercel.app/) 
