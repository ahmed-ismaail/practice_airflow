SELECT 
    customerid,
    count(orderid) as orders_count,
    count(storeid) as store_count,
    sum(revenue) as revenue 
FROM
    l2_processing.orders_fact
GROUP BY
    customerid
;