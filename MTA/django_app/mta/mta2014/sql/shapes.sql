UPDATE mta2014_shapes
SET routeinfo_id = r.id
FROM mta2014_routeinfo AS r
WHERE 
route_name = r.route_id

