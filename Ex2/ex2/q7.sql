select distinct a.year, a.name
from authors a
where a.year <= 2020 and a.year >= 2000 and a.conference = 'focs' and a.institution = 'Hebrew University of Jerusalem' and not exists (
    select a1.year, a1.name
    from authors a1
    where a1.year = a.year and a1.institution = a.institution and a1.conference = a.conference and a1.count > a.count)
order by a.year, a.name;