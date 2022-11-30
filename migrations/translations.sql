CREATE TABLE IF NOT EXISTS "translations" (
    "id" INTEGER NOT NULL,
    "originaltext" TEXT NOT NULL,
    "language" CHAR(3),
    "translatedtext" TEXT NOT NULL,
    PRIMARY KEY("id" AUTOINCREMENT)
)