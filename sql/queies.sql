SELECT
  t.customer_id,
  t.orders_count,
  CASE
    WHEN t.orders_count = 0 THEN 'inactive'
    WHEN t.orders_count = 1 THEN 'new'
    ELSE 'active'
  END AS customer_status
FROM (
  SELECT
    c.customer_id,
    COUNT(s.invoice_id) AS orders_count
  FROM customers c
  LEFT JOIN sales s
    ON c.customer_id = s.customer_id
  GROUP BY c.customer_id
) t
ORDER BY t.orders_count DESC;

SELECT
    c.customer_id
FROM customers c 
LEFT JOIN sales s 
    ON c.customer_id = s.customer_id
    WHERE s.invoice_id IS NULL