alerts = LOAD '/data/clean/incidents_clean.csv'
    USING PigStorage(',')
    AS (type:chararray, comuna:chararray, descripcion:chararray,
        report_rating:int, location_x:double, location_y:double);

alerts_clean = FILTER alerts BY type != 'type';

-- Conteo por tipo
by_type = GROUP alerts_clean BY type;
count_by_type = FOREACH by_type GENERATE
    group AS type,
    COUNT(alerts_clean) AS count;
STORE count_by_type INTO '/data/output/incidents_by_type.csv' USING PigStorage(',');

-- Conteo por comuna
by_comuna = GROUP alerts_clean BY comuna;
count_by_comuna = FOREACH by_comuna GENERATE
    group AS comuna,
    COUNT(alerts_clean) AS count;
STORE count_by_comuna INTO '/data/output/incidents_by_comuna.csv' USING PigStorage(',');

-- Conteo por tipo + comuna
by_both = GROUP alerts_clean BY (type, comuna);
count_by_both = FOREACH by_both GENERATE
    group.type AS type,
    group.comuna AS comuna,
    COUNT(alerts_clean) AS count;
STORE count_by_both INTO '/data/output/incidents_by_type_and_comuna.csv' USING PigStorage(',');

-- Comunas con más incidentes
ordered_comunas = ORDER count_by_comuna BY count DESC;
STORE ordered_comunas INTO '/data/output/top_comunas.csv' USING PigStorage(',');
