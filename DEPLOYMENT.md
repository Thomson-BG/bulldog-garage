# Deployment Guide — Bulldog Garage

This site is split across two platforms for optimal performance and cost:

## Vercel (HTML, CSS, JS, PDFs, PowerPoints)

The site pages, assets, and static files are hosted on Vercel. This folder contains everything except videos.

**To deploy:**
1. Create a GitHub repository with this folder's contents
2. Go to vercel.com and click "New Project"
3. Import the GitHub repo
4. Vercel auto-detects it as a static site (no build step needed)
5. Deploy — done. The site goes live immediately.

Vercel handles all caching, CDN distribution, and HTTPS automatically.

---

## Cloudflare R2 (Training Videos)

The 141 training videos (2.9 GB) live in Cloudflare R2 for zero-cost unlimited streaming.

### Set up R2 (one-time, ~5 minutes)

1. **Create a Cloudflare R2 bucket**
   - Go to dash.cloudflare.com (create free account if needed)
   - Navigate to R2 → Create bucket
   - Name: `bulldog-garage-videos`
   - Leave all other settings default

2. **Upload the videos**
   - In the bucket, click "Upload" and select the `videos/` folder
   - Uploads run in the background; 2.9 GB takes ~15 minutes depending on your connection

3. **Make the bucket public**
   - Click on the bucket → Settings
   - Scroll to "Public access" and enable it
   - Click "Allow access"
   - You'll get a **Public R2 URL** (looks like `https://pub-abc123def456.r2.dev`)
   - Copy this URL

4. **Update player.html in Vercel**
   - In the repo, edit `player.html`
   - The player rewrites any relative media path to your R2 public URL
   - Replace the placeholder public URL in `player.html` with the one you copied (without the trailing slash)
   - Commit and push. Vercel redeploys automatically.

That's it. Videos now stream from R2 at zero cost, no matter how many students watch them.

---

## Cost Breakdown

- **Vercel (free tier):** $0/month. Includes 100 GB bandwidth/month, more than enough for the interactive content. If you need more, upgrade to Pro ($20/month) for 1 TB bandwidth.
- **Cloudflare R2 (free tier):** $0/month. Includes 10 GB storage (your 2.9 GB fits free), and **zero egress fees forever** — unlimited streaming, no extra cost.
- **Total: $0/month** (or $20/month on Vercel Pro if you scale beyond free limits, which is unlikely for a classroom).

---

## Testing

Once both are live:
1. Open the Vercel site in a browser
2. Navigate to any board page with videos (e.g., Intro to Auto Tech)
3. Click a video chip — the player should load and stream smoothly from R2
4. Check that quizzes work — all Flash quizzes run through Ruffle (fixed by hosting on Vercel)

---

## Updating Videos Later

If you need to add or replace videos:
1. Upload them to the R2 bucket (same "Upload" button)
2. The site automatically sees the new files — no redeployment needed

If you update board pages or add new curriculum content:
1. Edit the files in the GitHub repo
2. Commit and push
3. Vercel redeploys in ~30 seconds

---

## Support & Monitoring

- **Vercel dashboard:** vercel.com → select your project → see real-time traffic, analytics, and logs
- **R2 dashboard:** dash.cloudflare.com → R2 → select bucket → see storage usage and bandwidth stats
- Both have email alerts if anything goes wrong

---

## Questions?

- Vercel docs: vercel.com/docs
- Cloudflare R2 docs: cloudflare.com/developer-platform/products/r2/
- Player.html video loading: look at the script at the bottom of player.html — it redirects `videos/` paths to R2
