-- Run once in the Supabase SQL editor.
-- Progress only. Question text stays in the study files.

create table if not exists public.study_progress (
  name text primary key,
  history jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

alter table public.study_progress enable row level security;

revoke all on table public.study_progress from anon, authenticated;

create or replace function public.load_progress(p_name text, p_pin text)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  rec jsonb;
begin
  if p_pin is distinct from 'CAS005' then
    raise exception 'denied';
  end if;
  if p_name not in (
    'Orlando', 'Scott', 'Daniel', 'Donald', 'Leslie',
    'Jaye', 'Kelly', 'Albert', 'Johnny', 'Mark', 'Kevin'
  ) then
    raise exception 'unknown account';
  end if;
  select history into rec from public.study_progress where name = p_name;
  return coalesce(rec, '{}'::jsonb);
end;
$$;

create or replace function public.save_progress(p_name text, p_pin text, p_history jsonb)
returns void
language plpgsql
security definer
set search_path = public
as $$
begin
  if p_pin is distinct from 'CAS005' then
    raise exception 'denied';
  end if;
  if p_name not in (
    'Orlando', 'Scott', 'Daniel', 'Donald', 'Leslie',
    'Jaye', 'Kelly', 'Albert', 'Johnny', 'Mark', 'Kevin'
  ) then
    raise exception 'unknown account';
  end if;
  insert into public.study_progress (name, history, updated_at)
  values (p_name, coalesce(p_history, '{}'::jsonb), now())
  on conflict (name) do update
    set history = excluded.history,
        updated_at = now();
end;
$$;

revoke all on function public.load_progress(text, text) from public;
revoke all on function public.save_progress(text, text, jsonb) from public;
grant execute on function public.load_progress(text, text) to anon, authenticated;
grant execute on function public.save_progress(text, text, jsonb) to anon, authenticated;
