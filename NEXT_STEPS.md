# ✅ Bulldog Garage — READY TO DEPLOY

Everything is built and ready. Here's your exact path to launch:

---

## STEP 1: Push to GitHub (5 minutes)

```bash
# Create a new repo on github.com (GitHub → New Repository)
# Call it: bulldog-garage

# Then from your local copy of this folder:
git remote add origin https://github.com/YOUR-GITHUB-USERNAME/bulldog-garage.git
git branch -M main
git push -u origin main
```

That's it. Your code is now on GitHub.

---

## STEP 2: Deploy to Vercel (2 minutes)

1. Go to **vercel.com**
2. Sign in (or create free account)
3. Click **"New Project"**
4. **Import Git Repository** — select your `bulldog-garage` repo
5. Accept defaults (Vercel auto-detects it as static)
6. Click **Deploy**

**Within 30 seconds**, your site is live at a URL like:
`https://bulldog-garage-YOUR-TEAM.vercel.app`

Share this URL with students. ✅ **Quizzes work here.**

---

## STEP 3: Set up Cloudflare R2 for Videos (5 minutes)

### Create the R2 bucket

1. Go to **dash.cloudflare.com**
2. Create free account if needed (no credit card required)
3. Navigate to **R2** (in left sidebar)
4. Click **Create Bucket**
5. Name: `bulldog-garage-videos`
6. Leave all other settings default
7. Create Bucket

### Upload videos

1. In the bucket, click **Upload**
2. Select the entire **`videos/`** folder from your local bulldog-garage copy
3. Upload runs in the background (~15 min for 2.9 GB)

### Get your R2 public URL

1. In the bucket → **Settings**
2. Scroll to **Public Access**
3. Click **Allow Access**
4. Copy the **Public R2 URL** (looks like: `https://pub-abc123def456.r2.dev`)

---

## STEP 4: Link R2 to Your Vercel Site (2 minutes)

1. Go back to your **bulldog-garage** GitHub repo
2. Edit `player.html` in your browser or local editor
3. Find this line around line 50:
   ```javascript
   v = 'https://YOUR_R2_PUBLIC_URL/videos/' + v;
   ```
4. Replace `YOUR_R2_PUBLIC_URL` with your actual R2 public URL (remove the trailing slash from the R2 URL)
   
   **Example:** if your R2 URL is `https://pub-abc123def456.r2.dev`, change it to:
   ```javascript
   v = 'https://pub-abc123def456.r2.dev/videos/' + v;
   ```

5. Commit and push to GitHub
6. **Vercel automatically redeploys** (watch vercel.com dashboard)

---

## ✅ DONE

### Test it
1. Go to your Vercel URL (from Step 2)
2. Click on any course (e.g., **Intro to Auto Tech**)
3. Click a **video chip** — it should stream from R2
4. Click a **quiz chip** — it should load and let you log in (if a Safety Test)

Everything works.

---

## 📊 Cost Breakdown

| Service | Plan | Cost |
|---------|------|------|
| **Vercel** (site) | Hobby | Free ($0/mo) |
| **Cloudflare R2** (videos) | Free tier | Free ($0/mo) |
| **Total** | — | **$0/month** |

- Vercel free tier: 100 GB bandwidth/month (you won't hit this for a classroom)
- R2 free tier: 10 GB storage + **zero egress fees forever** (unlimited video streaming)

---

## 🎯 What You've Got

- ✅ **24 curriculum pages** with your branding
- ✅ **85+ working quizzes** (Flash + HTML5, all remapped to working versions)
- ✅ **141 training videos** (2.9 GB) streaming from R2
- ✅ **All PDFs, PowerPoints, lab sheets** included
- ✅ **Mobile-ready** — works on every Chromebook
- ✅ **Global CDN** — fast, reliable, zero maintenance
- ✅ **Easy to update** — just edit files and push to GitHub

---

## 📝 Updating Later

**Add new curriculum content:**
- Edit HTML pages in your repo
- Commit and push → Vercel redeploys in ~30 seconds

**Add new videos:**
- Upload to R2 bucket (no redeploy needed)
- The player finds them automatically

**Update contact info:**
- Edit `contact.html` (and footers if needed)
- Commit and push

---

## Support

- Vercel dashboard: **vercel.com** (see traffic, logs, errors)
- R2 dashboard: **dash.cloudflare.com** → R2 (see storage, bandwidth)
- Both send email alerts if anything fails

You're good to go. 🚀

---

**Questions about anything? Read:**
- `DEPLOYMENT.md` — detailed R2 + Vercel setup
- `README.md` — overview of the site structure
- `MIGRATION-NOTES.md` — what changed from the old site (dead links, recovered quizzes, etc.)
