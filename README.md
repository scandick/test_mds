Архитектура 1.0

```shell
project/
├─ data/
│ ├─ raw/ # сырые данные
│ ├─ interim/ # промежуточные
│ └─ processed/ # фичи/датасеты для train
├─ notebooks/
│ ├─ 01_eda.ipynb
│ ├─ 02_feature_ideas.ipynb
│ └─ 03_model_experiments.ipynb
├─ src/
│ ├─ config.py
│ ├─ data/
│ │  ├─ load_data.py
│ │  └─ validate_data.py
│ ├─ features/
│ │  └─ build_features.py
│ ├─ models/
│ │  ├─ train.py
│ │  ├─ predict.py
│ │  └─ evaluate.py
│ ├─ pipelines/
│ │  ├─ train_pipeline.py
│ │  └─ batch_predict_pipeline.py
│ └─ api/
│ └─ main.py # FastAPI
├─ app/
│ └─ streamlit_app.py
├─ sql/
│ ├─ schema.sql
│ ├─ marts.sql
│ └─ kpi_queries.sql
├─ artifacts/
│ ├─ model.pkl
│ └─ metrics.json
├─ tests/
│ ├─ test_features.py
│ ├─ test_train.py
│ └─ test_api.py
├─ airflow/
│ └─ dags/
│ └─ ml_pipeline_dag.py
├─ docker/
│ ├─ Dockerfile.api
│ └─ Dockerfile.streamlit
├─ docker-compose.yml
├─ requirements.txt
└─ README.md
```