# GPT Labeler performance review

Live site: https://simkessy.github.io/gpt-labeler-performance-review/

Open index.html in any browser. No build step or external assets are required.

Includes an executive summary with memory recommendations and sample lineage, current-workflow views, resource measurements, static savings estimates, and an overlaid proposed workflow. Estimated savings are unverified; delivery estimates and the pilot checklist are omitted.

The original memory and worker-count data is preserved.

The workflow diagram source is included as workflow-overlay.py. Regenerate the standalone SVG with `uv run workflow-overlay.py --output workflow-overlay.svg`. The page embeds its own copy of the SVG.
