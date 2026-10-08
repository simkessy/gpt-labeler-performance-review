# GPT Labeler performance review

Live site: https://simkessy.github.io/gpt-labeler-performance-review/

Open index.html in any browser. No build step or external assets are required.

Includes an executive summary with memory recommendations and sample lineage, an expandable current process map with recovered September sampling timings, resource measurements, assumed savings, and an overlaid proposed workflow. Estimated savings are unverified; delivery estimates and the pilot checklist are omitted.

The original memory and worker-count data is preserved.

The workflow diagram source is included as workflow-overlay.py. Regenerate the standalone SVG with `uv run workflow-overlay.py --output workflow-overlay.svg`. The page embeds its own copy of the SVG.

September sampling breakdown: 57 min to the last output event, 4h32 to the source cost-row event, and 1h06 through estimation and approval handling, across 1,476 parent links to 1,458 recently created samples. These are elapsed intervals, not isolated model-call duration. Source links are included in the report.
