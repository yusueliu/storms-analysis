select 
	distinct locations."EVENT_ID",
	locations."EPISODE_ID",
	locations."YEARMONTH",
	events."EVENT_TYPE",
	--events."TOR_F_SCALE",
	events."YEAR",
	events."MONTH_NAME",
	events."DAMAGE_PROPERTY",
	locations."LOCATION",
	events."STATE",
	locations."LONGITUDE",
	locations."LATITUDE"
from events
inner join locations
on events."EVENT_ID" = locations."EVENT_ID" and events."EPISODE_ID"=locations."EPISODE_ID"
where 
	events."EVENT_TYPE" = 'Tornado'
	and events."YEAR" = '2006'
	
order by 
	events."EVENT_TYPE" desc;
