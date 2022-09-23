select distinct institution,name
from authors natural join institutions
where country='il'
order by institution,name ;
