USE dk_dtu_compute_facebook;
ALTER TABLE main ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on main;
ALTER TABLE main ADD UNIQUE INDEX(uniqueness_hash);

ALTER TABLE developer ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on developer;
ALTER TABLE developer ADD UNIQUE INDEX(uniqueness_hash);

ALTER TABLE researcher ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on researcher;
ALTER TABLE researcher ADD UNIQUE INDEX(uniqueness_hash);

USE dk_dtu_compute_questionnaire;
ALTER TABLE main ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on main;
ALTER TABLE main ADD UNIQUE INDEX(uniqueness_hash);

ALTER TABLE developer ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on developer;
ALTER TABLE developer ADD UNIQUE INDEX(uniqueness_hash);

ALTER TABLE researcher ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on researcher;
ALTER TABLE researcher ADD UNIQUE INDEX(uniqueness_hash);

USE edu_mit_media_funf_probe_builtin_BluetoothProbe;
ALTER TABLE main ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on main;
ALTER TABLE main ADD UNIQUE INDEX(uniqueness_hash);

ALTER TABLE developer ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on developer;
ALTER TABLE developer ADD UNIQUE INDEX(uniqueness_hash);

ALTER TABLE researcher ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on researcher;
ALTER TABLE researcher ADD UNIQUE INDEX(uniqueness_hash);

USE edu_mit_media_funf_probe_builtin_CallLogProbe;
ALTER TABLE main ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on main;
ALTER TABLE main ADD UNIQUE INDEX(uniqueness_hash);

ALTER TABLE developer ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on developer;
ALTER TABLE developer ADD UNIQUE INDEX(uniqueness_hash);

ALTER TABLE researcher ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on researcher;
ALTER TABLE researcher ADD UNIQUE INDEX(uniqueness_hash);

USE edu_mit_media_funf_probe_builtin_CellProbe;
ALTER TABLE main ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on main;
ALTER TABLE main ADD UNIQUE INDEX(uniqueness_hash);

ALTER TABLE developer ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on developer;
ALTER TABLE developer ADD UNIQUE INDEX(uniqueness_hash);

ALTER TABLE researcher ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on researcher;
ALTER TABLE researcher ADD UNIQUE INDEX(uniqueness_hash);

USE edu_mit_media_funf_probe_builtin_ContactProbe;
ALTER TABLE main ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on main;
ALTER TABLE main ADD UNIQUE INDEX(uniqueness_hash);

ALTER TABLE developer ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on developer;
ALTER TABLE developer ADD UNIQUE INDEX(uniqueness_hash);

ALTER TABLE researcher ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on researcher;
ALTER TABLE researcher ADD UNIQUE INDEX(uniqueness_hash);

USE edu_mit_media_funf_probe_builtin_HardwareInfoProbe;
ALTER TABLE main ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on main;
ALTER TABLE main ADD UNIQUE INDEX(uniqueness_hash);

ALTER TABLE developer ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on developer;
ALTER TABLE developer ADD UNIQUE INDEX(uniqueness_hash);

ALTER TABLE researcher ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on researcher;
ALTER TABLE researcher ADD UNIQUE INDEX(uniqueness_hash);

USE edu_mit_media_funf_probe_builtin_LocationProbe;
ALTER TABLE main ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on main;
ALTER TABLE main ADD UNIQUE INDEX(uniqueness_hash);

ALTER TABLE developer ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on developer;
ALTER TABLE developer ADD UNIQUE INDEX(uniqueness_hash);

ALTER TABLE researcher ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on researcher;
ALTER TABLE researcher ADD UNIQUE INDEX(uniqueness_hash);

USE edu_mit_media_funf_probe_builtin_ScreenProbe;
ALTER TABLE main ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on main;
ALTER TABLE main ADD UNIQUE INDEX(uniqueness_hash);

ALTER TABLE developer ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on developer;
ALTER TABLE developer ADD UNIQUE INDEX(uniqueness_hash);

ALTER TABLE researcher ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on researcher;
ALTER TABLE researcher ADD UNIQUE INDEX(uniqueness_hash);

USE edu_mit_media_funf_probe_builtin_SMSProbe;
ALTER TABLE main ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on main;
ALTER TABLE main ADD UNIQUE INDEX(uniqueness_hash);

ALTER TABLE developer ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on developer;
ALTER TABLE developer ADD UNIQUE INDEX(uniqueness_hash);

ALTER TABLE researcher ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on researcher;
ALTER TABLE researcher ADD UNIQUE INDEX(uniqueness_hash);

USE edu_mit_media_funf_probe_builtin_TimeOffsetProbe;
ALTER TABLE main ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on main;
ALTER TABLE main ADD UNIQUE INDEX(uniqueness_hash);

ALTER TABLE developer ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on developer;
ALTER TABLE developer ADD UNIQUE INDEX(uniqueness_hash);

ALTER TABLE researcher ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on researcher;
ALTER TABLE researcher ADD UNIQUE INDEX(uniqueness_hash);

USE edu_mit_media_funf_probe_builtin_WifiProbe;
ALTER TABLE main ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on main;
ALTER TABLE main ADD UNIQUE INDEX(uniqueness_hash);

ALTER TABLE developer ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on developer;
ALTER TABLE developer ADD UNIQUE INDEX(uniqueness_hash);

ALTER TABLE researcher ADD uniqueness_hash BINARY(20);
DROP INDEX compound_unique on researcher;
ALTER TABLE researcher ADD UNIQUE INDEX(uniqueness_hash);