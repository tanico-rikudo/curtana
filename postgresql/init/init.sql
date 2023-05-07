CREATE USER docker  WITH PASSWORD 'pass';
CREATE DATABASE docker;
GRANT ALL PRIVILEGES ON DATABASE docker TO docker;
\c docker

create table BUYBACK_HEADLINE
(
    id SERIAL NOT NULL,
    edinet_code CHAR(16) NOT NULL,
    doc_id CHAR(16) NOT NULL,
    filer_name CHAR(256) NOT NULL,
    doc_type_code CHAR(256) NOT NULL,
    submit_datetime TIMESTAMP NOT NULL,
    xbrl_flag bool NOT NULL,
    created_on TIMESTAMP default CURRENT_TIMESTAMP,
    updated_on TIMESTAMP default CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

create table BUYBACK_DETAIL
(
    id SERIAL NOT NULL,
    doc_id CHAR(16) NOT NULL,
    acquition_type CHAR(256) NOT NULL,
    buy_date DATE NOT NULL,
    buy_qty DOUBLE PRECISION NOT NULL,
    buy_notional DOUBLE PRECISION NOT NULL,
    created_on TIMESTAMP default CURRENT_TIMESTAMP,
    updated_on TIMESTAMP default CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

create table DOCUMENT_FETCH_HISTORY
(
    id SERIAL NOT NULL,
    doc_type CHAR(16) NOT NULL,
    doc_id CHAR(16) NOT NULL,
    success_flag CHAR(16) NOT NULL,
    created_on TIMESTAMP default CURRENT_TIMESTAMP,
    updated_on TIMESTAMP default CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Function
CREATE  FUNCTION update_updated_on_user_task()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_on = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

--  Trigers
CREATE TRIGGER update_buyback_detail_updated_on
    BEFORE UPDATE
    ON
        BUYBACK_HEADLINE
    FOR EACH ROW
EXECUTE PROCEDURE update_updated_on_user_task();

CREATE TRIGGER update_buyback_detail_updated_on
    BEFORE UPDATE
    ON
        BUYBACK_DETAIL
    FOR EACH ROW
EXECUTE PROCEDURE update_updated_on_user_task();

