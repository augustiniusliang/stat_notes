#!/usr/bin/env python3
r"""Convert LaTeX files in a folder to Markdown files.

Features implemented:
1) Remove preamble and keep real content.
2) Convert inline math \(...\) -> $...$.
3) Convert display math (linenomath+equation, equation, \[...\]) -> $$...$$.
4) Split chapters into separate markdown files when more than one chapter exists.
5) Convert theorem-like environments into bold captions.
6) Convert figure environments, copy images to output graphics folder, center images.
7) Convert basic tabular/table environments to markdown tables.
8) Omit tikzpicture environments.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


THEOREM_ENVS = ["theorem", "corollary", "remark", "proof", "proposition"]
DEFAULT_MACRO_RULES: list[tuple[str, str]] = [
	(r"\\thermfrac\s*\{([^{}]*)\}\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"\\left( \\frac{\\partial \1}{\\partial \2} \\right)_{\3}"),
	(r"\\jacobian\s*\{([^{}]*)\}\s*\{([^{}]*)\}\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"\\frac{\\partial \\left(\1, \2\\right)}{\\partial \\left(\3, \4\\right)}"),
	(r"\\ppp\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"\\frac{\\partial \1}{\\partial \2}"),
	(r"\\tr(?![A-Za-z])", r"\\mathrm{tr}"),
	(r"\\bigzero(?![A-Za-z])", r"\\mbox{\\normalfont\\Large\\bfseries 0}"),
	(r"\\rvline(?![A-Za-z])", r"\\hspace*{-\\arraycolsep}\\vline\\hspace*{-\\arraycolsep}"),
]


def load_macro_rules() -> list[tuple[str, str]]:
	rules = list(DEFAULT_MACRO_RULES)
	try:
		import tex2md_params as params  # type: ignore
	except ImportError:
		return rules

	extra_rules = getattr(params, "MACRO_RULES", None)
	if extra_rules:
		rules.extend(list(extra_rules))
	return rules


def expand_macros(text: str, rules: Iterable[tuple[str, str]]) -> str:
	for pattern, replacement in rules:
		text = re.sub(pattern, replacement, text)
	return text


@dataclass
class ConversionContext:
	source_dir: Path
	output_dir: Path
	graphics_source_dir: Path
	graphics_output_dir: Path
	macro_rules: list[tuple[str, str]] = field(default_factory=load_macro_rules)
	copied_images: set[str] = field(default_factory=set)
	warnings: list[str] = field(default_factory=list)


def strip_comments(text: str) -> str:
	# Remove unescaped % comments.
	return re.sub(r"(?<!\\)%.*$", "", text, flags=re.MULTILINE)


def extract_real_content(text: str) -> str:
	text = text.replace("\r\n", "\n").replace("\r", "\n")
	text = strip_comments(text)

	if "\\begin{document}" in text:
		text = text.split("\\begin{document}", 1)[1]
	if "\\end{document}" in text:
		text = text.split("\\end{document}", 1)[0]

	# Drop frontmatter-ish commands and keep from first structural heading when possible.
	start_match = re.search(r"\\(chapter|section|subsection|subsubsection)\{", text)
	if start_match:
		text = text[start_match.start() :]

	# Remove common non-content commands.
	text = re.sub(r"^\\(frontmatter|mainmatter|appendix|tableofcontents|linenumbers|nolinenumbers|resetlinenumber)\b.*$", "", text, flags=re.MULTILINE)
	text = re.sub(r"^\\newcommand\{.*?\}.*$", "", text, flags=re.MULTILINE)
	text = re.sub(r"^\\renewcommand\{.*?\}.*$", "", text, flags=re.MULTILINE)
	text = re.sub(r"^\\(title|author|date|institute)\{.*?\}\s*$", "", text, flags=re.MULTILINE)
	text = re.sub(r"^\\(maketitle)\s*$", "", text, flags=re.MULTILINE)
	text = re.sub(r"^\\(include|input)\{.*?\}\s*$", "", text, flags=re.MULTILINE)

	return text.strip() + "\n"


def convert_display_math(text: str) -> str:
	placeholders: list[tuple[str, str]] = []

	def stash(rendered: str) -> str:
		token = f"__DISPLAY_MATH_{len(placeholders)}__"
		placeholders.append((token, rendered))
		return token

	def wrap_block(body: str) -> str:
		return f"\n$$\n{body.strip()}\n$$\n"

	def wrap_env(env: str, body: str) -> str:
		normalized_env = {
			"align": "aligned",
			"align*": "aligned",
			"alignat": "alignedat",
			"alignat*": "alignedat",
		}.get(env, env)
		content = f"\\begin{{{normalized_env}}}\n{body.strip()}\n\\end{{{normalized_env}}}"
		return wrap_block(content)

	# Shield outer display-math delimiters first so nested align-family
	# environments are not wrapped a second time later.
	text = re.sub(
		r"\\begin\{linenomath\}\s*\\begin\{equation\*?\}(.*?)\\end\{equation\*?\}\s*\\end\{linenomath\}",
		lambda m: stash(wrap_block(m.group(1))),
		text,
		flags=re.DOTALL,
	)
	text = re.sub(
		r"\\begin\{linenomath\}\s*\\begin\{(align\*?|aligned|alignedat\*?|cases)\}(.*?)\\end\{\1\}\s*\\end\{linenomath\}",
		lambda m: stash(wrap_env(m.group(1), m.group(2))),
		text,
		flags=re.DOTALL,
	)
	text = re.sub(r"\\\[(.*?)\\\]", lambda m: stash(wrap_block(m.group(1))), text, flags=re.DOTALL)
	text = re.sub(r"\\begin\{equation\*?\}(.*?)\\end\{equation\*?\}", lambda m: stash(wrap_block(m.group(1))), text, flags=re.DOTALL)

	# Bare align-family and cases blocks get a single outer display wrapper.
	text = re.sub(
		r"\\begin\{(align\*?|aligned|alignedat\*?|cases|alignat\*?)\}(.*?)\\end\{\1\}",
		lambda m: wrap_env(m.group(1), m.group(2)),
		text,
		flags=re.DOTALL,
	)

	for token, rendered in placeholders:
		text = text.replace(token, rendered)

	return text


def convert_inline_math(text: str) -> str:
	return re.sub(r"\\\((.*?)\\\)", r"$\1$", text, flags=re.DOTALL)


def _find_matching_list_end(text: str, start: int) -> tuple[int, int] | None:
	pattern = re.compile(r"\\begin\{(itemize|enumerate)\}|\\end\{(itemize|enumerate)\}")
	depth = 0
	for match in pattern.finditer(text, start):
		if match.group(1):
			depth += 1
		else:
			depth -= 1
			if depth == 0:
				return match.start(), match.end()
	return None


def _indent_list_item(text: str, indent: str = "  ") -> str:
	lines = text.splitlines()
	if not lines:
		return ""
	formatted = [lines[0].strip()]
	for line in lines[1:]:
		if line.strip():
			formatted.append(f"{indent}{line}")
		else:
			formatted.append("")
	return "\n".join(formatted).rstrip()


def _render_list_block(env: str, body: str) -> str:
	body = convert_lists(body)
	item_matches = list(re.finditer(r"\\item(?:\[(.*?)\])?", body))
	if not item_matches:
		return ""

	intro = body[: item_matches[0].start()].strip()
	items: list[str] = []
	for index, match in enumerate(item_matches, start=1):
		item_start = match.end()
		item_end = item_matches[index].start() if index < len(item_matches) else len(body)
		item_text = body[item_start:item_end].strip()
		label = match.group(1)
		if label:
			item_text = f"**{label.strip()}** {item_text}".strip()

		prefix = "- " if env == "itemize" else f"{index}. "
		items.append(_indent_list_item(f"{prefix}{item_text}"))

	block = "\n".join(items)
	if intro:
		return f"\n{intro}\n\n{block}\n"
	return f"\n{block}\n"


def convert_lists(text: str) -> str:
	search_pos = 0
	parts: list[str] = []
	begin_re = re.compile(r"\\begin\{(itemize|enumerate)\}")

	while True:
		begin_match = begin_re.search(text, search_pos)
		if not begin_match:
			parts.append(text[search_pos:])
			break

		parts.append(text[search_pos:begin_match.start()])
		end_match = _find_matching_list_end(text, begin_match.start())
		if end_match is None:
			parts.append(text[begin_match.start():])
			break

		body = text[begin_match.end():end_match[0]]
		parts.append(_render_list_block(begin_match.group(1), body))
		search_pos = end_match[1]

	return "".join(parts)


def normalize_text_styles(text: str) -> str:
	# Convert common LaTeX inline formatting to markdown.
	text = re.sub(r"\\textbf\{(.*?)\}", r"**\1**", text, flags=re.DOTALL)
	text = re.sub(r"\\textit\{(.*?)\}", r"*\1*", text, flags=re.DOTALL)
	text = re.sub(r"\\emph\{(.*?)\}", r"*\1*", text, flags=re.DOTALL)

	# Remove Chinese font commands while preserving enclosed content if present.
	text = re.sub(r"\\(?:songti|kaishu)\{(.*?)\}", r"\1", text, flags=re.DOTALL)
	text = re.sub(r"\\(?:songti|kaishu)\b", "", text)
	return text


def convert_headings(text: str) -> str:
	mapping = [
		(r"\\chapter\{(.*?)\}", "# "),
		(r"\\section\{(.*?)\}", "## "),
		(r"\\subsection\{(.*?)\}", "### "),
		(r"\\subsubsection\{(.*?)\}", "#### "),
	]
	for pattern, prefix in mapping:
		text = re.sub(pattern, lambda m: f"\n{prefix}{m.group(1).strip()}\n", text)
	return text


def convert_theorem_like(text: str) -> str:
	for env in THEOREM_ENVS:
		title = env.capitalize()
		pattern = rf"\\begin\{{{env}\}}(?:\[(.*?)\])?(.*?)\\end\{{{env}\}}"

		def repl(match: re.Match[str], caption: str = title) -> str:
			opt = match.group(1)
			body = match.group(2).strip()
			if opt:
				head = f"**{caption} ({opt.strip()}).**"
			else:
				head = f"**{caption}.**"
			return f"\n{head}\n\n{body}\n"

		text = re.sub(pattern, repl, text, flags=re.DOTALL)
	return text


def _find_graphics_candidate(ctx: ConversionContext, include_path: str) -> Path | None:
	raw = include_path.strip().replace("\\", "/")
	possible = [raw]
	if raw.startswith("./"):
		possible.append(raw[2:])
	if raw.startswith("graphics/"):
		possible.append(raw.split("graphics/", 1)[1])

	exts = ["", ".png", ".jpg", ".jpeg", ".pdf", ".svg", ".webp"]
	for p in possible:
		base = Path(p)
		checks = [base]
		if base.suffix == "":
			checks.extend(base.with_suffix(ext) for ext in exts if ext)
		for candidate in checks:
			full = (ctx.graphics_source_dir / candidate).resolve()
			if full.exists() and full.is_file():
				return full
	return None


def _convert_pdf_to_png(src_pdf: Path, dst_png: Path) -> bool:
	# Prefer PyMuPDF when available.
	try:
		import fitz  # type: ignore

		doc = fitz.open(src_pdf)
		if len(doc) == 0:
			return False
		page = doc.load_page(0)
		pix = page.get_pixmap(dpi=200)
		pix.save(dst_png)
		doc.close()
		return True
	except Exception:
		pass

	# Fallback to common system tools.
	if shutil.which("magick"):
		result = subprocess.run(
			["magick", "-density", "200", f"{src_pdf}[0]", str(dst_png)],
			capture_output=True,
			text=True,
		)
		if result.returncode == 0 and dst_png.exists():
			return True

	if shutil.which("pdftoppm"):
		base = dst_png.with_suffix("")
		result = subprocess.run(
			["pdftoppm", "-png", "-f", "1", "-singlefile", str(src_pdf), str(base)],
			capture_output=True,
			text=True,
		)
		if result.returncode == 0 and dst_png.exists():
			return True

	return False


def convert_figures(text: str, ctx: ConversionContext) -> str:
	figure_pattern = r"\\begin\{figure\*?\}.*?\\end\{figure\*?\}"

	def repl(match: re.Match[str]) -> str:
		block = match.group(0)
		includes = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", block)
		caption_match = re.search(r"\\caption\{(.*?)\}", block, flags=re.DOTALL)
		caption = ""
		if caption_match:
			caption = re.sub(r"\s+", " ", caption_match.group(1)).strip()

		output_parts: list[str] = []
		for inc in includes:
			src = _find_graphics_candidate(ctx, inc)
			if src is None:
				ctx.warnings.append(f"Image not found for includegraphics path: {inc}")
				continue

			output_name = src.name
			if src.suffix.lower() == ".pdf":
				output_name = f"{src.stem}.png"

			dest = ctx.graphics_output_dir / output_name
			if output_name not in ctx.copied_images:
				if src.suffix.lower() == ".pdf":
					converted = _convert_pdf_to_png(src, dest)
					if not converted:
						ctx.warnings.append(
							f"Failed to convert PDF to PNG for: {src.name}. Install PyMuPDF, ImageMagick, or pdftoppm."
						)
						continue
					legacy_pdf = ctx.graphics_output_dir / src.name
					if legacy_pdf.exists() and legacy_pdf.is_file():
						legacy_pdf.unlink()
				else:
					shutil.copy2(src, dest)
				ctx.copied_images.add(output_name)

			alt = caption if caption else src.stem
			output_parts.append(
				f"<p align=\"center\"><img src=\"graphics/{output_name}\" alt=\"{alt}\" /></p>"
			)

		if caption:
			output_parts.append(f"<p align=\"center\"><em>{caption}</em></p>")

		return "\n" + "\n".join(output_parts) + "\n"

	return re.sub(figure_pattern, repl, text, flags=re.DOTALL)


def _latex_text_cleanup(cell: str) -> str:
	cell = cell.strip()
	cell = normalize_text_styles(cell)
	cell = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?\{(.*?)\}", r"\2", cell)
	cell = re.sub(r"\\[a-zA-Z]+", "", cell)
	return re.sub(r"\s+", " ", cell).strip()


def _tabular_to_markdown(block: str) -> str:
	tabular_match = re.search(r"\\begin\{tabular\}\{.*?\}(.*?)\\end\{tabular\}", block, flags=re.DOTALL)
	if not tabular_match:
		return ""

	body = tabular_match.group(1)
	body = re.sub(r"\\hline|\\cline\{.*?\}", "", body)
	raw_rows = [r.strip() for r in re.split(r"(?<!\\)\\\\", body) if r.strip()]

	rows: list[list[str]] = []
	for raw in raw_rows:
		cells = [
			_latex_text_cleanup(c)
			for c in re.split(r"(?<!\\)&", raw)
		]
		if any(cells):
			rows.append(cells)

	if not rows:
		return ""

	col_count = max(len(r) for r in rows)
	norm_rows = [r + [""] * (col_count - len(r)) for r in rows]
	header = norm_rows[0]
	separator = ["---"] * col_count
	lines = [
		"| " + " | ".join(header) + " |",
		"| " + " | ".join(separator) + " |",
	]
	for row in norm_rows[1:]:
		lines.append("| " + " | ".join(row) + " |")
	return "\n" + "\n".join(lines) + "\n"


def convert_tables(text: str) -> str:
	table_pattern = r"\\begin\{table\*?\}.*?\\end\{table\*?\}"
	text = re.sub(table_pattern, lambda m: _tabular_to_markdown(m.group(0)), text, flags=re.DOTALL)
	tabular_pattern = r"\\begin\{tabular\}\{.*?\}.*?\\end\{tabular\}"
	text = re.sub(tabular_pattern, lambda m: _tabular_to_markdown(m.group(0)), text, flags=re.DOTALL)
	return text


def remove_tikz(text: str) -> str:
	return re.sub(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", "", text, flags=re.DOTALL)


def cleanup_leftovers(text: str) -> str:
	# Preserve display-math env markers before generic begin/end cleanup.
	protected_math_markers: list[tuple[str, str]] = []

	def protect_math_marker(match: re.Match[str]) -> str:
		token = f"__MATH_ENV_MARKER_{len(protected_math_markers)}__"
		protected_math_markers.append((token, match.group(0)))
		return token

	text = re.sub(
		r"\\(?:begin|end)\{(?:alignedat\*?|aligned|cases|matrix|pmatrix)\}",
		protect_math_marker,
		text,
	)

	text = normalize_text_styles(text)
	text = re.sub(r"\\label\{.*?\}", "", text)
	text = re.sub(r"\\centering", "", text)
	text = re.sub(r"\\noindent", "", text)
	text = re.sub(r"\\begin\{center\}|\\end\{center\}", "", text)

	# Drop unknown begin/end markers that may survive conversion.
	text = re.sub(r"\\begin\{[^}]+\}", "", text)
	text = re.sub(r"\\end\{[^}]+\}", "", text)

	for token, original in protected_math_markers:
		text = text.replace(token, original)

	# Collapse excessive empty lines.
	text = re.sub(r"\n{3,}", "\n\n", text)
	return text.strip() + "\n"


def slugify(value: str) -> str:
	value = value.strip().lower()
	value = re.sub(r"\s+", "-", value)
	value = re.sub(r"[^\w\-\u4e00-\u9fff]", "", value)
	value = re.sub(r"-+", "-", value).strip("-")
	return value or "chapter"


def split_by_chapter(markdown_text: str) -> list[tuple[str, str]]:
	lines = markdown_text.splitlines()
	chapter_indices = [i for i, line in enumerate(lines) if line.startswith("# ")]

	if len(chapter_indices) <= 1:
		return []

	chunks: list[tuple[str, str]] = []
	for idx, start in enumerate(chapter_indices):
		end = chapter_indices[idx + 1] if idx + 1 < len(chapter_indices) else len(lines)
		title = lines[start][2:].strip() or f"chapter-{idx + 1}"
		content = "\n".join(lines[start:end]).strip() + "\n"
		chunks.append((title, content))
	return chunks


def convert_latex_to_markdown(tex: str, ctx: ConversionContext) -> str:
	tex = expand_macros(tex, ctx.macro_rules)
	text = extract_real_content(tex)
	text = normalize_text_styles(text)
	text = remove_tikz(text)
	text = convert_display_math(text)
	text = convert_theorem_like(text)
	text = convert_figures(text, ctx)
	text = convert_tables(text)
	text = convert_lists(text)
	text = convert_headings(text)
	text = convert_inline_math(text)
	text = cleanup_leftovers(text)
	return text


def convert_file(tex_file: Path, ctx: ConversionContext) -> list[Path]:
	rel = tex_file.relative_to(ctx.source_dir)
	content = tex_file.read_text(encoding="utf-8", errors="ignore")
	markdown = convert_latex_to_markdown(content, ctx)

	chapter_chunks = split_by_chapter(markdown)
	written: list[Path] = []

	if chapter_chunks:
		split_dir = (ctx.output_dir / rel.parent / rel.stem)
		split_dir.mkdir(parents=True, exist_ok=True)
		for i, (title, chunk) in enumerate(chapter_chunks, start=1):
			out_name = f"{i:02d}-{slugify(title)}.md"
			out_path = split_dir / out_name
			out_path.write_text(chunk, encoding="utf-8")
			written.append(out_path)
	else:
		out_path = (ctx.output_dir / rel.parent / f"{rel.stem}.md")
		out_path.parent.mkdir(parents=True, exist_ok=True)
		out_path.write_text(markdown, encoding="utf-8")
		written.append(out_path)

	return written


def find_tex_files(source_dir: Path, output_dir: Path) -> list[Path]:
	files: list[Path] = []
	for f in source_dir.rglob("*.tex"):
		if output_dir in f.parents:
			continue
		files.append(f)
	return sorted(files)


def build_output_dir(source_dir: Path) -> Path:
	return source_dir.parent / f"md_{source_dir.name}"


def main() -> None:
	parser = argparse.ArgumentParser(description="Convert LaTeX folder to Markdown folder.")
	parser.add_argument(
		"source",
		nargs="?",
		default=".",
		help="Source directory containing .tex files (default: current directory).",
	)
	args = parser.parse_args()

	source_dir = Path(args.source).resolve()
	if not source_dir.exists() or not source_dir.is_dir():
		raise SystemExit(f"Source directory does not exist: {source_dir}")

	output_dir = build_output_dir(source_dir)
	output_dir.mkdir(parents=True, exist_ok=True)

	graphics_source_dir = source_dir / ".."
	graphics_output_dir = output_dir / "graphics"
	graphics_output_dir.mkdir(parents=True, exist_ok=True)

	ctx = ConversionContext(
		source_dir=source_dir,
		output_dir=output_dir,
		graphics_source_dir=graphics_source_dir,
		graphics_output_dir=graphics_output_dir,
	)

	tex_files = find_tex_files(source_dir, output_dir)
	if not tex_files:
		print("No .tex files found.")
		return

	written_files: list[Path] = []
	for tex_file in tex_files:
		written_files.extend(convert_file(tex_file, ctx))

	print(f"Converted {len(tex_files)} tex files into {len(written_files)} markdown files.")
	print(f"Output directory: {output_dir}")
	print(f"Copied graphics: {len(ctx.copied_images)}")
	if ctx.warnings:
		print("Warnings:")
		for warning in ctx.warnings:
			print(f"- {warning}")


if __name__ == "__main__":
	main()
