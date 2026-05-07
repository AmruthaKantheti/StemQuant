# StemQuant 🧬
### A Pan-Cancer Web Application for Tumor Stemness Quantification and Clinical Outcome Prediction

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![R](https://img.shields.io/badge/R-4.0+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## Overview
StemQuant is a computational tool and web application that quantifies 
tumor stemness across multiple cancer types using transcriptomic data 
from TCGA and GEO databases. It integrates statistical analysis, 
machine learning-based prediction, and an interactive web interface 
for clinical outcome prediction.

Developed as part of MSc Bioinformatics research at Pondicherry University.

## Cancer Types Analyzed
| Cancer | TCGA Code | Analysis Performed |
|--------|-----------|-------------------|
| Glioblastoma | GBM | Stemness scoring + Survival analysis |
| Low-Grade Glioma | LGG | Stemness scoring + Survival + Biological validation |
| Liver Cancer | LIHC | Stemness scoring + Survival analysis |
| Pan-Cancer | Multiple | ML model + Prediction + Pathway enrichment |

## Features
- 🧬 RNA-seq based tumor stemness score quantification
- 📊 Kaplan-Meier survival analysis and Cox regression
- 🔬 Biological validation of stemness signatures
- 🧪 Differential stemness gene identification
- 🛤️ Pathway enrichment analysis (GO/KEGG)
- 🤖 Pan-cancer machine learning prediction model
- 🖥️ Interactive web interface with login, dashboard, prediction and history
- 📁 Multi-cancer transcriptomic data integration (TCGA)

## Project Structure

├── app.py                    # Main application entry point
├── config.py                 # Configuration settings
├── preview.py                # Preview module
├── requirements.txt          # Python dependencies
├── scripts_R/                # R analysis pipeline
│   ├── 01_GEO_Stemness_Signature.R
│   ├── 02_TCGA_Download_Preprocess.R
│   ├── 03_GBM_Survival_Analysis.R
│   ├── 03_LGG_Survival_Analysis.R
│   ├── 04_LGG_Biological_Validation.R
│   ├── 05_LGG_Differential_Stemness_Genes.R
│   ├── 06_Pathway_Enrichment_Analysis.R
│   ├── 07_LIHC_Analysis.R
│   ├── 08_Multi_Cancer_Analysis.R
│   ├── 09_PanCancer_Model_Data_Export.R
│   └── 11_Model_Biological_Validation.R
├── scripts_python/           # Python ML pipeline
│   ├── 10_PanCancer_ML_Model.py
│   ├── train_marker_model.py
│   ├── predict.py
│   └── make_test_samples.py
├── modules/                  # Web application pages
│   ├── dashboard.py
│   ├── prediction.py
│   ├── login.py
│   ├── register.py
│   ├── history.py
│   └── about.py
├── utils/                    # Utility modules
│   ├── auth.py
│   ├── db.py
│   ├── predictor.py
│   └── styling.py
├── model/                    # Trained ML models
├── assets/                   # UI assets
└── figures/                  # Output visualizations

## Tech Stack
- **Language:** Python 3.8+, R 4.0+
- **Web Framework:** Streamlit
- **ML Libraries:** scikit-learn, pandas, numpy
- **R Packages:** DESeq2, survival, clusterProfiler, TCGAbiolinks, ggplot2, Bioconductor
- **Database:** SQLite
- **Data Sources:** TCGA (GBM, LGG, LIHC — HiSeqV2), GEO

## How to Run
```bash
# Clone the repository
git clone https://github.com/AmruthaKantheti/StemQuant.git
cd StemQuant

# Install Python dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## Data Sources
- **TCGA** — The Cancer Genome Atlas (GBM, LGG, LIHC HiSeqV2 datasets)
- **GEO** — Gene Expression Omnibus (ESC stemness signature)

## Results
- Stemness scores successfully quantified across GBM, LGG and LIHC
- Significant correlation between stemness scores and patient survival outcomes
- Pan-cancer ML model trained and validated across multiple cancer types
- Pathway enrichment analysis revealed key biological processes linked to tumor stemness

## Developer
**Kantheti Amrutha**
MSc Bioinformatics, Pondicherry University

📧 amruthakantheti3@gmail.com
📞 7032732545
🔗 [LinkedIn](https://linkedin.com/in/kantheti-amrutha-753221318)
💻 [GitHub](https://github.com/AmruthaKantheti)

## License
This project is licensed under the MIT License.
