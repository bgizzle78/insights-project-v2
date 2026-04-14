-- ==============================
-- BLS Employment Preview
-- ==============================

-- -- Row count check
-- SELECT COUNT(*)
-- FROM bls_employment;

-- -- Sample data check
-- SELECT *
-- FROM bls_employment
-- LIMIT ;

-- -- Industry count check
-- SELECT DISTINCT industry
-- FROM bls_employment;

-- ==============================
-- BLS Unemployment Preview
-- ==============================

-- -- Row count check
-- SELECT COUNT(*)
-- FROM bls_unemployment;

-- -- Sample data check
-- SELECT *
-- FROM bls_unemployment;

-- ==============================
-- WVSOS Preview
-- ==============================

-- -- Row count check
-- SELECT COUNT(*)
-- FROM wvsos_yearly;

-- -- Distinct industry check
-- SELECT DISTINCT industry
-- FROM wvsos_yearly;

-- ==============================
-- BEA Preview
-- ==============================

-- -- Row count check
-- SELECT COUNT(*)
-- FROM bea_gdp;

-- -- Distinct industry check
-- SELECT DISTINCT industry
-- FROM bea_gdp;


-- ==============================
-- BEA/BLS Employment Join Validation
-- ==============================

-- -- -- Row count check
-- SELECT COUNT(*)
-- FROM employment_gdp;

-- -- Sample data check
-- SELECT *
-- FROM employment_gdp_enriched
-- LIMIT ;


-- ============================================
-- VALIDATE WVSOS VIEWS (2)
-- ============================================

-- -- Total rows
-- SELECT COUNT(*)
-- FROM wvsos_yearly;

-- -- Check unknown share
-- SELECT industry, COUNT(*)
-- FROM wvsos_yearly
-- GROUP BY industry
-- ORDER BY COUNT(*) DESC;

-- -- Compare clean vs total
-- SELECT COUNT(*)
-- FROM wvsos_clean;

-- SELECT COUNT(*)
-- FROM wvsos_total;


-- ============================================
-- VALIDATE ECONOMIC MASTER VIEW
-- ============================================

-- SELECT COUNT(*)
-- FROM economic_master;

-- SELECT *
-- FROM economic_master
-- LIMIT 10;


-- ============================================
-- VALIDATE UNEMPLOYMENT VIEW
-- ============================================

SELECT *
FROM unemployment;

SELECT COUNT(*)
FROM unemployment;