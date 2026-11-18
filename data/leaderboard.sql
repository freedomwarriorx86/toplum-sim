-- Liderlik tablosu: her bitmiş oyunda her oyuncu için bir satır.
-- rooms'a bağlı DEĞİL: gece temizliği odaları silse de sonuçlar kalır.
create table if not exists public.game_results (
  id uuid primary key default gen_random_uuid(),
  room_id uuid not null,
  player_id uuid not null,
  name text not null,
  role text,
  city text,
  rounds int,
  players int,
  mission_code text,
  won boolean not null default false,
  impact numeric not null default 0,      -- kararlarının halk konforuna toplam etkisi
  best_label text,                        -- en iyi kararı
  best_impact numeric,
  badges text[] not null default '{}',    -- o oyunun "en"leri
  ep_spent int not null default 0,
  created_at timestamptz not null default now(),
  unique (room_id, player_id)
);
create index if not exists game_results_created_idx on public.game_results(created_at desc);
alter table public.game_results enable row level security;
drop policy if exists "game_results open select" on public.game_results;
drop policy if exists "game_results open insert" on public.game_results;
create policy "game_results open select" on public.game_results for select to anon, authenticated using (true);
create policy "game_results open insert" on public.game_results for insert to anon, authenticated with check (true);
grant select, insert on public.game_results to anon, authenticated;

-- Yetkiler artık tura bağlı: hangi turda kullanıldığı tutulur (EP her tur yenilenir)
alter table public.role_actions add column if not exists round int;
