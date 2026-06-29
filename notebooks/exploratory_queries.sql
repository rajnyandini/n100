-- ==========================================================
-- N100 Financial Intelligence Platform
-- Exploratory SQL Queries
-- ==========================================================

-- Query 1: Total number of companies
SELECT COUNT(*) AS total_companies
FROM companies;


-- Query 2: Top 10 companies by ROE
SELECT
    company_name,
    roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;


-- Query 3: Companies with highest book value
SELECT
    company_name,
    book_value
FROM companies
ORDER BY book_value DESC
LIMIT 10;


-- Query 4: Number of records in each table
SELECT 'companies' AS table_name, COUNT(*) FROM companies
UNION ALL
SELECT 'profitandloss', COUNT(*) FROM profitandloss
UNION ALL
SELECT 'balancesheet', COUNT(*) FROM balancesheet
UNION ALL
SELECT 'cashflow', COUNT(*) FROM cashflow
UNION ALL
SELECT 'analysis', COUNT(*) FROM analysis
UNION ALL
SELECT 'documents', COUNT(*) FROM documents
UNION ALL
SELECT 'prosandcons', COUNT(*) FROM prosandcons
UNION ALL
SELECT 'sectors', COUNT(*) FROM sectors
UNION ALL
SELECT 'stock_prices', COUNT(*) FROM stock_prices
UNION ALL
SELECT 'financial_ratios', COUNT(*) FROM financial_ratios
UNION ALL
SELECT 'peer_groups', COUNT(*) FROM peer_groups
UNION ALL
SELECT 'market_cap', COUNT(*) FROM market_cap;


-- Query 5: Companies having fewer than 5 years of financial records
SELECT
    company_id,
    COUNT(*) AS years
FROM profitandloss
GROUP BY company_id
HAVING COUNT(*) < 5
ORDER BY years;


-- Query 6: Highest market capitalization
SELECT
    company_id,
    MAX(market_cap_crore) AS market_cap
FROM market_cap
GROUP BY company_id
ORDER BY market_cap DESC
LIMIT 10;


-- Query 7: Companies with highest EPS
SELECT
    company_id,
    MAX(eps) AS highest_eps
FROM profitandloss
GROUP BY company_id
ORDER BY highest_eps DESC
LIMIT 10;


-- Query 8: Average closing stock price
SELECT
    company_id,
    ROUND(AVG(close_price),2) AS average_close
FROM stock_prices
GROUP BY company_id
ORDER BY average_close DESC
LIMIT 10;


-- Query 9: Sector-wise company count
SELECT
    broad_sector,
    COUNT(*) AS companies
FROM sectors
GROUP BY broad_sector
ORDER BY companies DESC;


-- Query 10: Companies having negative operating cash flow
SELECT
    company_id,
    year,
    operating_activity
FROM cashflow
WHERE operating_activity < 0
ORDER BY operating_activity;