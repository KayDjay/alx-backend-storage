-- SQL script that lists all bands with Glam rock, ranked by their longevity
SELECT band_name,
	CASE
        	WHEN split IS NULL THEN (2022 - formed)
        	ELSE (split - formed)
    	END as lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC
;