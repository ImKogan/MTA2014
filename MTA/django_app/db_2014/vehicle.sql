COPY temp ({}) FROM STDIN WITH CSV HEADER;

WITH temp AS (
	SELECT * FROM temp
)
, staging AS (
	SELECT status.id AS status_id,
		temp.current_stop_sequence,
		t.id AS timestamp_id, temp.{header_timestamp_id},
		temp.updateid, 
		r.id AS route_id,
		d.id AS start_date_id, temp.{start_date_id},
		s.id AS stop_id,
		temp.timestamp,
		tr.id AS trip_id, temp.trip AS {trip_id}
		FROM temp
		LEFT JOIN mta2014_status status
		ON temp.current_status = status.status
		LEFT JOIN mta2014_timestamp t
		ON temp.header_timestamp = t.timestamp
		LEFT JOIN mta2014_routeinfo r
		ON temp.route = r.route_id
		LEFT JOIN mta2014_date d
		ON temp.start_date = d.date
		LEFT JOIN mta2014_stops s
		ON temp.stop = s.stop_id
		LEFT JOIN mta2014_tripname tr
		ON temp.trip = tr.trip_name
)
, ins_timestamp AS (
		INSERT INTO mta2014_timestamp(timestamp)
		SELECT DISTINCT {header_timestamp_id} FROM staging
		WHERE timestamp_id IS NULL
		RETURNING id AS timestamp_id, timestamp
)
, ins_tripname AS (
		INSERT INTO mta2014_tripname(trip_name)
		SELECT DISTINCT {trip_id} FROM staging
		WHERE trip_id IS NULL
		RETURNING id AS trip_id, trip_name
)
, ins_date AS (
		INSERT INTO mta2014_date(date)
		SELECT DISTINCT {start_date_id} FROM staging
		WHERE start_date_id IS NULL
		RETURNING id AS start_date_id, date
)
INSERT INTO {} ({})
		SELECT staging.status_id,
		staging.current_stop_sequence,
		COALESCE(staging.timestamp_id, t.timestamp_id),
		staging.updateid,
		staging.route_id,
		COALESCE(staging.start_date_id, d.start_date_id),
		staging.stop_id,
		staging.timestamp,
		COALESCE(staging.trip_id, tr.trip_id)
		FROM staging
		LEFT JOIN ins_timestamp t
		ON staging.header_timestamp = t.timestamp
		LEFT JOIN ins_tripname tr
		ON staging.trip = tr.trip_name
		LEFT JOIN ins_date d
		ON staging.start_date = d.date
;
