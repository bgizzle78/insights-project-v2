-- ============================================
-- 1. BASE JOINS (FOUNDATION)
-- ============================================

-- -- employment + gdp
-- SELECT *
-- FROM bls_employment e
-- JOIN bea_gdp g
-- ON e.year = g.year
-- AND e.industry = g.industry;


-- ============================================
-- 2. DERIVED METRICS
-- ============================================

-- -- gdp per employee
-- SELECT
--     year,
--     industry,
--     employment,
--     gdp,
--     ROUND(CAST((gdp / NULLIF(employment, 0)) AS numeric), 2) AS gdp_per_worker
-- FROM employment_gdp;

-- ============================================
-- 3. TEST JOIN: WVSOS + EMPLOYMENT
-- ============================================

-- add wvsos data
SELECT
    w.year,
    w.industry,
    w.new_filings,
    e.employment
FROM wvsos_clean w
JOIN bls_employment e
    ON w.year = e.year
    AND w.industry = e.industry;


-- ============================================
-- 4. DASHBOARD QUERIES
-- ============================================

-- queries specifically for Streamlit