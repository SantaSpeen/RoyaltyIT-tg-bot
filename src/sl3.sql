DROP TABLE IF EXISTS `users`;

CREATE TABLE users (
    id           INTEGER PRIMARY KEY AUTOINCREMENT
                         UNIQUE,
    user_id      INTEGER UNIQUE
                         NOT NULL,
    warns        INTEGER DEFAULT (0),
    muted_until  DOUBLE  DEFAULT (0.0),
    banned_until DOUBLE  DEFAULT (0.0)
);