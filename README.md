# col-tracker
Cost-of-living tracker
#### Input data
.xlsx with 5 columns date, category, item, cost, store and optional note
## Getting started
### Using docker
1. Install docker https://docs.docker.com/desktop/install/
2. Clone repo locally
3. Execute the following command in the repository folder:
    `docker compose build`
   `docker compose up -d`
4. Visit http://localhost:8501 in your browser

 ### Using python
 1. Clone repo locally
 2. pip install -r dashboard/requirements.txt
 3. streamlit run Analysis.py --server.port=8501
 4. Visit http://localhost:8501 in your browser
