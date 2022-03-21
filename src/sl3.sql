DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `mailing`;

CREATE TABLE users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT
                        UNIQUE,
    user_id     INTEGER UNIQUE
                        NOT NULL,
    warns       INTEGER DEFAULT (0),
    muted_until DOUBLE  DEFAULT (0.0),
    banned      BOOLEAN DEFAULT (0),
    ban_by      INTEGER,
    ban_msg     TEXT
);


CREATE TABLE mailing (
    id      INTEGER PRIMARY KEY AUTOINCREMENT
                    UNIQUE,
    user_id INTEGER UNIQUE
                    NOT NULL,
    enable  BOOLEAN DEFAULT (1)
);
