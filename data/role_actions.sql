-- Rol yetkileri: her oyuncu rolünün eylem puanını (EP) özel aksiyonlara harcar.
-- Etkiler apply_card_effects ile uygulanır; bu tablo yalnızca kaydı ve harcanan EP'yi tutar.
create table if not exists public.role_actions (
  id uuid primary key default gen_random_uuid(),
  room_id uuid not null references public.rooms(id) on delete cascade,
  player_id uuid not null references public.players(id) on delete cascade,
  action text not null,
  cost int not null check (cost between 1 and 3),
  created_at timestamptz not null default now()
);
create index if not exists role_actions_room_idx on public.role_actions(room_id);

alter table public.role_actions enable row level security;
-- Prototip: diğer tablolar gibi herkese açık
drop policy if exists "role_actions open select" on public.role_actions;
drop policy if exists "role_actions open insert" on public.role_actions;
create policy "role_actions open select" on public.role_actions for select to anon, authenticated using (true);
create policy "role_actions open insert" on public.role_actions for insert to anon, authenticated with check (true);
grant select, insert on public.role_actions to anon, authenticated;

do $$ begin
  alter publication supabase_realtime add table public.role_actions;
exception when duplicate_object then null; end $$;
