from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List
import html


@dataclass
class ProfileData:
    username: str
    name: str
    title: str
    location: str
    education: str
    languages_programming: List[str]
    libraries_tools: List[str]
    interests: List[str]
    email: str
    linkedin: str
    github: str
    stats: dict


ASCII_ART = r'''
           .--.
          |o_o |
          |:_/ |
         //   \ \
        (|     | )
       /'\_   _/`\\
       \___)=(___/
'''.strip("\n")


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def format_line(label: str, value: str, width: int = 54) -> str:
    left = f"{label}:"
    dots = "." * max(2, width - len(label) - len(value) - 2)
    return f"{left} {dots} {value}"


def format_stats(stats: dict) -> List[str]:
    return [
        format_line("Repos", str(stats.get("repos", "N/A"))),
        format_line("Commits", str(stats.get("commits", "N/A"))),
    ]


def build_content(data: ProfileData) -> List[str]:
    lines: List[str] = []
    lines.append(f"{data.name} (@{data.username})")
    lines.append("")
    lines.append(format_line("Title", data.title))
    lines.append(format_line("Location", data.location))
    lines.append(format_line("Education", data.education))
    lines.append("")
    lines.append(format_line("Languages", ", ".join(data.languages_programming)))
    lines.append(format_line("Tools", ", ".join(data.libraries_tools)))
    lines.append(format_line("Interests", ", ".join(data.interests)))
    lines.append("")
    lines.append(format_line("Email", data.email))
    lines.append(format_line("LinkedIn", data.linkedin))
    lines.append(format_line("GitHub", data.github))
    lines.append("")
    lines.append("GitHub Stats")
    lines.extend(format_stats(data.stats))
    return lines


def make_svg(data: ProfileData, theme: str = "dark") -> str:
    themes = {
        "dark": {
            "bg": "#0d1117",
            "panel": "#161b22",
            "border": "#30363d",
            "text": "#c9d1d9",
            "muted": "#8b949e",
            "accent": "#58a6ff",
        },
        "light": {
            "bg": "#ffffff",
            "panel": "#f6f8fa",
            "border": "#d0d7de",
            "text": "#24292f",
            "muted": "#57606a",
            "accent": "#0969da",
        },
    }
    palette = themes[theme]

    ascii_lines = ASCII_ART.splitlines()
    info_lines = build_content(data)

    total_lines = max(len(ascii_lines), len(info_lines))
    line_height = 24
    top_padding = 54
    height = top_padding + total_lines * line_height + 40
    width = 980

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(data.name)} profile card">',
        '<style>',
        f".bg {{ fill: {palette['bg']}; }}",
        f".panel {{ fill: {palette['panel']}; stroke: {palette['border']}; stroke-width: 1; }}",
        f".title {{ fill: {palette['accent']}; font: 700 24px 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; }}",
        f".mono {{ fill: {palette['text']}; font: 18px 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; white-space: pre; }}",
        f".muted {{ fill: {palette['muted']}; font: 16px 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; }}",
        '</style>',
        f'<rect class="bg" x="0" y="0" width="{width}" height="{height}" rx="18" />',
        f'<rect class="panel" x="20" y="20" width="{width - 40}" height="{height - 40}" rx="16" />',
        f'<text class="title" x="42" y="56">{esc(data.name)} — profile</text>',
        f'<text class="muted" x="42" y="84">Generated with Python → SVG</text>',
    ]

    ascii_x = 48
    info_x = 360

    for i in range(total_lines):
        y = top_padding + 40 + i * line_height
        left = ascii_lines[i] if i < len(ascii_lines) else ""
        right = info_lines[i] if i < len(info_lines) else ""
        svg_parts.append(f'<text class="mono" x="{ascii_x}" y="{y}">{esc(left)}</text>')
        svg_parts.append(f'<text class="mono" x="{info_x}" y="{y}">{esc(right)}</text>')

    svg_parts.append('</svg>')
    return "\n".join(svg_parts)


def write_files(output_dir: str = ".") -> None:
    data = ProfileData(
        username="emilylopez",
        name="Emily Lopez",
        title="CS @ NYU",
        location="New York, NY",
        education="B.S. Computer Science, NYU Tandon",
        languages_programming=["Python", "C++", "Java", "JavaScript", "SQL", "HTML", "CSS"],
        libraries_tools=["NumPy", "Pandas", "scikit-learn", "OpenCV", "Matplotlib", "Git", "GitHub", "VS Code", "IntelliJ"],
        interests=["S"],
        email="015emily.lopez@gmail.com",
        linkedin="linkedin.com/in/emily-lopez-/",
        github="github.com/emilylopez",
        stats={
            "repos": "update me",
            "commits": "update me",
        },
    )

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "dark_mode.svg").write_text(make_svg(data, "dark"), encoding="utf-8")
    (out / "light_mode.svg").write_text(make_svg(data, "light"), encoding="utf-8")

    readme_snippet = '''<p align="center">
  <img src="./dark_mode.svg#gh-dark-mode-only" alt="Emily Lopez profile card" width="900" />
  <img src="./light_mode.svg#gh-light-mode-only" alt="Emily Lopez profile card" width="900" />
</p>
'''
    (out / "README_snippet.md").write_text(readme_snippet, encoding="utf-8")


if __name__ == "__main__":
    write_files()
    print("Created dark_mode.svg, light_mode.svg, and README_snippet.md")
