CREATE TABLE guest
(
    id SERIAL NOT NULL PRIMARY KEY,
    reg_number VARCHAR(50),
    full_name_uz TEXT,
    full_name_ru TEXT,
    table_number INTEGER NOT NULL,
    persons_count INTEGER,
    is_reg_number_generated BOOLEAN DEFAULT FALSE,
    is_registered BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

alter table guest
add column phone_number TEXT;

alter table guest
add column is_entered BOOLEAN DEFAULT FALSE;

alter table guest
add column telegram_id BIGINT;