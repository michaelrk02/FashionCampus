FROM postgres:latest

EXPOSE 5432

COPY ./migration/init.sql /docker-entrypoint-initdb.d/001-init.sql
COPY ./migration/v_001_000/up.sql /docker-entrypoint-initdb.d/002-migrate-v_001_000.sql
