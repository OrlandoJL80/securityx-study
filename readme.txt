CompTIA SecurityX (CAS-005) private study deck
482 practice items. Closed study group only.

NOT CompTIA official exam content. Licensed practice-bank items.
Do not publish this repo, the live URL, question text, or answers.

--------------------------------
GROUP (no setup)
--------------------------------
Open the link Orlando sends.
Pick your name. Enter PIN CAS005.
Orlando, Scott, Daniel, Donald, Leslie, Jaye, Kelly, Albert, Johnny, Mark, Kevin, Andy.
The home screen should say saved to Supabase.

--------------------------------
ONE-TIME SUPABASE SETUP (Orlando)
--------------------------------
1. Create a free project at https://supabase.com
2. SQL Editor → New query → paste supabase/schema.sql → Run
3. Project Settings → API
   Copy the project URL and the anon public key.
   Do not copy the service_role key.
4. Paste both into supabase-config.js:
   window.SUPABASE = { url: "https://YOURPROJECT.supabase.co", anonKey: "YOUR_ANON_KEY" };
5. Host this folder privately (Cloudflare Pages + Access, or another private host).
   Do not enable public GitHub Pages. The PIN does not hide questions-data.js.
6. Send the private link. Send the PIN separately if you want.

Until step 4 is done, progress stays in that browser only.
python server.py is no longer required.
