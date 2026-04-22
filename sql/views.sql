-- ============================================
-- VIEW: employment + gdp
-- ============================================

-- CREATE VIEW employment_gdp AS
-- SELECT
--     e.year,
--     e.industry,
--     e.employment,
--     g.gdp
-- FROM bls_employment e
-- INNER JOIN bea_gdp g
--     ON e.year = g.year
--     AND e.industry = g.industry
-- ORDER BY e.year, e.industry;


-- ============================================
-- VIEW: employment + gdp + productivity
-- ============================================

-- CREATE VIEW employment_gdp_enriched AS
-- SELECT
--     year,
--     industry,
--     employment,
--     gdp,
--     ROUND(CAST((gdp / NULLIF(employment, 0)) AS numeric), 2) AS gdp_per_worker
-- FROM employment_gdp;


-- ============================================
-- VIEW: WVSOS CLEAN (standardized industries)
-- Used for joins with BLS + BEA
-- ============================================

-- CREATE VIEW wvsos_clean AS
-- SELECT
--     year,
--     industry,
--     new_filings,
--     terminations
-- FROM wvsos_yearly
-- WHERE industry != 'Unknown Industry';


-- ============================================
-- VIEW: WVSOS TOTAL ACTIVITY (includes unknown)
-- Used for KPI + data completeness analysis
-- ============================================

-- CREATE VIEW wvsos_total AS
-- SELECT
--     year,
--     industry,
--     new_filings,
--     terminations
-- FROM wvsos_yearly;


-- ============================================
-- VIEW: ECONOMIC MASTER (CORE ANALYTICS LAYER)
-- ============================================

-- CREATE VIEW economic_master AS
-- SELECT
--     e.year,
--     e.industry,
--     e.employment,
--     e.gdp,
--     e.gdp_per_worker,
--     w.new_filings,
--     w.terminations
-- FROM employment_gdp_enriched e
-- JOIN wvsos_clean w
--     ON e.year = w.year
--     AND e.industry = w.industry;



-- ============================================
-- VIEW: UNEMPLOYMENT (MACRO LEVEL)
-- ============================================

-- CREATE VIEW unemployment AS
-- SELECT
--     year,
--     unemployment_rate,
--     labor_force_participation_rate,
--     labor_force
-- FROM bls_unemployment;