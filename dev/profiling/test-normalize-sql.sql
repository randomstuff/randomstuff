select * from (select * from TEST where x in (8, 9, 10, 11));
select * from TEST where x = 1, y>2 and k is not NULL;
select * from TEST where x in (1,2,3,4);
select * from TEST where x in (1,2,3,4) and z > 0;
select * from (select * from TEST where x in (1, 2, 3, 4));
select * from (select * from TEST where x in (1, 2, 3, 9));
select * from (select * from TEST where x in (1, 2, 3,9));
