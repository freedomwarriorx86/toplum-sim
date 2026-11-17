create or replace function public.apply_card_effects(p_room uuid, p_delta jsonb, p_corruption boolean default true)
returns setof public.game_state
language sql
security invoker
set search_path = public
as $$
  update public.game_state set
    health    = least(100, greatest(0, health    + coalesce((p_delta->>'health')::int, 0))),
    education = least(100, greatest(0, education + coalesce((p_delta->>'education')::int, 0))),
    security  = least(100, greatest(0, security  + coalesce((p_delta->>'security')::int, 0))),
    transport = least(100, greatest(0, transport + coalesce((p_delta->>'transport')::int, 0))),
    social    = least(100, greatest(0, social    + coalesce((p_delta->>'social')::int, 0))),
    treasury  = treasury + coalesce((p_delta->>'treasury')::int, 0),
    businessman_cash = greatest(0, businessman_cash + coalesce((p_delta->>'businessman_cash')::int, 0)),
    suspicion = case when p_corruption
                  then least(100, greatest(0, coalesce(suspicion, 0) + coalesce((p_delta->>'suspicion')::int, 0)))
                  else suspicion end,
    updated_at = now()
  where room_id = p_room
  returning *;
$$;
grant execute on function public.apply_card_effects(uuid, jsonb, boolean) to anon, authenticated;
delete from public.players where room_id = '64ec8717-d0a6-40f3-9b04-80fec163720f';
delete from public.rooms where id = '64ec8717-d0a6-40f3-9b04-80fec163720f';
