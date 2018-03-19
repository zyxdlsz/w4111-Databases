select a.*, countries.id as country_id, countries.continent_id, countries.continent_label, countries.country_id, countries.country_label
from
	(SELECT
		dates.id as date_id, dates.date_year, dates.date_quarter, dates.date_month, dates.date_week, dates.date_day,
        webvisits.date_id, webvisits.country_id, webvisits.browser, webvisits.source_id, webvisits.newsletter, webvisits.pageviews
	FROM
		webvisits
	JOIN
		dates
	dates on webvisits.date_id = dates.id) as a
join
	countries on a.country_id = countries.id;