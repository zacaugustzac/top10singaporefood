Add a restaurant to the top10singaporefood database using a Google Maps link.

Arguments format: `[dish name] | [Google Maps URL]`

Example: `char kway teow | https://www.google.com/maps/place/Meng+Kee+Fried+Kway+Teow/...`

The details are: **$ARGUMENTS**

Steps to follow:
1. Parse the dish name and URL by splitting on `|` and trimming whitespace
2. Extract the restaurant name from the URL path — it appears after `/maps/place/` before the next `/`, URL-decode the `+` signs and `%XX` sequences
3. Fetch the Google Maps URL with `curl -sL` and try to extract the address — look for Singapore postal codes (`Singapore [0-9]{6}`), street numbers, road/street/avenue/lorong/crescent patterns in the page source
4. If the address cannot be extracted from the page, ask the user to paste it
5. Read the Supabase service role key from `.env` (key is `SUPABASE_SERVICE_KEY`)
6. Look up `category_id` from the `dishes` table using `ilike` on the dish name
7. Check if a restaurant with the same name already exists for that `category_id` — if yes, tell the user and stop
8. Insert into `restaurants` with `category_id`, `name`, and `address`
9. Run `python scripts/generate-static.py` to regenerate static pages
10. Stage the affected dish HTML and `sitemap.xml`, pull --rebase, commit, and push
11. Confirm what was added and the live URL
