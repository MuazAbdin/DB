select distinct a.name
from authors a
where not exists (
    select a1.conference
    from authors a1 natural join conferences
    where a1.name = 'Noam Nisan' and area = 'ai'
    except
    select a2.conference
    from authors a2 natural join conferences
    where a2.name = a.name
    )
order by a.name;