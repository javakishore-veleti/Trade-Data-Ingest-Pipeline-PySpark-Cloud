CREATE TABLE IF NOT EXISTS TRADE_EVENT_INGEST_BATCH (
    id VARCHAR(50) PRIMARY KEY,
    file_name VARCHAR(50) NOT NULL,
    row_count INTEGER NOT NULL,
    created_dt TIMESTAMP NOT NULL,
    ingest_status VARCHAR(50) NOT NULL,
    ingest_start_date_time TIMESTAMP NOT NULL,
    ingest_end_date_time TIMESTAMP NOT NULL,
    updated_dt TIMESTAMP NOT NULL,
    concurrent_number INTEGER NOT NULL
);


CREATE TABLE TRADE_EVENT (
    TradeId VARCHAR(50),
    CustomerId VARCHAR(50),
    From_Currency VARCHAR(50),
    To_Currency VARCHAR(50),
    From_Cost NUMERIC,
    To_Cost NUMERIC,
    From_Pip NUMERIC,
    To_Pip NUMERIC,
    Transaction_Date TIMESTAMP,
    Transaction_Status VARCHAR(50),
    Created_By VARCHAR(50),
    Created_On TIMESTAMP,
    Updated_By VARCHAR(50),
    Updated_on TIMESTAMP,
    From_Deposited_Account VARCHAR(50),
    To_Debited_Account VARCHAR(50),
    batch_id VARCHAR(50),
    batch_concurrent_number INTEGER,
    ingest_date TIMESTAMP,
    concurrent_number INTEGER
);
