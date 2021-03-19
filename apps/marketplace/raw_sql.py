ROOT_WITH_LOTS_COUNT = """WITH RECURSIVE

flat_categories (id, flat_id, parent_id) AS
(
  SELECT id, id, parent_id
    FROM marketplace_category
  UNION ALL
  SELECT c.id, ft.flat_id, c.parent_id
    FROM marketplace_category c
    INNER JOIN flat_categories ft ON c.id = ft.parent_id
),

top_cats_with_l_c (id, parent_id, lots_count) AS
(
SELECT id, parent_id, cat_lots_count.count AS lots_count
FROM
  (
    SELECT
      flat_ac.category_id, COUNT(*) AS count
    FROM
      (
        SELECT fc.id AS category_id
        FROM flat_categories fc
        left JOIN marketplace_lot ll ON fc.flat_id = ll.category_id
        WHERE ll.is_active = true -- only active lots
      ) AS flat_ac
    GROUP BY flat_ac.category_id
  ) cat_lots_count
INNER JOIN marketplace_category AS ct ON ct.id = cat_lots_count.category_id
WHERE parent_id IS null -- only root categories
)

select 
    cc.id, 
    cc.name, 
    cc.slug, 
    cc.parent_id, 
    coalesce(lots_count, 0) as lots_count
from marketplace_category cc
left join top_cats_with_l_c top on cc.id = top.id
WHERE cc.parent_id IS null
ORDER BY name
"""

CHILDREN_WITH_LOTS_COUNT = """WITH RECURSIVE

flat_categories (id, flat_id, parent_id) AS
(
  SELECT id, id, parent_id
    FROM marketplace_category
  UNION ALL
  SELECT c.id, ft.flat_id, c.parent_id
    FROM marketplace_category c
    INNER JOIN flat_categories ft ON c.id = ft.parent_id
),

children_cats_with_l_c (id, parent_id, lots_count) AS
(
SELECT id, parent_id, cat_lots_count.count AS lots_count
FROM
  (
    SELECT
      flat_ac.category_id, COUNT(*) AS count
    FROM
      (
        SELECT fc.id AS category_id
        FROM flat_categories fc
        left JOIN marketplace_lot ll ON fc.flat_id = ll.category_id
        WHERE ll.is_active = true -- only active lots
      ) AS flat_ac
    GROUP BY flat_ac.category_id
  ) cat_lots_count
INNER JOIN marketplace_category AS ct ON ct.id = cat_lots_count.category_id
WHERE parent_id = %(parent_id)s
)

select 
    cc.id, 
    cc.name,
    cc.parent_id, 
    cc.slug, 
    coalesce(lots_count, 0) as lots_count
from marketplace_category cc
left join children_cats_with_l_c children on cc.id = children.id
WHERE cc.parent_id = %(parent_id)s
ORDER BY name
"""
