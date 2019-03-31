CREATE TEMPORARY TABLE temp(header_timestamp, update_id, trip_id, route_id, stop_id, current_stop_id, stop_number, start_date, arrival, departure);

\copy temp (header_timestamp, update_id, trip_id, route_id, stop_id, current_stop_id, stop_number, start_date, arrival, departure) FROM {} WITH CSV HEADER

WITH staging AS (
		SELECT t.id AS timestamp_id, temp.header_timestamp,
				temp.update_id, 
				tr.id AS tripname_id, temp.trip_id AS trip,
				r.id AS route_id,
				s.id AS stop_id,
				cs.id AS current_stop_id,
				temp.stop_number,
				d.id AS date_id, temp.start_date,
				temp.arrival,
				temp.departure
		FROM (temp
				LEFT JOIN mta2014_timestamp t
				ON temp.header_timestamp = t.timestamp
				LEFT JOIN mta2014_tripname tr
				ON temp.trip_id = tr.trip_name
				LEFT JOIN mta2014_routeinfo r
				ON temp.route_id = r.route_id
				LEFT JOIN mta2014_stops s
				ON temp.stop_id = s.stop_id
				LEFT JOIN mta2014_stops cs
				ON temp.current_stop_id = cs.stop_id
				LEFT JOIN mta2014_date d
				ON temp.start_date = d.date
		)
)
, ins_timestamp AS (
		INSERT INTO mta2014_timestamp(timestamp)
		SELECT DISTINCT header_timestamp FROM staging
		WHERE timestamp_id IS NULL
		RETURNING id AS timestamp_id, timestamp
)
, ins_tripname AS (
		INSERT INTO mta2014_tripname(trip_name)
		SELECT DISTINCT trip FROM staging
		WHERE tripname_id IS NULL
		RETURNING id AS trip_id, trip_name
)
, ins_date AS (
		INSERT INTO mta2014_date(date)
		SELECT DISTINCT start_date FROM staging
		WHERE date_id IS NULL
		RETURNING id AS date_id, date
)
INSERT INTO mta2014_trip (
		header_timestamp_id,
		updateid,
		trip_id,
		route_id,
		stop_id,
		current_stop_id,
		stop_number,
		start_date_id,
		arrival,
		departure)
		VALUES(
				SELECT COALESCE(staging.timestamp_id, t.timestamp_id)
				FROM staging
				LEFT JOIN ins_timestamp t
				ON staging.header_timestamp = t.timestamp,
				staging.update_id,
				SELECT COALESCE(staging.trip_id, tr.trip_id)
				FROM staging
				LEFT JOIN ins_tripname tr
				ON staging.trip = t.trip_name,
				staging.route_id,
				staging.stop_id,
				staging.current_stop_id,
				staging.stop_number,
				SELECT COALESCE(staging.date_id, d.date_id)
				FROM staging
				LEFT JOIN ins_date d
				ON staging.start_date = d.date,
				staging.arrival,
				staging.departure
		)
;

