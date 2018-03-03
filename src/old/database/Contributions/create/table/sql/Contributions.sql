create table "Contributions"(
    "Id"                integer primary key,
    "Date"              text not null,
    "Count"             integer not null check(0 <= "Count")
);
