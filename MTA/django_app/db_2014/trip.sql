COPY temp ({}) FROM STDIN WITH CSV HEADER;

WITH temp AS (
		SELECT DISTINCT ON
		(temp.start_date, temp.trip, temp.stop) *
		FROM temp
		WHERE temp.header_timestamp <= temp.arrival
		OR temp.header_timestamp <= temp.departure
		ORDER BY temp.start_date, temp.trip, temp.stop, temp.stop_number,
		temp.header_timestamp DESC
)
, staging AS (
		SELECT t.id AS timestamp_id, temp.{header_timestamp_id},
				temp.updateid, 
				tr.id AS trip_id, temp.trip AS {trip_id},
				r.id AS route_id,
				s.id AS stop_id,
				cs.id AS current_stop_id,
				temp.stop_number,
				d.id AS start_date_id, temp.{start_date_id},
				temp.arrival,
				temp.departure
				FROM temp
				LEFT JOIN mta2014_timestamp t
				ON temp.header_timestamp = t.timestamp
				LEFT JOIN mta2014_tripname tr
				ON temp.trip = tr.trip_name
				LEFT JOIN mta2014_routeinfo r
				ON temp.route = r.route_id
				LEFT JOIN mta2014_stops s
				ON temp.stop = s.stop_id
				LEFT JOIN mta2014_stops cs
				ON temp.current_stop = cs.stop_id
				LEFT JOIN mta2014_date d
				ON temp.start_date = d.date
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
		SELECT COALESCE(staging.timestamp_id, t.timestamp_id),
		staging.updateid,
		COALESCE(staging.trip_id, tr.trip_id),
		staging.route_id,
		staging.stop_id,
		staging.current_stop_id,
		staging.stop_number,
		COALESCE(staging.start_date_id, d.start_date_id),
		staging.arrival,
		staging.departure
		FROM staging
		LEFT JOIN ins_timestamp t
		ON staging.header_timestamp = t.timestamp
		LEFT JOIN ins_tripname tr
		ON staging.trip = tr.trip_name
		LEFT JOIN ins_date d
		ON staging.start_date = d.date
		ON CONFLICT (start_date_id, trip_id, stop_id)
		DO UPDATE
		SET header_timestamp_id = excluded.header_timestamp_id,
		updateid = excluded.updateid,
		route_id = excluded.route_id,
		current_stop_id = excluded.current_stop_id,
		stop_number = excluded.stop_number,
		arrival = excluded.arrival,
		departure = excluded.departure
;
