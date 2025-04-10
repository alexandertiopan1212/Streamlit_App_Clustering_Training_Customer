
# 🚢 TRAINCLUST – Clustering Training Customers (POLTEKPEL Banten)

TRAINCLUST is an interactive Streamlit-based application built to cluster training participants (cadets and alumni) of POLTEKPEL Banten using Age, Recency, Frequency, and Monetary (ARFM) features.

This app offers interactive visualizations, automated preprocessing, and clustering analysis using both **K-Means** and **K-Medoids** algorithms — all within an intuitive Google Sheets-like interface.

## 📊 Key Features

- **Automated Data Processing**: Converts raw Excel training data into structured ARFM format.
- **Time-based Analysis**:
  - Daily cadet/alumni attendance charts.
  - Monthly revenue bar charts.
  - Average cost per participant.
- **ARFM Calculation**:
  - Automatically derives Age, Recency, Frequency, and Monetary values from transaction data.
- **Clustering Algorithms**:
  - Choose between KMeans or KMedoids (custom implemented from scratch).
  - Visualize clusters with histograms for each feature.
- **Evaluation Metrics**:
  - Compute and visualize Davies-Bouldin Score to assess cluster quality.

## 📁 File Structure

```
.
├── main.py                # Streamlit app interface
├── data_mentah_taruna_dan_alumni.xlsx  # Sample dataset
├── requirements.txt       # Python dependencies
└── README.md              # You are here!
```

## ▶️ How to Run Locally

```bash
git clone https://github.com/alexandertiopan1212/Streamlit_App_Clustering_Training_Customer.git
cd Streamlit_App_Clustering_Training_Customer
pip install -r requirements.txt
streamlit run main.py
```

## 🖼️ Screenshots

(Space for inserting screenshots of clustering visualizations and ARFM charts)

## 📌 Use Cases

- Segmenting training program participants for targeted campaigns
- Understanding alumni spending behavior
- Identifying loyal vs inactive cadets based on frequency and recency

## 🛡 License

This project is open-source and available under the MIT License.
