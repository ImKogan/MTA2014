CREATE UNIQUE INDEX trip_idx_date_trip_stop ON mta2014_trip (start_date_id, trip_id, stop_id);
ALTER TABLE mta2014_trip ALTER COLUMN created SET DEFAULT statement_timestamp();
