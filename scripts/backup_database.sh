pg_dumpall -U postgres -h localhost -p 5432 --clean --globals-only --file=globals.sql
pg_dump -U postgres -h localhost -p 5432 --clean --file=pimp.sql pimp