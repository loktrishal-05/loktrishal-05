# Starlight profile assets

Created with the built-in imagegen tool. Original generated files are retained outside the repository; the consumed assets live here. The galaxy artwork is an artistic interpretation, not scientific imaging.

## Portrait edit prompt

Use case: identity-preserve. Edit this professional portrait. Change only the background and purple lighting: replace entire purple dotted space background with pure seamless white #FFFFFF, remove every purple halo, purple rim light and violet cast from hair and jacket. Keep EXACT same face identity, facial features, natural skin texture, expression, gaze, hairstyle, black jacket, white shirt, pose and framing unchanged. Natural neutral studio lighting, realistic edges, clean professional headshot, no dots, no decorations, no text. Maintain portrait 4:5 composition and high resolution.

## Galaxy avatar prompt

Use case: style-transfer. Input: reference screenshot of a glowing white spiral galaxy. Create a refined cinematic square GitHub avatar inspired by this image. Deep pure black space, centered face-on Milky Way-like spiral galaxy fully inside a circular safe area occupying 75% of square. Brilliant luminous WHITE central core, elegant clearly separated curved spiral arms made of thousands of tiny sparkling white stars and silvery dust, subtle ice-blue highlights, a few bright pin-sharp diffraction sparkles, airy dark gaps. Strong visual sense of clockwise swirling rotation, not a literal motion blur. More rich star detail and depth than reference, sophisticated photorealistic astrophotography blended with crisp particle art. Dominantly glowing WHITE on BLACK, no purple, no text, no icons, no frame, no screenshot borders. Symmetric square 1024x1024 with dark corners suitable for circular profile crop.

## Hero prompt

Create a finished ultra-wide cinematic GitHub profile hero banner, 3:1 aspect ratio approximately 1536x512. Premium editorial design for Loktrishal K, AI and full stack engineer. Near black charcoal #0B1018 space background. Right half: stunning luminous WHITE spiral galaxy seen obliquely, silver stardust, subtle ice blue star highlights, elegant orbital light arcs, refined cinematic depth. Left half: generous quiet negative space with beautifully typeset clear typography, text exactly 'LOKTRISHAL K' in large white modern sans serif, and below in smaller tracked pale silver type 'AI / DATA SCIENCE / FULL STACK'. A short hairline of ice blue above the name. All text within central 85% of image; type large enough to read in a GitHub README. Restrained, confident, polished, premium, masterful composition. Glowing white is dominant accent; no purple, no neon rainbow, no logos, no extra words, no fake interface panels, no watermark. Galaxy and stardust must not interfere with name. Flat rectangular image no rounded mockup frame.

## Exports

`python scripts/render_galaxy.py` creates `galaxy-avatar.jpg` (500 × 500, under 1 MB) and `galaxy-spin.gif` (120 frames, 12-second seamless clockwise loop) from `galaxy.png`. Requires Pillow. The JPEG is the upload-ready account avatar; the GIF is used in the README. Account avatar changes require a separate upload in GitHub profile settings and are not applied by a git push.

## Sources

- [GitHub profile picture requirements](https://docs.github.com/en/account-and-profile/reference/profile-reference)
- [GitHub profile update API fields](https://docs.github.com/en/rest/users/users#update-the-authenticated-user)
- [Summary card themes and workflow options](https://github.com/vn7n24fzkq/github-profile-summary-cards)
- Project descriptions were checked against each linked public repository README on 2026-11-01.

