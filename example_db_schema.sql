/* DATABASE SCHEMA : example.db :: sqlite3                            */

CREATE TABLE IF NOT EXISTS country (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT    NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS customer (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL UNIQUE,
    country_id INTEGER NOT NULL,
    FOREIGN KEY ( country_id )
        REFERENCES country ( id )
        ON DELETE CASCADE
        ON UPDATE RESTRICT
);

CREATE TABLE IF NOT EXISTS merchant (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL UNIQUE,
    country_id INTEGER NOT NULL,
    FOREIGN KEY ( country_id )
        REFERENCES country ( id )
        ON DELETE CASCADE
        ON UPDATE RESTRICT
);

CREATE TABLE IF NOT EXISTS product (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    merchant_id INTEGER NOT NULL,
    name        TEXT    NOT NULL,
    price       REAL    NOT NULL,
    status      TEXT    NOT NULL,
    FOREIGN KEY ( merchant_id )
        REFERENCES merchant ( id )
        ON DELETE CASCADE
        ON UPDATE RESTRICT
);

CREATE TABLE IF NOT EXISTS customer_order (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    status      TEXT    NOT NULL,
    FOREIGN KEY ( customer_id )
        REFERENCES customer ( id )
        ON DELETE CASCADE
        ON UPDATE RESTRICT
);

CREATE TABLE IF NOT EXISTS order_item (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_order_id INTEGER NOT NULL,
    product_id        INTEGER NOT NULL,
    quantity          INTEGER NOT NULL,
    FOREIGN KEY ( customer_order_id )
        REFERENCES customer_order ( id )
        ON DELETE CASCADE
        ON UPDATE RESTRICT
    FOREIGN KEY ( product_id )
        REFERENCES product ( id )
        ON DELETE CASCADE
        ON UPDATE RESTRICT
);

/* END DATABASE SCHEMA : example.db :: sqlite3                        */
