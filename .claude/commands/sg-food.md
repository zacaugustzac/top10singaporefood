Generate SQL to insert the top 10 **$ARGUMENTS** restaurants in Singapore into the `restaurants` table.

Rules:
- Use a subquery to resolve `category_id` from the `dishes` table by matching the food name — do not hardcode the id
- Do not specify `id` — let the sequence auto-continue
- Include `name` and `address` columns only
- Use `(VALUES ...)` with 10 rows
- Escape any single quotes inside strings by doubling them (e.g. `Zheng''s`)
- Add a note at the end reminding the user to verify addresses before running

The food is: **$ARGUMENTS**
