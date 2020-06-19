
select player_id, player_name_id, count(*) matches, count(distinct m.event_id) eventos
from player p 
inner join match m
on m.winner_player_1 = p.player_id or m.winner_player_2 = p.player_id or m.looser_player_1 = p.player_id or m.looser_player_1 = p.player_id
where p.player_name_id like '%known%'
group by player_id

/*
 player_id |    player_name_id     | matches | eventos 
-----------+-----------------------+---------+---------
 a240      | unknown-unknown       |       2 |       1
 bc49      | unknown-bahr          |       1 |       1
 br40      | unknown-bassett       |       1 |       1
 br41      | unknown-briggs        |       1 |       1
 cl30      | unknown-cory          |       2 |       1
 d246      | unknown-unknown       |       2 |       1
 de40      | unknown-dry           |       1 |       1
 de89      | unknown-de-klazkowski |       1 |       1
 e950      | unknown-espanol       |       1 |       1
 f548      | unknown-futternecht   |       1 |       1
 f549      | unknown-friscic       |       1 |       1
 fb11      | unknown-fairbridge    |       1 |       1
 fb12      | unknown-forsaith      |       1 |       1
 fb40      | unknown-ferrier       |       1 |       1
 gh65      | unknown-gaston        |       3 |       1
 h738      | unknown-hamza         |       1 |       1
 hc30      | unknown-hamilton      |       1 |       1
 he47      | unknown-hatterley     |       1 |       1
 he79      | unknown-holliday      |       1 |       1
 he80      | unknown-henville      |       3 |       1
 k796      | unknown-kreuzhuber    |       1 |       1
 k797      | unknown-kolik         |       1 |       1
 kg83      | unknown-krishen       |       1 |       1
 l776      | unknown-lockington    |       2 |       1
 lg30      | unknown-linwood       |       2 |       1
 md79      | unknown-markoff       |       1 |       1
 mp69      | unknown-michod        |       1 |       1
 mr51      | unknown-matthews      |       2 |       1
 mt07      | unknown-mcgibbon      |       1 |       1
 n848      | unknown-nydis         |       1 |       1
 n888      | unknown-nelson        |       1 |       1
 o283      | unknown-ostroff       |       1 |       1
 o590      | unknown-olivares      |       3 |       1
 pk04      | unknown-pawsey        |       1 |       1
 ss11      | unknown-stebler       |       1 |       1
 sv05      | unknown-siedoff       |       2 |       2
 sv50      | unknown-sturm         |       1 |       1
 tf17      | unknown-turner        |       1 |       1
 u073      | unknown-unknown3      |       4 |       4
 u074      | unknown-unknown4      |       4 |       3
 u075      | unknown-unknown5      |       1 |       1
 u076      | unknown-unknown6      |       1 |       1
 u077      | unknown-unknown7      |       1 |       1
 u078      | unknown-unknown8      |       1 |       1
 u079      | unknown-unknown9      |       1 |       1
 u998      | unknown-unknown2      |       4 |       4
 u999      | unknown-unknown1      |       5 |       5
 w752      | unknown-warfield      |       1 |       1
 w977      | unknown-wormall       |       1 |       1
 z201      | unknown-zollner       |       1 |       1
(50 rows)
*/
