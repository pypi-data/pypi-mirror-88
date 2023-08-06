-- Table: profile_transform

-- DROP TABLE profile_transform;

CREATE TABLE profile_transform (
          id serial NOT NULL,
          branch character varying(20), -- Entwicklungszweig, oder NULL für Trunk
          rev integer, -- Revision, wie vom versioninformation-Browser angegeben
          method character varying, -- "regex" (alte Methode) oder "soup" (neue Methode mit BeautifulSoup)
          "timestamp" timestamp without time zone, -- Wann war der Request?
          path character varying(255), -- Pfad der Anforderung
          debug boolean DEFAULT false, -- Wenn debug-Modus aktiv war, ist die gemessene Zeit nicht aussagekräftig
          traced boolean DEFAULT false, -- Wenn set_trace aktiv war, ist die gemessene Zeit noch weniger aussagekräftig
          size_input integer, -- Länge des Eingabe-Strings (Python-Standardfunktion "len")
          size_output integer, -- Länge des Ausgabe-Strings (Python-Standardfunktion "len")
          time_processor double precision, -- Für die Anforderung aufgewendete Prozessorzeit
          time_total double precision, -- Gestoppte Zeit von Anforderung bis Ausgabe
          CONSTRAINT profile_transform_pk PRIMARY KEY (id)
);
ALTER TABLE profile_transform
  OWNER TO "www-data";
COMMENT ON TABLE profile_transform
  IS 'Tabelle zur Performanzanalyse des transform-Browsers';
COMMENT ON COLUMN profile_transform.branch IS 'Entwicklungszweig, oder NULL für Trunk';
COMMENT ON COLUMN profile_transform.rev IS 'Revision, wie vom versioninformation-Browser angegeben';
COMMENT ON COLUMN profile_transform.method IS '"regex" (alte Methode) oder "soup" (neue Methode mit BeautifulSoup)';
COMMENT ON COLUMN profile_transform."timestamp" IS 'Wann war der Request?';
COMMENT ON COLUMN profile_transform.path IS 'Pfad der Anforderung';
COMMENT ON COLUMN profile_transform.debug IS 'Wenn debug-Modus aktiv war, ist die gemessene Zeit nicht sehr aussagekräftig';
COMMENT ON COLUMN profile_transform.traced IS 'Wenn set_trace aktiv war, ist die gemessene Zeit noch weniger aussagekräftig (für einzelne Requests manuell zu setzen)';
COMMENT ON COLUMN profile_transform.size_input IS 'Länge des Eingabe-Strings (Python-Standardfunktion "len")';
COMMENT ON COLUMN profile_transform.size_output IS 'Länge des Ausgabe-Strings (Python-Standardfunktion "len")';
COMMENT ON COLUMN profile_transform.time_processor IS 'Für die Anforderung aufgewendete Prozessorzeit';
COMMENT ON COLUMN profile_transform.time_total IS 'Gestoppte Zeit von Anforderung bis Ausgabe';


