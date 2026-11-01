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

## Expanded profile research and validation — 2026-11-01

The revised README restores visible 3D contributions, the contribution snake, recent activity, full analytics, social badges, a fuller toolbox and a code-style biography. Six featured project cards link to source and available demos; additional projects and domain navigation use native expandable sections. Existing private repository information is not added to the public profile.

GitHub sanitizes scripts, inline styles and classes out of README HTML, so interaction uses anchor links, clickable images, `details` sections, theme-aware `picture` elements and the existing interactive portfolio. The orbital illustration is an animated SVG with fixed readable text, a shaded globe, isometric cubes and slow decorative orbital motion. CSS transform animation uses linear 24/32-second orbits and a 6-second floating cycle; reduced-motion preferences remove movement. The local typing SVG has a 24-second cycle and a static reduced-motion state. No new package dependencies were added.

The typing and streak hosted endpoints returned HTTP 403 during this session. Typing is therefore a repository-owned SVG; the streak card is generated daily using GitHub GraphQL and `scripts/render_streak.py`. Streaks cover the last 365 calendar days, use UTC and allow today to be unfinished. The longest streak is explicitly limited to that window. The script includes checks for empty, broken and ongoing streaks. Standard badges and skill icons still use their existing external image services.

Sources consulted:

- [GitHub markup sanitization](https://github.com/github/markup)
- [Typing SVG options and local-hosting guidance](https://github.com/DenverCoder1/readme-typing-svg)
- [3D contributions: separate light/dark configurations](https://github.com/yoshi389111/github-profile-3d-contrib/blob/main/EXAMPLES.md)
- [Contribution snake output and theme support](https://github.com/Platane/snk)
- [Summary cards: stats, sequence animation and duration](https://github.com/vn7n24fzkq/github-profile-summary-cards)
- [Streak stats behavior and appearance options](https://github.com/DenverCoder1/github-readme-streak-stats)

DP exported to `C:\Users\Lohith k\Downloads\Loktrishal-Galaxy-DP.jpg` (500 × 500, 100,140 bytes). The account DP will be uploaded by the user.

### Portrait crop prompt (built-in imagegen)

Use case: precise-object-edit. This is a CROP AND PADDING adjustment only of the provided portrait. Keep all photographic pixels, identity, face, expression, hair, lighting, black suit and white shirt visually identical; do not beautify, redraw or change facial details. Tighten framing by removing approximately the bottom 20 percent of the photograph (excess lower torso), retaining head and upper chest, then make a square professional headshot composition with balanced clean white padding around the sides, a small comfortable white space above hair, subject centered. Background remains plain pure white. No effects, dots, border, caption or watermark. Final 1:1 square suited to a README profile card. The goal is less empty lower torso and better padding, not a different photo.

Validation: GitHub's Markdown API retains the image assets, project tables and four native expandable sections. Playwright checks passed for 390px mobile horizontal overflow and opening/closing a details section. The local orbit SVG runs three CSS animations; emulating reduced motion leaves zero active animations. Desktop and mobile previews were visually inspected. XML parsing and portrait square dimensions passed. Streak calculation self-checks passed, followed by a successful live GitHub contribution query.
