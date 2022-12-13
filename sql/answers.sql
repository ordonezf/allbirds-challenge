/* 
Questions 
---------
1. Report on quantity sold by month and product_type. Order sale date is in the " created_at_pacific_timestamp" column. 

2. List email addresses of customers that ordered Runners before the first time they ordered Loungers. 

3. List email addresses that ordered Runners twice before the first time they ordered Loungers. 

4. List of customers emails and its highest product price whose last order was 5 days ago.

5. Since question #2 and #3 are similar. Do you know any tool, framework or way to create a generic way to resolve this problem? For example dbt, PLSQL, etc.

6. How (if at all) would you change this schema to better support queries of this kind?
*/


-- 1. Report on quantity sold by month and product_type. Order sale date is in the " created_at_pacific_timestamp" column.
select
    to_char(created_at_pacific_timestamp, 'yyyy-mm') as month,
    s.product_type,
    sum(oli.quantity)
from orders o
join order_line_items oli on oli.order_id = o.id
join skus s on s.sku = oli.sku
group by 1,2
;

-- 2. List email addresses of customers that ordered Runners before the first time they ordered Loungers. 
with base as (
    select
        o.email,
        array_agg(s.product_type order by o.created_at_pacific_timestamp, oli.order_line_number) as products
    from orders o
    join order_line_items oli on oli.order_id = o.id
    join skus s on s.sku = oli.sku
    group by 1
)
select
    email
from base
where (cardinality((products)[:array_position(products, 'Lounger')]) - 1) >= 1


-- 3. List email addresses that ordered Runners twice before the first time they ordered Loungers. 
with base as (
    select
        o.email,
        array_agg(s.product_type order by o.created_at_pacific_timestamp, oli.order_line_number) as products
    from orders o
    join order_line_items oli on oli.order_id = o.id
    join skus s on s.sku = oli.sku
    group by 1
)
select
    email
from base
where (cardinality((products)[:array_position(products, 'Lounger')]) - 1) >= 2


-- 4. List of customers emails and its highest product price whose last order was 5 days ago.
with base as (
    select
        distinct o.email
    from orders o
    where o.created_at_pacific_timestamp >= now() - interval '5 days'
)
select
    o.email,
    max(oli.price)
from base b
join orders o on o.email = b.email
join order_line_items oli on oli.order_id = o.id
join skus s on s.sku = oli.sku
group by 1


-- 5. Since question #2 and #3 are similar. Do you know any tool, framework or way to create a generic way to resolve this problem? For example dbt, PLSQL, etc.
/*
First of all I'd change the query to support several product types, so instead of doing

where (cardinality((products)[:array_position(products, 'Lounger')]) - 1) >= x

it'd be changed to this

where cardinality(array_positions((row)[:array_position(row, 'Lounger')], 'Runner')) >= x

The difference is that the first query does not take into account having more than one product type before the first Lounger, while the second one does by "filtering" the array of products before the first Lounger to be of the type we want to check.

----------------

Materializing the CTE would probably save some computation time if we want to run this query several times.
We can do that in dbt by using an incremental model so as to not recompute the whole thing every time we run the query or go with a postgres materialized view.
Having the CTE materialized we can run the second part of the query with the arguments we like.

Going a step further, we can combine the materialization with a function on PLSQL that would take the product type and the number of times it should appear before the first "Lounger" and return the emails that match that criteria.
I've never used PLSQL so I don't know how to do that, but I'm sure it's possible.
*/

-- 6. How (if at all) would you change this schema to better support queries of this kind?
/*
I'd save time and have everything in a single table.
For a transactional model it's great to have everything normalized, but for a reporting model I like to avoid doing the same 3 joins every time I want to run a query.
An agregated materialization with some precalculations would be great for this case too.

If we can't do that at least I'd add some indexes and change the id's to autoincremental instead of varchars.
*/
