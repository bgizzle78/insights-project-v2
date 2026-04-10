-- Row count check
SELECT COUNT(*)
FROM bls_employment;

-- Sample data check
SELECT *
FROM bls_employment
LIMIT ;

-- Industry count check
SELECT DISTINCT industry
FROM bls_employment;