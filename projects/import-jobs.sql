.mode csv
CREATE TABLE IF NOT EXISTS jobs (
  JobID NOT NULL PRIMARY KEY,
  Start,
  End,
  Elapsed,
  AllocCPUS,
  Partition,
  Account,
  State
);
.import "jobs.csv" jobs
