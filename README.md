# Dockerized Airflow Stock Pipeline (GOOGL)

This project fetches live stock market data (GOOGL) using AlphaVantage API, loads it into PostgreSQL, and schedules tasks via Apache Airflow.

---

#  How to Run

## Install Docker Desktop
https://www.docker.com/products/docker-desktop

## Generate a Fernet Key (required by Airflow)

Run this command:

```
docker run --rm python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Copy the output.

## Get Alpha Vantage API Key
Sign up free:  
https://www.alphavantage.co/support/#api-key

## Create .env file

Copy:
```
cp .env.example .env
```

Edit:
- `AIRFLOW__FERNET_KEY`
- `ALPHA_VANTAGE_API_KEY`

## Start system

```
docker compose up --build
```

Access Airflow:

http://localhost:8080  
User: **admin**  
Pass: **admin**

Enable DAG: **stock_pipeline_googl**

Trigger DAG manually.

---

## Check Data in PostgreSQL

```
docker compose exec postgres psql -U airflow -d airflow_db -c "SELECT * FROM stock_data;"
```

---

## GitHub Setup

```
git init
git add .
git commit -m "Initial pipeline"
git branch -M main
git remote add origin <your_repo_url>
git push -u origin main
```

---

# Troubleshooting

- If `.env` not loading → ensure file name is exactly `.env`
- If Airflow scheduler not running → restart Docker
- Alpha Vantage free tier has rate limit (5 calls/min)
