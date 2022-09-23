select distinct name,year
from authors natural join conferences
where institution='Hebrew University of Jerusalem' and subarea='vision'
intersect
select name,year
from authors natural join conferences
where institution='Hebrew University of Jerusalem' and subarea='ml'
order by name,year;
