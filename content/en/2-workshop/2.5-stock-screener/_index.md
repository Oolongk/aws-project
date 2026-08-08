---
weight: 5
title: "US Stock Screener Pipeline"
date: 2026-07-06
chapter: true
pre: "<b>2.5. </b>"
---
# US Stock Screener Pipeline

US Stock Screener Pipeline is a Data Engineering project that builds an end-to-end quantitative pipeline to ingest, normalize, and score S&P 500 stocks using Quality Minus Junk (QMJ) metrics, displaying results on a web frontend.

The objective of the project extends beyond fetching stock prices: the pipeline maintains historical datasets, segregates Raw and Processed zones, and provides a serving layer for QMJ ticker lookups.

## Project Objectives

| Objective | Project Solution |
|---|---|
| Ingest S&P 500 stock data | Fetch the ticker list from Wikipedia and market data from Yahoo Finance via `yfinance` |
| Build historical data | Local Backfill Script fetches price data from 2023 and writes by actual trading date |
| Update data daily | AWS Glue Python Shell fetches the latest price snapshot, Company Info, and Financials snapshot |
| Normalize input data | Enforce schema, convert column names to `snake_case`, cast metrics to `float64`, and date fields to `string` |
| Compute quantitative scores | AWS Glue PySpark computes profitability, growth, safety, value, momentum, and QMJ score |
| Serve data to the Web | Lambda QMJ Loader loads Processed Parquet into DynamoDB; Lambda Reader returns data to the API and Frontend |

## Key Deliverables

After completing the pipeline, the system creates three primary data layers:

| Data Layer | Location | Role |
|---|---|---|
| Raw Zone | `s3://stock-screener-raw-your-name/raw_us_market/` | Store normalized raw data from Backfill and Daily Ingestion |
| Processed Zone | `s3://stock-screener-processed-your-name/processed_qmj/as_of_date=YYYY-MM-DD/` | Store QMJ-scored, ranked Parquet output by date |
| Serving Store | DynamoDB table `qmj_screener` | Store data projected by `ticker` and `snapshot_date` for fast API queries |

Users can enter a ticker (e.g., `AAPL`) on the Web Frontend to view QMJ score history and metrics for stock screening.


![US Stock Screener Pipeline Architecture](/aws-project/images/stock-screener/diagram.jpg?featherlight=false&width=90pc)

## Architecture Layers

| Layer | Component | Responsibility |
|---|---|---|
| Data Sources | Wikipedia, Yahoo Finance, yfinance | Provide S&P 500 tickers, prices, Company Info, and Financials |
| Ingestion Layer | Local Backfill Script, Glue Python Shell | Load historical data and update daily into Raw Zone |
| Storage Layer | Amazon S3 Raw Zone, Amazon S3 Processed Zone | Store Snappy-compressed Parquet by processing stage |
| Processing Layer | AWS Glue PySpark | Clean, deduplicate, compute metrics and QMJ ranking |
| Serving Layer | S3 Event Notification, Lambda QMJ Loader, DynamoDB | Convert analytical dataset into API-optimized data |
| Presentation Layer | Lambda Reader, API Gateway, Static Web Frontend | Provide API and display QMJ information to users |

## Core Datasets

| Dataset | Description | Source |
|---|---|---|
| `us_prices_raw.parquet` | Trading prices by ticker and `price_date` | Local Backfill and Glue Python Shell |
| `us_company_info.parquet` | Company information snapshot | Local Backfill and Glue Python Shell |
| `us_financials_raw.parquet` | Quarterly or annual financial reports | Glue Python Shell |
| QMJ Processed Parquet | QMJ score, rank, profitability, growth, safety, value, and momentum | Glue PySpark Transform |
| `qmj_screener` | API-serving data by `ticker` and `snapshot_date` | Lambda QMJ Loader |

## Design Principles

| Principle | Application in Project |
|---|---|
| Schema parity | Backfill and Daily Ingestion normalize all column names, data types, and date formats before writing Parquet |
| Partitioning | Prices partitioned by trading date; Company Info and Financials partitioned by pipeline run date |
| Reprocessing | Glue Transform can be re-run from Raw Zone when QMJ formulas change, without re-crawling source data |
| Idempotent serving write | Lambda Loader uses `ticker` and `snapshot_date` as composite write key to prevent duplicate DynamoDB records |
| Separation of concerns | S3 Processed is the analytical source of truth; DynamoDB is only a serving projection for Web/API |

## Document Scope

This guide covers project deployment in the following phases:

| Chapter | Content |
|---|---|
| Chapter 1 | AWS resource preparation, S3 zones, IAM Roles, and data contract |
| Chapter 2 | Local Backfill and Glue Python Shell Daily Ingestion |
| Chapter 3 | Glue PySpark QMJ Transformation |
| Chapter 4 | Lambda QMJ Loader, DynamoDB, Lambda Reader, API Gateway, and Web Frontend |
| Chapter 5 | Automation, monitoring, testing, and resource cleanup |

{{% children %}}