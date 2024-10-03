.mode csv
SELECT *, ROUND("weight" * "reps" * "sets", 1) as "volume"
FROM "training";
.quit