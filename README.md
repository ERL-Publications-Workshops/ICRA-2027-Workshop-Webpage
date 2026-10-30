# ICRA 2027 Underwater Robotics Workshop

A static, review-stage workshop website for **Dronification of Underwater Robotics: Accessible Manipulation with Small-Scale Platforms**.

## Preview

Open `index.html` directly, or serve this folder with:

```sh
python -m http.server 8080 --bind 127.0.0.1
```

Then visit <http://127.0.0.1:8080>. No build step or dependency installation is required.

## Editing

- `index.html`: workshop overview, programme, speakers and organizers.
- `call-for-papers.html`: the planned contribution format, topics and submission status.
- `sponsors-institutions.html`: institutions represented by organizers and speakers, plus sponsorship enquiries.
- `styles.css`: responsive layout and both ocean-inspired color palettes.
- `theme.js`: applies the saved preference before first paint.
- `app.js`: theme selection, mobile navigation and active section tracking.
- `assets/`: self-hosted images, fonts and favicon. `portrait-sources.json` records the portrait sources.

Each page has its own title, main heading and navigation state. Header, footer and theme-control markup are present in each HTML file so the entire site works without a build step. Keep that shared markup consistent when editing. All page and asset links are relative for GitHub Pages repository hosting.

The theme control offers direct **Light**, **Dark** and **Use device setting** buttons. The sun, moon and monitor icons select the mode in one click. Keyboard arrow keys move between modes. The preference persists across reloads and stays synchronized between tabs. All core content and links remain available without JavaScript. Motion respects the system preference for reduced motion.

## GitHub Pages

This directory is ready for branch-based GitHub Pages hosting from the repository root. All internal asset paths are relative, so the repository URL prefix works. `.nojekyll` disables unnecessary processing. No hosting settings have been changed by this draft.

Before public release, review the workshop title, acceptance status, date, location, agenda and portraits. The page currently carries a review-only banner and `noindex, nofollow` metadata. These indicate draft status and do not make a published page private.

## Content and image sources

Content follows the supplied workshop proposal and the 30 October 2026 meeting. The morning timetable is tentative. The three named speakers are listed as confirmed in that proposal. The industry slot remains pending. Portraits are present for all three speakers and seven organizers. Moritz Graf's initials remain until a verified portrait is available.

The Call for Papers section describes the planned two-page abstracts and presentation formats. Submissions are not open, and dates and review rules remain unconfirmed. The Sponsors section accepts enquiries through the primary contact; no sponsors, prices or benefits are claimed.

The hero shows a **work-class ROV**, identified in its caption as context for underwater intervention. It does not depict the proposed small-scale challenge platform. The photograph was donated to the public domain by Oceaneering's Duncan McLean and uploaded by Frank van Mierlo: [source and rights](https://commons.wikimedia.org/wiki/File:ROV_working_on_a_subsea_structure.jpg).

Draft portraits were sourced from public professional profiles, as discussed for the review-stage site. Their rights remain with the respective owners. The repository's CC0 license does not relicense these third-party images.

| File | Source |
| --- | --- |
| `corina-barbalata.png` | [LSU faculty profile](https://www.lsu.edu/eng/mie/people/faculty/barbalata.php) |
| `marco-tognon.jpg` | [Marco Tognon's research website](https://marco-tognon-robotics.com/) |
| `stefan-sosnowski.webp` | [TUM ITR profile](https://www.ce.cit.tum.de/en/itr/sosnowski/) |
| `daniel-duecker.jpg` | [HippoCampus Robotics team](https://hippocampusrobotics.github.io/people/) |
| `pawel-ladosz.jpg` | [CRADLE team](https://cradlerobotics.co.uk/about/team/) |
| `nathalie-bauschmann.jpg` | [TU Hamburg profile](https://www.tuhh.de/mum/team/wimi/nathalie-bauschmann) |
| `giancarlo-troni.jpg` | [MBARI annual report](https://annualreport.mbari.org/2023/) |
| `seyonne-leslie-dalley.png` | [Seyonne's research website](https://sladalley.github.io/) |
| `alp-ortakci.jpg` | [Alp's personal website](https://www.alportakci.com/) |
| `michele-grimaldi.png` | [Ignacio Carlucho's group page](https://ignaciocarlucho.github.io/People/) |

Manrope and Space Grotesk are self-hosted under the SIL Open Font License. Their license texts are included beside the font files. No analytics, external font services, cookies or third-party scripts are included. Local storage contains only the color-theme preference.
