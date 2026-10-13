# DoF · Embodied AI

A bilingual educational library for embodied AI, robotics papers and practical research concepts.

- **Website:** [https://dld0621.github.io/DoF/](https://dld0621.github.io/DoF/)
- **Dexterous retargeting course:** [https://dld0621.github.io/DoF/retargeting/](https://dld0621.github.io/DoF/retargeting/)
- **Research map:** [DoF Embodied AI Paper Analysis](https://github.com/Dld0621/Embodied-AI-Paper-Analysis)

The static site contains 41 library entries, references to 52 videos, and a six-chapter retargeting course with 28 method profiles and interactive teaching experiments. Chinese and English can be switched in the interface. Original figures and author demonstrations retain their source citations; the teaching experiments are illustrations, not independent benchmark results.

## Hosting

GitHub Pages serves this repository from the `main` branch, root directory. `.nojekyll` preserves the static files. No Node installation, server, Worker, API key, or build action is needed to serve it.

Video files are intentionally not stored in this repository. Playback keeps using the existing public media endpoint at `https://dof-embodied-ai.steven12123.chatgpt.site/media/`. This preserves the full video library without duplicating large video files in Git. That media service must remain available for playback; the Pages site is a static frontend, not a migration of video storage.

## Updating the static export

Use a fresh static `public` source directory, then export to a separate destination:

```sh
python3 scripts/build-pages.py --source ./source-public --output ./pages-output --repo-base /DoF/ --site-origin https://dld0621.github.io
```

Review the export manifest and test the project path before replacing the published repository contents. The exporter changes internal links and media URLs, preserves image bytes, checks local resource targets, and refuses detected local filesystem paths or credential patterns. It does not publish or push anything.

## Attribution

Paper figures, quoted research findings, third-party demonstrations and linked media remain subject to their respective authors' terms. This repository does not grant a new license to third-party material or claim author endorsement. See the source links accompanying each item. Narration is AI-generated; videos identify the music and research sources used.
