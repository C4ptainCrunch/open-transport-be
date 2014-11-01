DROP TABLE stop_point;
DROP TABLE journey_pattern;

CREATE TABLE stop_point (
    id SERIAL PRIMARY KEY,
    uid varchar(255),
    stib_id int,
    name_fr varchar(255),
    name_nl varchar(255),
    slug_fr varchar(255),
    slug_nl varchar(255),
    pattern_order int,
    journey_pattern_id int DEFAULT null
);

SELECT AddGeometryColumn('stop_point','coord',-1,'POINT',2);

CREATE TABLE journey_pattern (
    id SERIAL PRIMARY KEY,
    uid varchar(255),
    mode varchar(255),
    line_number varchar(255),
    direction varchar(4)
);

SELECT AddGeometryColumn('journey_pattern','shape',-1,'LINESTRING',2);
SELECT AddGeometryColumn('journey_pattern','start_point',-1,'POINT',2);