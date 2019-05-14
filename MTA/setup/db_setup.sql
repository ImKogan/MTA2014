-- Sets up database
-- usage: sudo -u postgres psql -f db_setup.sql
-- Change as you wish, but must match settings.ini in django app!

CREATE USER mta2014 WITH PASSWORD 'mta123';
CREATE DATABASE mta2014 OWNER mta2014;

-- change user
\c mta2014;
CREATE EXTENSION postgis;
