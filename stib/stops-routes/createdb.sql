DROP TABLE stop_point;
DROP TABLE journey_pattern;

CREATE TABLE stop_point (id SERIAL PRIMARY KEY, gml_id varchar(255), name_fr varchar(255), name_nl varchar(255), journey_pattern_id int DEFAULT null);
SELECT AddGeometryColumn('stop_point','coord',-1,'POINT',2);

CREATE TABLE journey_pattern (id SERIAL PRIMARY KEY, direction varchar(4));
SELECT AddGeometryColumn('journey_pattern','shape',-1,'LINESTRING',2);