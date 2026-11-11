# email-assets
Logo and icon images for Neem email, plus the Gmail signature generator.

## Signatures
1. Add or edit a person in `people.json` (`name`, `title`, `phone`, `email`; `phone` is optional, and can be a list for more than one number).
2. Run `python3 generate.py` (everyone) or `python3 generate.py "Name"` (one person).
3. Open `signatures/<name>.html` in a browser, click **Copy signature**, paste into Gmail
   (Settings → See all settings → General → Signature).

The signature loads its images from this repo's `main` branch, so keep the repo public and don't rename the PNGs.
