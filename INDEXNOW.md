# IndexNow setup

This site now uses the recommended root-key setup for IndexNow.

## What was added

- Verification key file: `https://getcosmoapp.com/947b59ae-0baf-4b2b-a6fe-3b3621828c4d.txt`
- Sitemap: `https://getcosmoapp.com/sitemap.xml`
- Submission script: `scripts/submit-indexnow.ps1`

## How to submit URLs

Dry run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\submit-indexnow.ps1 -DryRun
```

Submit all public HTML pages discovered in this repo:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\submit-indexnow.ps1
```

Submit to a different endpoint if needed:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\submit-indexnow.ps1 -Endpoint "https://www.bing.com/indexnow"
```

## Notes

- The script converts `index.html` to `/` and `es\index.html` style files to `/es/`.
- `index_deprecated.html` is excluded.
- If you add or remove public pages, rerun the script after deployment.
