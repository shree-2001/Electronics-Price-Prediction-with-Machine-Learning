# 📦 Electronics Price Prediction

## 📌 Project Overview
This project aims to **predict the prices of various electronic devices**—including **laptops, mobile phones, and televisions**—using **machine learning techniques**.  
With the rapid evolution of technology and fluctuating market trends, accurate price prediction can help **consumers, retailers, and manufacturers** make informed decisions.

Our approach leverages **data-driven models** instead of relying solely on traditional expert judgment, enabling dynamic adjustments to market changes.

---

## 🛠️ Technologies Used
- **Programming Language:** Python  
- **Databases:** MongoDB, PostgreSQL 16  
- **Libraries & Tools:** Pandas, NumPy, Matplotlib, Seaborn, Plotly  
- **Development Environment:** Visual Studio Code (Windows & macOS)  

---

## 📂 Datasets
We used **three datasets** sourced from **Kaggle**:

1. **Television Dataset** – Includes product specifications, ratings, operating systems, and prices.  
2. **Laptop Dataset** – Contains details such as OS, screen resolution, weight, and price.  
3. **Mobile Dataset** – Includes RAM, ROM, battery capacity, camera quality, and price.

---

## 🔄 Project Workflow

1. **Data Collection & Storage**  
   - Extracted datasets from Kaggle (CSV format).  
   - Stored data in **MongoDB** (JSON/CSV formats).  

2. **Data Cleaning & Preprocessing**  
   - Removed missing values, duplicates, and irrelevant data.  
   - Transformed data into PostgreSQL tables for structured storage.  

3. **Exploratory Data Analysis (EDA)**  
   - Used Matplotlib, Seaborn, and Plotly for visualizations.  
   - Identified trends and correlations between specifications and prices.  

4. **Merging Datasets**  
   - Combined all datasets to analyze **cross-category trends**.  
   - Performed additional visualizations such as **battery distribution histograms** and **price variation box plots**.  

---

## 📊 Key Insights
- **RAM, ROM, and battery capacity** have a strong positive correlation with price in mobile devices.  
- **Screen size** significantly influences laptop pricing.  
- **Operating system type** impacts TV price variations.  
- Merged dataset analysis revealed **consumer preferences** for higher battery capacities and highlighted OS-based price differences.  

---

## 📈 Visualizations
- **Histograms & KDE plots** – Show distribution of features like battery capacity.  
- **Box Plots** – Price variation by operating system.  
- **Bar Charts & Pie Charts** – Ratings and brand popularity.  
- **Scatter Plots** – Relationships between specifications and price.  

---

## 📚 Conclusion
The project successfully demonstrates that **machine learning-based analysis** of specifications and ratings can provide valuable insights for:  
- **Consumers** – Finding the best value for money.  
- **Retailers** – Adjusting pricing strategies.  
- **Manufacturers** – Aligning production with market demand.  

---

## 📜 References
1. Mark D. Allendorf et al. – *Electronics Industry Research*  
2. Matt Casters et al. – *Pentaho Kettle Solutions*  
3. W.H. Inmon – *Building the Data Warehouse*  
4. Kimball & Caserta – *The Data Warehouse ETL Toolkit*  

---

## 👨‍💻 Authors
- **Ajith Gundan** – Mobile Price Analysis  
- **Jayashree Rajkumar** – Television Price Analysis  
- **Dineshkumar Lingapandiyan** – Laptop Price Analysis  
