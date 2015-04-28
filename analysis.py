from sqlalchemy import *
from schema import *
import sys


conn = engine.connect()

last_changes = select([ranks.c.race_id, ranks.c.player, func.max(ranks.c.timestamp).label('last_change')]) \
        .group_by(ranks.c.race_id, ranks.c.player).alias()



#last_race = select([func.max(races.c.id)]).where(and_( \
#                                                      races.c.set_id == bindparam('set_id') \
#                                                      func.exists())

standings = select([ranks.c.race_id, ranks.c.player, ranks.c.rank, ranks.c.timestamp]).select_from(ranks.join(last_changes, \
                            and_( \
                                 ranks.c.race_id == last_changes.c.race_id, \
                                 ranks.c.player == last_changes.c.player, \
                                 ranks.c.timestamp == last_changes.c.last_change \
                                 ) \
                            )).alias()
#print last_race
#last_race_rank = select([races.set_id, 

other = select([ranks.c.race_id, ranks.c.player, ranks.c.rank]) \
    .select_from(standings)

winners = select([standings.c.race_id, standings.c.player, standings.c.rank, standings.c.timestamp]).select_from(standings).alias()

race_times = select([(laps.c.timestamp + laps.c.elapsed).label('race_length'), laps.c.player, laps.c.race_id]).where(laps.c.lap==3).alias()

rank_changes = select([winners.c.rank, ranks.c.rank, (ranks.c.timestamp / race_times.c.race_length).label('perc_thru')]) \
    .select_from(winners \
                 .join(ranks, \
                              and_( winners.c.race_id == ranks.c.race_id, \
                                   ranks.c.player == winners.c.player \
                                   )) \
                 .join(race_times, \
                       and_( \
                            race_times.c.race_id == winners.c.race_id,
                            race_times.c.player == winners.c.player))) 

last_rank_changes = select([standings.c.rank, (standings.c.timestamp / race_times.c.race_length)]) \
    .select_from(standings \
                 .join(race_times, \
                       and_( \
                            race_times.c.race_id == standings.c.race_id,
                            race_times.c.player == standings.c.player))) 

time_in_rank = select([(func.sum(ranks.c.elapsed) / race_times.c.race_length).label("time_in_rank"), ranks.c.rank.label("current_rank"), standings.c.rank.label("final_rank"), ranks.c.race_id]) \
    .select_from(standings \
                 .join(ranks, \
                       and_( \
                            ranks.c.race_id == standings.c.race_id, \
                            ranks.c.player == standings.c.player)) \
                 .join(race_times, \
                       and_( \
                            race_times.c.race_id == standings.c.race_id, \
                            race_times.c.player == standings.c.player \
                       ))).group_by(standings.c.race_id, standings.c.rank, ranks.c.rank).alias()

avg_tim_in_rank = select([func.avg(time_in_rank.c.time_in_rank), time_in_rank.c.current_rank, time_in_rank.c.final_rank]) \
    .group_by(time_in_rank.c.current_rank, time_in_rank.c.final_rank)



from collections import defaultdict

results = conn.execute(avg_tim_in_rank).fetchall()
#print results
#print last_rank_changes
#sys.exit()

d = [[None] * 4 for i in range(4)]
#print len(results)
for result in results:
    time, current, final = result
    d[final - 1][current - 1] = time

for row in d:
    print ", ".join(map(str, row))


    #print ", ".join(map(str, result))
    #cells = ["#N/A"] * 4
    #cells[final-1] = current
    #print ", ".join(map(str, [ts] + cells))


#print d
#for key, vals in d.items():
#    print ", ".join(map(str, [key] + vals))

#    print ", ".join(map(str, result))
#print results
