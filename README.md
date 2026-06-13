# Bulldog Garage — Hemet High School Automotive Technology

A complete, modern rebuild of the CTE Automotive Technology program website. Hosted on **Vercel** (site pages) + **Cloudflare R2** (training videos) for speed, reliability, and zero ongoing cost.

**Live at:** (your Vercel URL here — e.g., `bulldog-garage.vercel.app`)

---

## Quick Start for Deployment

### 1. Connect this repo to Vercel
1. Go to **vercel.com**
2. Click "New Project" and import this GitHub repository
3. Accept the defaults (Vercel auto-detects it as static)
4. Deploy — your site goes live in ~30 seconds

### 2. Set up videos on Cloudflare R2
See **[DEPLOYMENT.md](DEPLOYMENT.md)** for step-by-step R2 setup (takes ~5 minutes).

Then update `player.html` with your R2 public URL and redeploy.

**That's it.** The site is live and all quizzes and videos work.

---

## What's Inside

**On this GitHub repo (Vercel):**
- 24 curriculum pages (homepage, six AST courses, resources, etc.)
- All PDFs, PowerPoints, and lab handouts
- Interactive quizzes (Flash via Ruffle emulator)
- Full CSS/JS design system

**On Cloudflare R2 (separate, free):**
- 141 training videos (~2.9 GB) — streamed with zero egress fees

---

## Key Features

✅ **Quizzes work.** All 85+ Flash quizzes (including recovered Safety Tests) run through the bundled Ruffle emulator. Hosting on Vercel fixes the browser security restriction.

✅ **Videos stream smoothly.** Cloudflare R2 has zero egress fees, so unlimited streaming costs you nothing.

✅ **Mobile-friendly.** Responsive design works on Chromebooks, phones, and tablets.

✅ **Zero ongoing cost.** Free Vercel tier + free Cloudflare R2 tier = $0/month for a classroom.

✅ **Easy to update.** Edit files in this repo, push, and Vercel redeploys in ~30 seconds.

---

## File Structure

```
.
├── index.html                    # Homepage
├── intro.html, electrical.html   # Six AST course boards
├── contact.html, start-server.html
├── player.html                   # Video player (redirects to R2)
├── quiz.html                     # Flash quiz player (Ruffle)
├── vercel.json                   # Vercel deployment config
├── assets/                       # CSS, JS, fonts, Ruffle engine
├── powerpoints/                  # All PPT files
├── labs/, worksheets/, etc.      # Curriculum assets
├── assessments/                  # All quizzes (SWFs + iSpring HTML5)
├── DEPLOYMENT.md                 # R2 + Vercel setup guide
└── README.md                     # This file
```

(Videos are stored in Cloudflare R2, not in this repo.)

---

## Editing the Site

### Add a new page or curriculum board
1. Create a new `.html` file (or copy an existing board like `electrical.html`)
2. Update the nav links in other pages to point to it
3. Push to GitHub — Vercel redeploys automatically

### Update contact info
- Edit `contact.html` and the footer in every page

### Change colors, fonts, or spacing
- Edit `assets/css/main.css`
- CSS variables at the top control the theme

---

## Quizzes — How They Work

**Flash quizzes:** Stored as `.swf` files in `assessments/`. The player (`quiz.html`) uses the bundled Ruffle engine to run them. Ruffle is JavaScript-based and requires a web server (hence Vercel). Works on every browser, including Chromebooks.

All 85+ quizzes are working. No student setup needed — they click and take the quiz.

---

## Videos — How They Stream

`player.html` detects any relative media path and rewrites it to your R2 public URL. Update the URL with your R2 bucket's public endpoint (see `DEPLOYMENT.md`).

Videos stream from R2's global CDN with zero cost. Unlimited downloads, no egress charges.

---

## Costs

| Component | Plan | Cost/month |
|-----------|------|-----------|
| **Vercel** (site) | Hobby (free) | $0 |
| **Cloudflare R2** (videos) | Free tier | $0 |
| **Total** | — | **$0** |

If you exceed 100 GB bandwidth on Vercel (unlikely for a classroom), upgrade to Pro at $20/month for 1 TB/month.

---

## Support

- **Vercel docs:** vercel.com/docs
- **Cloudflare R2 docs:** cloudflare.com/products/r2
- **Ruffle (Flash emulator):** ruffle.rs

For detailed R2 setup and deployment, see `DEPLOYMENT.md`.

---

## Maintenance

The site is static HTML — no database, no backend. Updates are as simple as editing files and pushing to GitHub.

---

**Ready?** Start at the Quick Start above, then read `DEPLOYMENT.md` for the R2 setup.
