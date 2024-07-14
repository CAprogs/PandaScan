
-- table "Websites"

CREATE TABLE IF NOT EXISTS "Websites" (
    "Website" TEXT,
    "Language" TEXT,
    "Link" TEXT,
    "n_update" INTEGER,
    "n_manga" INTEGER,
    "time_to_update" NUMERIC,
    "last_update" DATETIME,
    CONSTRAINT "PK_Websites" PRIMARY KEY ("Website")
);

-- table "Mangas"

CREATE TABLE IF NOT EXISTS "Mangas" (
    "MangaName" TEXT,
    "Website" TEXT,
    "n_chapter" INTEGER,
    "has_tome" TEXT,
    "last_tome"	TEXT,
    "MangaLink"	TEXT,
    CONSTRAINT "FK_Websites" FOREIGN KEY ("Website") REFERENCES "Websites" ("Website"),
    CONSTRAINT "PK_Mangas" PRIMARY KEY ("MangaName", "Website")
);

-- table "Chapters"

CREATE TABLE IF NOT EXISTS "Chapters" (
    "Website" TEXT,
    "MangaName" TEXT,
    "Chapter" TEXT,
    "ChapterLink" TEXT,
    CONSTRAINT "FK_Mangas" FOREIGN KEY ("MangaName", "Website") REFERENCES "Mangas" ("MangaName", "Website"),
    CONSTRAINT "PK_ChapterLink" PRIMARY KEY ("Website", "MangaName", "Chapter")
);

-- table "Historic"

CREATE TABLE IF NOT EXISTS "Historic" (
    "Website" TEXT,
    "MangaName" TEXT,
    "Chapter" TEXT,
    "ChapterLink" TEXT,
    "datetime" DATETIME,
    "status" TEXT,
    "TypeTraitement" TEXT, -- "download" ou "update"
    "duration" NUMERIC, -- peut etre null si le status est failed
    "n_pages" INTEGER, -- peut etre null si le status est failed
    "size" INTEGER, -- peut etre null si le status est failed ou le type de traitement est "update"
    "changelog" TEXT, -- peut etre null si le status est type de traitement est download ou le status est failed. "add" ou "delete
    "error" TEXT, -- peut etre null si le status est success
    CONSTRAINT "FK_Chapters" FOREIGN KEY ("Website", "MangaName", "Chapter") REFERENCES "Chapters" ("Website", "MangaName", "Chapter"),
    CONSTRAINT "PK_Historic" PRIMARY KEY ("Website", "MangaName", "Chapter", "datetime")
);

-- table "Duplicates"

CREATE TABLE IF NOT EXISTS "Duplicates" (
    "Website" TEXT,
    "MangaName" TEXT,
    "Chapter" TEXT,
    "ChapterLink" TEXT,
    CONSTRAINT "PK_Duplicates" PRIMARY KEY ("Website", "MangaName", "Chapter", "ChapterLink")
);