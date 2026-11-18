-- Her gece 04:17'de (UTC) iki günden eski odaları siler.
-- players, game_state, played_cards ve role_actions satırları rooms'a "on delete cascade" bağlı olduğu için birlikte gider.
create extension if not exists pg_cron;
select cron.unschedule(jobid) from cron.job where jobname = 'tsim-cleanup-rooms';
select cron.schedule('tsim-cleanup-rooms', '17 4 * * *',
  $$delete from public.rooms where created_at < now() - interval '2 days'$$);
