-- lists all bands with Glam rock as their main style, ranked by longevity
-- Requirements:
-- Import this table dump: metal_bands.sql.zip
-- Column names must be: band_name and lifespan (in years)
-- You should use attributes formed and split for computing the lifespan
-- Your script can be executed on any database

SELECT band_name, (YEAR(split)-YEAR(formed)) AS lifespan
	FROM metal_bands
	WHERE main_style = 'Glam rock'
	ORDER BY lifespan DESC;
