-- niah_prospects: Niah outreach pipeline, mirror of pisco_prospects (Placewell).
-- Applied to project dprdnrgjkzgfgtcsguuq (neurodashboards) on 2026-08-10.
create table if not exists public.niah_prospects (
  id uuid primary key default gen_random_uuid(),
  country text,
  tier integer,
  sector text,
  company text,
  website text,
  decision_maker text,
  dm_role text,
  email text,
  email_status text,
  linkedin text,
  whatsapp text,
  phone text,
  source_url text,
  confidence text,
  status text default 'new',
  gate_notes text,
  notes text,
  researched_by text,
  outreach_message text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);
comment on table public.niah_prospects is 'Niah outreach pipeline (event organizers, venues, agencies). Mirrors pisco_prospects; drained by niah-writer / niah-sender edge functions.';
alter table public.niah_prospects enable row level security;
