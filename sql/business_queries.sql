SELECT 
        state,
        ROUND(SUM(amount_cr), 2) AS total_amount_cr,
        SUM(count) AS total_transactions,
        ROUND(SUM(amount_cr) * 100.0 / (SELECT SUM(amount_cr) FROM transactions), 2) AS pct_of_india
    FROM transactions
    GROUP BY state
    ORDER BY total_amount_cr DESC
    LIMIT 10



SELECT
        year,
        SUM(count) AS total_transactions,
        ROUND(SUM(amount_cr), 0) AS total_amount_cr,
        ROUND(
            (SUM(amount_cr) - LAG(SUM(amount_cr)) OVER (ORDER BY year)) 
            * 100.0 / LAG(SUM(amount_cr)) OVER (ORDER BY year), 
        2) AS yoy_growth_pct
    FROM transactions
    GROUP BY year
    ORDER BY year




WITH ranked AS (
        SELECT
            state,
            transaction_type,
            SUM(count) AS total_count,
            RANK() OVER (PARTITION BY state ORDER BY SUM(count) DESC) AS rnk
        FROM transactions
        GROUP BY state, transaction_type
    )
    SELECT state, transaction_type, total_count
    FROM ranked
    WHERE rnk = 1
    ORDER BY total_count DESC




WITH yearly AS (
        SELECT
            state,
            year,
            SUM(amount_cr) AS amount_cr
        FROM transactions
        GROUP BY state, year
    ),
    with_growth AS (
        SELECT
            state,
            year,
            amount_cr,
            LAG(amount_cr) OVER (PARTITION BY state ORDER BY year) AS prev_amount
        FROM yearly
    )
    SELECT
        state,
        year,
        ROUND(amount_cr, 1) AS amount_cr,
        ROUND((amount_cr - prev_amount) * 100.0 / prev_amount, 1) AS yoy_growth_pct
    FROM with_growth
    WHERE year = (SELECT MAX(year) FROM transactions)
        AND prev_amount IS NOT NULL
    ORDER BY yoy_growth_pct DESC
    LIMIT 10




SELECT
        quarter,
        ROUND(AVG(quarterly_amount), 0) AS avg_amount_cr,
        ROUND(SUM(quarterly_amount), 0) AS total_amount_cr,
        ROUND(
            AVG(quarterly_amount) * 100.0 / 
            (SELECT AVG(sub.quarterly_amount) 
             FROM (SELECT SUM(amount_cr) AS quarterly_amount 
                   FROM transactions GROUP BY year, quarter) sub),
        1) AS pct_vs_avg
    FROM (
        SELECT year, quarter, SUM(amount_cr) AS quarterly_amount
        FROM transactions
        GROUP BY year, quarter
    )
    GROUP BY quarter
    ORDER BY quarter




WITH state_totals AS (
        SELECT
            t.state,
            SUM(t.count) AS total_transactions,
            SUM(u.registered_users) AS total_users,
            ROUND(CAST(SUM(t.count) AS FLOAT) / SUM(u.registered_users), 2) AS txn_per_user
        FROM transactions t
        JOIN users u ON t.state = u.state AND t.year = u.year AND t.quarter = u.quarter
        GROUP BY t.state
    )
    SELECT
        state,
        total_transactions,
        total_users,
        txn_per_user,
        CASE
            WHEN txn_per_user < 5 THEN 'High churn risk'
            WHEN txn_per_user BETWEEN 5 AND 15 THEN 'Average engagement'
            ELSE 'Highly engaged'
        END AS engagement_label
    FROM state_totals
    ORDER BY txn_per_user ASC




WITH yearly_state AS (
        SELECT
            state,
            year,
            SUM(amount_cr) AS amount_cr,
            RANK() OVER (PARTITION BY year ORDER BY SUM(amount_cr) DESC) AS rnk
        FROM transactions
        GROUP BY state, year
    )
    SELECT state, year, ROUND(amount_cr, 0) AS amount_cr, rnk
    FROM yearly_state
    WHERE rnk <= 5
    ORDER BY year, rnk




