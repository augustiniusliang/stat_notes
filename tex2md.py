#!/usr/bin/env python3
"""Convert LaTeX files in a folder to Markdown files.

Features implemented:
1) Remove preamble and keep real content.
2) Convert inline math \(...\) -> $...$.
3) Convert display math (linenomath+equation, equation, \[...\]) -> $$...$$.
4) Split chapters into separate markdown files when more than one chapter exists.
5) Convert theorem-like environments into bold captions.
6) Convert figure environments, copy images to output graphics folder, center images.
7) Convert basic tabular/table environments to markdown tables.
8) Render tikzpicture environments into standalone PNG images.
9) Render asymptote environments into standalone PNG images.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


DEFAULT_CONFIG: dict[str, object] = {
	"theorem_envs": ["theorem", "corollary", "remark", "proof", "proposition", "definition", "assumption", "example", "lemma"],
	"tikz_envs": ["tikzpicture", "tikzcd"],
	"asymptote_envs": ["asy", "asymptote"],
	"standalone_packages": ["amsmath", "amssymb", "bm"],
	"tikz_standalone": {"font_size": "11pt", "border": "2pt"},
	"asymptote_standalone": {"font_size": "11pt", "border": "2pt"},
	"heading_levels": ["chapter", "section", "subsection", "subsubsection"],
	"list_envs": ["itemize", "enumerate"],
	"graphics_extensions": [".png", ".jpg", ".jpeg", ".pdf", ".svg", ".webp"],
	"protected_math_envs": ["alignedat*", "aligned", "cases", "matrix", "pmatrix", "bmatrix", "Bmatrix", "vmatrix", "Vmatrix", "smallmatrix", "array"],
	"macro_rules": [
		[r"\\thermfrac\s*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}\s*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}\s*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}", r"\\left( \\frac{\\partial \1}{\\partial \2} \\right)_{\3}"],
		[r"\\jacobian\s*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}\s*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}\s*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}\s*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}", r"\\frac{\\partial \\left(\1, \2\\right)}{\\partial \\left(\3, \4\\right)}"],
		[r"\\ppp\s*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}\s*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}", r"\\frac{\\partial \1}{\\partial \2}"],
		[r"\\tr(?![A-Za-z])", r"\\mathrm{tr}"],
		[r"\\bigzero(?![A-Za-z])", r"\\mbox{\\normalfont\\Large\\bfseries 0}"],
		[r"\\rvline(?![A-Za-z])", r"\\hspace*{-\\arraycolsep}\\vline\\hspace*{-\\arraycolsep}"],
	],
}
DEFAULT_MACRO_RULES: list[tuple[str, str]] = [
	(r"\\thermfrac\s*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}\s*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}\s*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}", r"\\left( \\frac{\\partial \1}{\\partial \2} \\right)_{\3}"),
	(r"\\jacobian\s*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}\s*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}\s*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}\s*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}", r"\\frac{\\partial \\left(\1, \2\\right)}{\\partial \\left(\3, \4\\right)}"),
	(r"\\ppp\s*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}\s*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}", r"\\frac{\\partial \1}{\\partial \2}"),
	(r"\\tr(?![A-Za-z])", r"\\mathrm{tr}"),
	(r"\\bigzero(?![A-Za-z])", r"\\mbox{\\normalfont\\Large\\bfseries 0}"),
	(r"\\rvline(?![A-Za-z])", r"\\hspace*{-\\arraycolsep}\\vline\\hspace*{-\\arraycolsep}"),
]


def _load_config(config_path: Path | None = None) -> dict[str, object]:
	if config_path is None:
		config_path = Path(__file__).with_name("tex2md_config.json")
	config: dict[str, object] = dict(DEFAULT_CONFIG)
	if not config_path.exists():
		return config

	try:
		loaded = json.loads(config_path.read_text(encoding="utf-8"))
	except Exception:
		return config

	if isinstance(loaded, dict):
		for key in (
			"theorem_envs",
			"tikz_envs",
			"asymptote_envs",
			"standalone_packages",
			"heading_levels",
			"list_envs",
			"graphics_extensions",
			"protected_math_envs",
			"macro_rules",
		):
			value = loaded.get(key)
			if isinstance(value, list):
				config[key] = value
		for key in ("tikz_standalone", "asymptote_standalone"):
			value = loaded.get(key)
			if isinstance(value, dict):
				config[key] = value
	return config


CONFIG: dict[str, object] = {}
THEOREM_ENVS: list[str] = []
TIKZ_ENVS: list[str] = []
ASYMPTOTE_ENVS: list[str] = []
DEFAULT_STANDALONE_PACKAGES: list[str] = []
HEADING_LEVELS: list[str] = []
LIST_ENVS: list[str] = []
GRAPHICS_EXTENSIONS: list[str] = []
PROTECTED_MATH_ENVS: list[str] = []
TIKZ_STANDALONE: object = {}
ASYMPTOTE_STANDALONE: object = {}
TIKZ_ENV_PATTERN = re.compile(r"$^")
ASYMPTOTE_ENV_PATTERN = re.compile(r"$^")
LIST_ENV_PATTERN = ""


def initialize_config(config_path: Path | None = None) -> None:
	global CONFIG
	global THEOREM_ENVS
	global TIKZ_ENVS
	global ASYMPTOTE_ENVS
	global DEFAULT_STANDALONE_PACKAGES
	global HEADING_LEVELS
	global LIST_ENVS
	global GRAPHICS_EXTENSIONS
	global PROTECTED_MATH_ENVS
	global TIKZ_STANDALONE
	global ASYMPTOTE_STANDALONE
	global TIKZ_ENV_PATTERN
	global ASYMPTOTE_ENV_PATTERN
	global LIST_ENV_PATTERN

	CONFIG = _load_config(config_path)
	THEOREM_ENVS = [str(v) for v in CONFIG.get("theorem_envs", DEFAULT_CONFIG["theorem_envs"])]
	TIKZ_ENVS = [str(v) for v in CONFIG.get("tikz_envs", DEFAULT_CONFIG["tikz_envs"])]
	ASYMPTOTE_ENVS = [str(v) for v in CONFIG.get("asymptote_envs", DEFAULT_CONFIG["asymptote_envs"])]
	DEFAULT_STANDALONE_PACKAGES = [str(v) for v in CONFIG.get("standalone_packages", DEFAULT_CONFIG["standalone_packages"])]
	HEADING_LEVELS = [str(v) for v in CONFIG.get("heading_levels", DEFAULT_CONFIG["heading_levels"])]
	LIST_ENVS = [str(v) for v in CONFIG.get("list_envs", DEFAULT_CONFIG["list_envs"])]
	GRAPHICS_EXTENSIONS = [str(v) for v in CONFIG.get("graphics_extensions", DEFAULT_CONFIG["graphics_extensions"])]
	PROTECTED_MATH_ENVS = [str(v) for v in CONFIG.get("protected_math_envs", DEFAULT_CONFIG["protected_math_envs"])]
	TIKZ_STANDALONE = CONFIG.get("tikz_standalone", DEFAULT_CONFIG["tikz_standalone"])
	ASYMPTOTE_STANDALONE = CONFIG.get("asymptote_standalone", DEFAULT_CONFIG["asymptote_standalone"])
	TIKZ_ENV_PATTERN = re.compile(
		rf"\\begin\{{({'|'.join(re.escape(env) for env in TIKZ_ENVS)})\}}(?:\[(.*?)\])?(.*?)\\end\{{\1\}}",
		flags=re.DOTALL,
	)
	ASYMPTOTE_ENV_PATTERN = re.compile(
		rf"\\begin\{{({'|'.join(re.escape(env) for env in ASYMPTOTE_ENVS)})\}}(?:\[(.*?)\])?(.*?)\\end\{{\1\}}",
		flags=re.DOTALL,
	)
	LIST_ENV_PATTERN = "|".join(re.escape(env) for env in LIST_ENVS)


initialize_config()


def _standalone_options(config_value: object, extras: list[str] | None = None) -> str:
	config_dict = config_value if isinstance(config_value, dict) else {}
	font_size = str(config_dict.get("font_size", "11pt")).strip()
	border = str(config_dict.get("border", "2pt")).strip()
	parts: list[str] = []
	if font_size:
		parts.append(font_size)
	if extras:
		parts.extend(extras)
	if border:
		parts.append(f"border={border}")
	return ",".join(parts)


def _macro_rules_from_config() -> list[tuple[str, str]]:
	rules_raw = CONFIG.get("macro_rules", DEFAULT_CONFIG["macro_rules"])
	parsed: list[tuple[str, str]] = []
	if isinstance(rules_raw, list):
		for item in rules_raw:
			if isinstance(item, (list, tuple)) and len(item) == 2:
				parsed.append((str(item[0]), str(item[1])))
	return parsed or list(DEFAULT_MACRO_RULES)


def load_macro_rules() -> list[tuple[str, str]]:
	rules = _macro_rules_from_config()
	return rules


def expand_macros(text: str, rules: Iterable[tuple[str, str]]) -> str:
	for pattern, replacement in rules:
		text = re.sub(pattern, replacement, text)
	return text


class ProcessLogger:
	def __init__(self, log_path: Path):
		self.log_path = log_path
		self.log_path.parent.mkdir(parents=True, exist_ok=True)
		self._fp = self.log_path.open("w", encoding="utf-8")

	def log(self, message: str) -> None:
		timestamp = datetime.now().strftime("%H:%M:%S")
		line = f"[{timestamp}] {message}"
		print(line)
		self._fp.write(line + "\n")
		self._fp.flush()

	def close(self) -> None:
		self._fp.close()


def _log(ctx: "ConversionContext", message: str) -> None:
	if ctx.logger is not None:
		ctx.logger.log(message)


@dataclass
class ConversionContext:
	source_dir: Path
	output_dir: Path
	graphics_source_dir: Path
	graphics_output_dir: Path
	logger: ProcessLogger | None = None
	macro_rules: list[tuple[str, str]] = field(default_factory=load_macro_rules)
	copied_images: set[str] = field(default_factory=set)
	warnings: list[str] = field(default_factory=list)
	tikz_counter: int = 0
	asymptote_counter: int = 0
	rendered_tikz_sources: dict[str, str] = field(default_factory=dict)
	rendered_asymptote_sources: dict[str, str] = field(default_factory=dict)


def strip_comments(text: str) -> str:
	# Remove unescaped % comments.
	return re.sub(r"(?<!\\)%.*$", "", text, flags=re.MULTILINE)


def extract_real_content(text: str) -> str:
	text = text.replace("\r\n", "\n").replace("\r", "\n")
	text = strip_comments(text)
	# Normalize indentation while preserving blank lines.
	text = "\n".join(line.lstrip() if line.strip() else "" for line in text.split("\n"))

	if "\\begin{document}" in text:
		text = text.split("\\begin{document}", 1)[1]
	if "\\end{document}" in text:
		text = text.split("\\end{document}", 1)[0]

	# Drop frontmatter-ish commands and keep from first structural heading when possible.
	start_match = re.search(rf"\\({'|'.join(re.escape(level) for level in HEADING_LEVELS)})\{{", text)
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
	return re.sub(r"\\\((.*?)\\\)", lambda m: f"${m.group(1).strip()}$", text, flags=re.DOTALL)


def normalize_math_delimiter_spacing(text: str) -> str:
	# Tighten inline math: no spaces touching the opening/closing $.
	text = re.sub(r"(?<!\$)\$(?!\$)\s*(.*?)\s*(?<!\$)\$(?!\$)", lambda m: f"${m.group(1).strip()}$", text, flags=re.DOTALL)
	# Tighten one-line display math tokens before block normalization.
	text = re.sub(r"\$\$\s*(.*?)\s*\$\$", lambda m: f"$${m.group(1).strip()}$$", text, flags=re.DOTALL)
	return text


def normalize_display_math_blocks(text: str) -> str:
	def repl(match: re.Match[str]) -> str:
		body = match.group(1).strip()
		return f"\n$$\n{body}\n$$\n"

	text = re.sub(r"\$\$(.*?)\$\$", repl, text, flags=re.DOTALL)
	# Ensure exactly one newline before opening $$ (no blank line).
	text = re.sub(r"([^\n])\s*\n*\$\$", r"\1\n$$", text)
	text = re.sub(r"\n{2,}\$\$", r"\n$$", text)
	# Ensure exactly one newline after closing $$ (no blank line).
	text = re.sub(r"\$\$\s*\n*([^\n])", r"$$\n\1", text)
	text = re.sub(r"\$\$\n{2,}", r"$$\n", text)
	return text


def _find_matching_list_end(text: str, start: int) -> tuple[int, int] | None:
	pattern = re.compile(rf"\\begin\{{({LIST_ENV_PATTERN})\}}|\\end\{{({LIST_ENV_PATTERN})\}}")
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
	begin_re = re.compile(rf"\\begin\{{({LIST_ENV_PATTERN})\}}")

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
	text = re.sub(r"\\textsc\{(.*?)\}", r"*\1*", text, flags=re.DOTALL)
	text = re.sub(r"\\emph\{(.*?)\}", r"*\1*", text, flags=re.DOTALL)

	# Remove Chinese font commands while preserving enclosed content if present.
	text = re.sub(r"\\(?:songti|kaishu)\{(.*?)\}", r"\1", text, flags=re.DOTALL)
	text = re.sub(r"\\(?:songti|kaishu)\b", "", text)
	return text


def _detect_heading_shift(text: str) -> int:
	first: tuple[int, int] | None = None
	for i, level in enumerate(HEADING_LEVELS):
		match = re.search(rf"\\{level}\{{", text)
		if match is None:
			continue
		if first is None or match.start() < first[0]:
			first = (match.start(), i)
	return first[1] if first is not None else 0


def convert_headings(text: str) -> str:
	shift = _detect_heading_shift(text)
	for i, level in enumerate(HEADING_LEVELS):
		depth = max(1, i - shift + 1)
		prefix = "#" * depth
		text = re.sub(rf"\\{level}\{{(.*?)\}}", lambda m, p=prefix: f"\n{p} {m.group(1).strip()}\n", text)
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

	exts = [""] + GRAPHICS_EXTENSIONS
	for p in possible:
		base = Path(p)
		checks = [base]
		if base.suffix == "":
			checks.extend(base.with_suffix(ext) for ext in exts if ext)
		for candidate in checks:
			full = (ctx.graphics_source_dir / candidate).resolve()
			if full.exists() and full.is_file():
				return full

	# Fallback: search recursively by filename in subfolders.
	base_name = Path(raw).stem if Path(raw).suffix else Path(raw).name
	search_exts = [Path(raw).suffix.lower()] if Path(raw).suffix else [ext for ext in exts if ext]
	for ext in search_exts:
		pattern = f"**/{base_name}{ext}"
		for candidate in ctx.graphics_source_dir.glob(pattern):
			if candidate.is_file():
				return candidate.resolve()
	return None


def _find_tikz_source_candidate(ctx: ConversionContext, include_path: str) -> Path | None:
	raw = include_path.strip().replace("\\", "/")
	possible = [raw]
	if raw.startswith("./"):
		possible.append(raw[2:])
	if raw.startswith("graphics/"):
		possible.append(raw.split("graphics/", 1)[1])

	for p in possible:
		base = Path(p)
		candidate = base.with_suffix(".tex")
		full = (ctx.graphics_source_dir / candidate).resolve()
		if full.exists() and full.is_file():
			return full

	# Fallback: search recursively by basename in subfolders.
	base_name = Path(raw).stem if Path(raw).suffix else Path(raw).name
	for candidate in ctx.graphics_source_dir.glob(f"**/{base_name}.tex"):
		if candidate.is_file():
			return candidate.resolve()
	return None


def _find_asymptote_source_candidate(ctx: ConversionContext, include_path: str) -> Path | None:
	raw = include_path.strip().replace("\\", "/")
	possible = [raw]
	if raw.startswith("./"):
		possible.append(raw[2:])
	if raw.startswith("graphics/"):
		possible.append(raw.split("graphics/", 1)[1])

	for p in possible:
		base = Path(p)
		candidate = base.with_suffix(".asy")
		full = (ctx.graphics_source_dir / candidate).resolve()
		if full.exists() and full.is_file():
			return full

	base_name = Path(raw).stem if Path(raw).suffix else Path(raw).name
	for candidate in ctx.graphics_source_dir.glob(f"**/{base_name}.asy"):
		if candidate.is_file():
			return candidate.resolve()
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


def _render_includegraphics(
	include_path: str,
	ctx: ConversionContext,
	source_tex_file: Path,
	caption: str = "",
	log_scope: str = "includegraphics",
) -> str | None:
	_log(ctx, f"[{source_tex_file.name}] {log_scope}: {include_path}")
	src = _find_graphics_candidate(ctx, include_path)
	if src is None:
		tikz_source = _find_tikz_source_candidate(ctx, include_path)
		if tikz_source is not None:
			_log(ctx, f"[{source_tex_file.name}] {log_scope} fallback: rendering TikZ source {tikz_source.name}")
			rendered = _render_tikz_from_source_file(ctx, tikz_source)
			if rendered:
				return rendered
		asy_source = _find_asymptote_source_candidate(ctx, include_path)
		if asy_source is not None:
			_log(ctx, f"[{source_tex_file.name}] {log_scope} fallback: rendering Asymptote source {asy_source.name}")
			rendered = _render_asymptote_from_source_file(ctx, asy_source)
			if rendered:
				return rendered
		ctx.warnings.append(f"Image not found for includegraphics path: {include_path}")
		_log(ctx, f"[{source_tex_file.name}] warning: image not found for includegraphics path: {include_path}")
		return None

	output_name = src.name
	if src.suffix.lower() == ".pdf":
		output_name = f"{src.stem}.png"

	dest = ctx.graphics_output_dir / output_name
	if output_name not in ctx.copied_images:
		if src.suffix.lower() == ".pdf":
			_log(ctx, f"[{source_tex_file.name}] converting PDF to PNG: {src.name} -> {output_name}")
			converted = _convert_pdf_to_png(src, dest)
			if not converted:
				ctx.warnings.append(
					f"Failed to convert PDF to PNG for: {src.name}. Install PyMuPDF, ImageMagick, or pdftoppm."
				)
				_log(ctx, f"[{source_tex_file.name}] warning: failed PDF->PNG conversion for {src.name}")
				return None
			legacy_pdf = ctx.graphics_output_dir / src.name
			if legacy_pdf.exists() and legacy_pdf.is_file():
				legacy_pdf.unlink()
		else:
			_log(ctx, f"[{source_tex_file.name}] copying image: {src.name}")
			shutil.copy2(src, dest)
		ctx.copied_images.add(output_name)

	alt = caption if caption else src.stem
	return f"<p align=\"center\"><img src=\"/graphics/{output_name}\" alt=\"{alt}\" /></p>"


def convert_figures(text: str, ctx: ConversionContext, source_tex_file: Path) -> str:
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
			rendered = _render_includegraphics(inc, ctx, source_tex_file, caption=caption, log_scope="figure includegraphics")
			if rendered:
				output_parts.append(rendered)

		for tikz_match in TIKZ_ENV_PATTERN.finditer(block):
			rendered = _render_tikz_picture(tikz_match, ctx, source_tex_file)
			if rendered:
				output_parts.append(rendered)

		for asy_match in ASYMPTOTE_ENV_PATTERN.finditer(block):
			rendered = _render_asymptote_block(asy_match, ctx, source_tex_file)
			if rendered:
				output_parts.append(rendered)

		if caption:
			output_parts.append(f"<p align=\"center\"><em>{caption}</em></p>")

		return "\n" + "\n".join(output_parts) + "\n"

	return re.sub(figure_pattern, repl, text, flags=re.DOTALL)


def convert_includegraphics(text: str, ctx: ConversionContext, source_tex_file: Path) -> str:
	pattern = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")

	def repl(match: re.Match[str]) -> str:
		include_path = match.group(1)
		rendered = _render_includegraphics(include_path, ctx, source_tex_file, log_scope="inline includegraphics")
		if rendered:
			return "\n" + rendered + "\n"
		# Keep original command if unresolved outside figures.
		return match.group(0)

	return pattern.sub(repl, text)


def _collect_tikz_dependencies(texts: Iterable[str]) -> list[str]:
	packages: list[str] = []
	libraries: list[str] = []
	seen_packages: set[str] = set()
	seen_libraries: set[str] = set()

	for text in texts:
		for match in re.finditer(r"^\\usepackage(?:\[[^\]]*\])?\{([^}]*)\}", text, flags=re.MULTILINE):
			for package in (part.strip() for part in match.group(1).split(",")):
				if not package:
					continue
				if package not in {"tikz", "tikz-cd"} and "tikz" not in package and "pgf" not in package and package != "ctex":
					continue
				if package in seen_packages:
					continue
				seen_packages.add(package)
				packages.append(f"\\usepackage{{{package}}}")

		for match in re.finditer(r"^\\usetikzlibrary\{([^}]*)\}", text, flags=re.MULTILINE):
			for library in (part.strip() for part in match.group(1).split(",")):
				if not library or library in seen_libraries:
					continue
				seen_libraries.add(library)
				libraries.append(f"\\usetikzlibrary{{{library}}}")

	if not any(line == "\\usepackage{tikz}" for line in packages):
		packages.insert(0, "\\usepackage{tikz}")
	for package in DEFAULT_STANDALONE_PACKAGES:
		line = f"\\usepackage{{{package}}}"
		if line not in packages:
			packages.append(line)

	return packages + libraries


def _compact_tikz_body(body: str) -> str:
	# Drop blank lines inside tikz blocks to avoid noisy standalone sources.
	lines = [line for line in body.splitlines() if line.strip()]
	return "\n".join(lines).strip()


def _compact_asymptote_body(body: str) -> str:
	lines = [line for line in body.splitlines() if line.strip()]
	return "\n".join(lines).strip()


def _clear_tikz_env_empty_lines(text: str) -> str:
	def repl(match: re.Match[str]) -> str:
		env_name = match.group(1)
		options = (match.group(2) or "").strip()
		body = _compact_tikz_body(match.group(3))
		if options:
			return f"\\begin{{{env_name}}}[{options}]\n{body}\n\\end{{{env_name}}}"
		return f"\\begin{{{env_name}}}\n{body}\n\\end{{{env_name}}}"

	return TIKZ_ENV_PATTERN.sub(repl, text)


def _clear_asymptote_env_empty_lines(text: str) -> str:
	def repl(match: re.Match[str]) -> str:
		env_name = match.group(1)
		options = (match.group(2) or "").strip()
		body = _compact_asymptote_body(match.group(3))
		if options:
			return f"\\begin{{{env_name}}}[{options}]\n{body}\n\\end{{{env_name}}}"
		return f"\\begin{{{env_name}}}\n{body}\n\\end{{{env_name}}}"

	return ASYMPTOTE_ENV_PATTERN.sub(repl, text)


def _standalone_tikz_document(env_name: str, tikz_body: str, options: str, dependencies: list[str]) -> str:
	class_options = _standalone_options(TIKZ_STANDALONE, extras=["tikz"])
	parts = [f"\\documentclass[{class_options}]{{standalone}}"]
	parts.extend(dependencies)
	parts.append("\\begin{document}")
	if options:
		parts.append(f"\\begin{{{env_name}}}[{options}]")
	else:
		parts.append(f"\\begin{{{env_name}}}")
	parts.append(tikz_body.strip())
	parts.append(f"\\end{{{env_name}}}")
	parts.append("\\end{document}")
	return "\n".join(parts) + "\n"


def _standalone_asymptote_document(env_name: str, asy_body: str, options: str, dependencies: list[str]) -> str:
	class_options = _standalone_options(ASYMPTOTE_STANDALONE)
	parts = [f"\\documentclass[{class_options}]{{standalone}}"]
	parts.extend(dependencies)
	parts.append("\\usepackage{asymptote}")
	parts.append("\\begin{document}")
	if options:
		parts.append(f"\\begin{{{env_name}}}[{options}]")
	else:
		parts.append(f"\\begin{{{env_name}}}")
	parts.append(asy_body.strip())
	parts.append(f"\\end{{{env_name}}}")
	parts.append("\\end{document}")
	return "\n".join(parts) + "\n"


def _compile_tikz_standalone(tex_file: Path) -> bool:
	output_dir = tex_file.parent

	if shutil.which("latexmk"):
		command = [
			"latexmk",
			"-xelatex",
			"-interaction=nonstopmode",
			"-halt-on-error",
			f"-outdir={output_dir}",
			str(tex_file),
		]
		result = subprocess.run(command, cwd=output_dir, capture_output=True, text=True)
		return result.returncode == 0

	compiler = shutil.which("xelatex") or shutil.which("pdflatex")
	if compiler is None:
		return False

	command = [
		compiler,
		"-interaction=nonstopmode",
		"-halt-on-error",
		f"-output-directory={output_dir}",
		str(tex_file),
	]
	first_run = subprocess.run(command, cwd=output_dir, capture_output=True, text=True)
	if first_run.returncode != 0:
		return False
	second_run = subprocess.run(command, cwd=output_dir, capture_output=True, text=True)
	return second_run.returncode == 0


def _compile_asymptote_standalone(tex_file: Path) -> bool:
	output_dir = tex_file.parent

	if shutil.which("latexmk"):
		command = [
			"latexmk",
			"-xelatex",
			"-shell-escape",
			"-interaction=nonstopmode",
			"-halt-on-error",
			f"-outdir={output_dir}",
			str(tex_file),
		]
		result = subprocess.run(command, cwd=output_dir, capture_output=True, text=True)
		return result.returncode == 0

	compiler = shutil.which("xelatex") or shutil.which("pdflatex")
	if compiler is None:
		return False

	command = [
		compiler,
		"-shell-escape",
		"-interaction=nonstopmode",
		"-halt-on-error",
		f"-output-directory={output_dir}",
		str(tex_file),
	]
	first_run = subprocess.run(command, cwd=output_dir, capture_output=True, text=True)
	if first_run.returncode != 0:
		return False
	second_run = subprocess.run(command, cwd=output_dir, capture_output=True, text=True)
	return second_run.returncode == 0


def _tikz_base_slug(ctx: ConversionContext, source_tex_file: Path) -> str:
	try:
		rel = source_tex_file.relative_to(ctx.source_dir)
		return slugify("-".join(rel.with_suffix("").parts))
	except ValueError:
		return slugify(source_tex_file.stem)


def _render_tikz_picture(match: re.Match[str], ctx: ConversionContext, source_tex_file: Path) -> str:
	env_name = (match.group(1) or "tikzpicture").strip()
	options = (match.group(2) or "").strip()
	body = _compact_tikz_body(match.group(3))
	if not body.strip():
		return ""

	ctx.tikz_counter += 1
	base_slug = _tikz_base_slug(ctx, source_tex_file)
	output_name = f"{base_slug}-tikz-{ctx.tikz_counter:02d}.png"
	standalone_name = f"{base_slug}-tikz-{ctx.tikz_counter:02d}.tex"
	standalone_tex = ctx.graphics_output_dir / standalone_name
	output_png = ctx.graphics_output_dir / output_name

	main_tex = ctx.source_dir / "main.tex"
	texts = [source_tex_file.read_text(encoding="utf-8", errors="ignore")]
	if main_tex.exists() and main_tex != source_tex_file:
		texts.append(main_tex.read_text(encoding="utf-8", errors="ignore"))
	dependencies = _collect_tikz_dependencies(texts)
	if env_name == "tikzcd" and "\\usetikzlibrary{cd}" not in dependencies:
		dependencies.append("\\usetikzlibrary{cd}")
	if any(ord(ch) > 127 for ch in body) and "\\usepackage{ctex}" not in dependencies:
		dependencies.insert(1 if dependencies and dependencies[0] == "\\usepackage{tikz}" else 0, "\\usepackage{ctex}")

	standalone_tex.write_text(_standalone_tikz_document(env_name, body, options, dependencies), encoding="utf-8")
	_log(ctx, f"[{source_tex_file.name}] render {env_name}: compiling {standalone_tex.name}")
	if not _compile_tikz_standalone(standalone_tex):
		ctx.warnings.append(f"Failed to compile {env_name} picture in {source_tex_file.name}.")
		_log(ctx, f"[{source_tex_file.name}] warning: failed to compile {env_name} standalone")
		return ""

	pdf_path = standalone_tex.with_suffix(".pdf")
	if not pdf_path.exists():
		ctx.warnings.append(f"Missing PDF output for TikZ picture in {source_tex_file.name}.")
		_log(ctx, f"[{source_tex_file.name}] warning: missing PDF output for {env_name}")
		return ""

	if not _convert_pdf_to_png(pdf_path, output_png):
		ctx.warnings.append(f"Failed to convert TikZ PDF to PNG in {source_tex_file.name}.")
		_log(ctx, f"[{source_tex_file.name}] warning: failed to convert {env_name} PDF to PNG")
		return ""

	ctx.copied_images.add(output_name)
	_log(ctx, f"[{source_tex_file.name}] rendered {env_name} -> graphics/{output_name}")
	alt = f"{env_name} diagram {ctx.tikz_counter}"
	return f'<p align="center"><img src="/graphics/{output_name}" alt="{alt}" /></p>'


def _render_tikz_from_source_file(ctx: ConversionContext, tikz_source_file: Path) -> str:
	cache_key = str(tikz_source_file.resolve())
	if cache_key in ctx.rendered_tikz_sources:
		output_name = ctx.rendered_tikz_sources[cache_key]
		return f'<p align="center"><img src="/graphics/{output_name}" alt="{tikz_source_file.stem}" /></p>'

	content = tikz_source_file.read_text(encoding="utf-8", errors="ignore")
	match = TIKZ_ENV_PATTERN.search(content)
	if match is None:
		ctx.warnings.append(f"TikZ source has no tikzpicture/tikzcd environment: {tikz_source_file.name}")
		return ""

	rendered = _render_tikz_picture(match, ctx, tikz_source_file)
	if not rendered:
		return ""

	name_match = re.search(r'src="graphics/([^"]+)"', rendered)
	if name_match:
		ctx.rendered_tikz_sources[cache_key] = name_match.group(1)
	return rendered


def _render_asymptote_content(env_name: str, options: str, body: str, ctx: ConversionContext, source_tex_file: Path) -> str:
	if not body.strip():
		return ""

	ctx.asymptote_counter += 1
	base_slug = _tikz_base_slug(ctx, source_tex_file)
	output_name = f"{base_slug}-asy-{ctx.asymptote_counter:02d}.png"
	standalone_name = f"{base_slug}-asy-{ctx.asymptote_counter:02d}.tex"
	standalone_tex = ctx.graphics_output_dir / standalone_name
	output_png = ctx.graphics_output_dir / output_name

	dependencies = [f"\\usepackage{{{pkg}}}" for pkg in DEFAULT_STANDALONE_PACKAGES]
	standalone_tex.write_text(_standalone_asymptote_document(env_name, body, options, dependencies), encoding="utf-8")
	_log(ctx, f"[{source_tex_file.name}] render {env_name}: compiling {standalone_tex.name}")
	if not _compile_asymptote_standalone(standalone_tex):
		ctx.warnings.append(f"Failed to compile {env_name} block in {source_tex_file.name}.")
		_log(ctx, f"[{source_tex_file.name}] warning: failed to compile {env_name} standalone")
		return ""

	pdf_path = standalone_tex.with_suffix(".pdf")
	if not pdf_path.exists():
		ctx.warnings.append(f"Missing PDF output for asymptote block in {source_tex_file.name}.")
		_log(ctx, f"[{source_tex_file.name}] warning: missing PDF output for {env_name}")
		return ""

	if not _convert_pdf_to_png(pdf_path, output_png):
		ctx.warnings.append(f"Failed to convert asymptote PDF to PNG in {source_tex_file.name}.")
		_log(ctx, f"[{source_tex_file.name}] warning: failed to convert {env_name} PDF to PNG")
		return ""

	ctx.copied_images.add(output_name)
	_log(ctx, f"[{source_tex_file.name}] rendered {env_name} -> graphics/{output_name}")
	alt = f"{env_name} diagram {ctx.asymptote_counter}"
	return f'<p align="center"><img src="graphics/{output_name}" alt="{alt}" /></p>'


def _render_asymptote_block(match: re.Match[str], ctx: ConversionContext, source_tex_file: Path) -> str:
	env_name = (match.group(1) or "asy").strip()
	options = (match.group(2) or "").strip()
	body = _compact_asymptote_body(match.group(3))
	return _render_asymptote_content(env_name, options, body, ctx, source_tex_file)


def _render_asymptote_from_source_file(ctx: ConversionContext, asy_source_file: Path) -> str:
	cache_key = str(asy_source_file.resolve())
	if cache_key in ctx.rendered_asymptote_sources:
		output_name = ctx.rendered_asymptote_sources[cache_key]
		return f'<p align="center"><img src="graphics/{output_name}" alt="{asy_source_file.stem}" /></p>'

	body = _compact_asymptote_body(asy_source_file.read_text(encoding="utf-8", errors="ignore"))
	if not body:
		ctx.warnings.append(f"Asymptote source is empty: {asy_source_file.name}")
		return ""
	rendered = _render_asymptote_content("asy", "", body, ctx, asy_source_file)
	if not rendered:
		return ""

	name_match = re.search(r'src="/graphics/([^"]+)"', rendered)
	if name_match:
		ctx.rendered_asymptote_sources[cache_key] = name_match.group(1)
	return rendered


def convert_asymptote_blocks(text: str, ctx: ConversionContext, source_tex_file: Path) -> str:
	def repl(match: re.Match[str]) -> str:
		rendered = _render_asymptote_block(match, ctx, source_tex_file)
		if rendered:
			return "\n" + rendered + "\n"
		return ""

	return ASYMPTOTE_ENV_PATTERN.sub(repl, text)


def convert_tikz_pictures(text: str, ctx: ConversionContext, source_tex_file: Path) -> str:
	def repl(match: re.Match[str]) -> str:
		rendered = _render_tikz_picture(match, ctx, source_tex_file)
		if rendered:
			return "\n" + rendered + "\n"
		return ""

	return TIKZ_ENV_PATTERN.sub(repl, text)


def _latex_text_cleanup(cell: str) -> str:
	cell = cell.strip()
	cell = normalize_text_styles(cell)
	# Keep table math inline-only: no display math delimiters inside markdown tables.
	cell = re.sub(r"\$\$(.*?)\$\$", lambda m: f"${m.group(1).strip()}$", cell, flags=re.DOTALL)
	cell = re.sub(r"\\\[(.*?)\\\]", lambda m: f"${m.group(1).strip()}$", cell, flags=re.DOTALL)
	cell = re.sub(r"\\\((.*?)\\\)", lambda m: f"${m.group(1).strip()}$", cell, flags=re.DOTALL)
	cell = re.sub(r"\$(?!\$)\s*(.*?)\s*(?<!\$)\$(?!\$)", lambda m: f"${m.group(1).strip()}$", cell, flags=re.DOTALL)

	# Protect inline math so command-stripping does not erase symbols like \Phi.
	placeholders: list[tuple[str, str]] = []

	def stash_math(match: re.Match[str]) -> str:
		token = f"__TABLE_MATH_{len(placeholders)}__"
		placeholders.append((token, match.group(0)))
		return token

	cell = re.sub(r"(?<!\$)\$(?!\$).*?(?<!\$)\$(?!\$)", stash_math, cell)
	cell = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?\{(.*?)\}", r"\2", cell)
	cell = re.sub(r"\\[a-zA-Z]+", "", cell)
	for token, original in placeholders:
		cell = cell.replace(token, original)

	# Never leave display delimiters in tables; drop empty math markers.
	cell = cell.replace("$$", "$")
	cell = re.sub(r"\$\s*\$", "", cell)
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


def cleanup_leftovers(text: str) -> str:
	# Preserve display-math env markers before generic begin/end cleanup.
	protected_math_markers: list[tuple[str, str]] = []

	def protect_math_marker(match: re.Match[str]) -> str:
		token = f"__MATH_ENV_MARKER_{len(protected_math_markers)}__"
		protected_math_markers.append((token, match.group(0)))
		return token

	text = re.sub(
		rf"\\(?:begin|end)\{{(?:{'|'.join(re.escape(env) for env in PROTECTED_MATH_ENVS)})\}}",
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


def convert_latex_to_markdown(tex: str, ctx: ConversionContext, source_tex_file: Path) -> str:
	_log(ctx, f"[{source_tex_file.name}] stage: expand macros")
	tex = expand_macros(tex, ctx.macro_rules)
	_log(ctx, f"[{source_tex_file.name}] stage: extract content")
	text = extract_real_content(tex)
	_log(ctx, f"[{source_tex_file.name}] stage: normalize styles")
	text = normalize_text_styles(text)
	text = _clear_tikz_env_empty_lines(text)
	text = _clear_asymptote_env_empty_lines(text)
	_log(ctx, f"[{source_tex_file.name}] stage: convert display math")
	text = convert_display_math(text)
	_log(ctx, f"[{source_tex_file.name}] stage: convert theorem-like blocks")
	text = convert_theorem_like(text)
	_log(ctx, f"[{source_tex_file.name}] stage: convert figures")
	text = convert_figures(text, ctx, source_tex_file)
	_log(ctx, f"[{source_tex_file.name}] stage: convert includegraphics outside figures")
	text = convert_includegraphics(text, ctx, source_tex_file)
	_log(ctx, f"[{source_tex_file.name}] stage: convert tikz blocks")
	text = convert_tikz_pictures(text, ctx, source_tex_file)
	_log(ctx, f"[{source_tex_file.name}] stage: convert asymptote blocks")
	text = convert_asymptote_blocks(text, ctx, source_tex_file)
	_log(ctx, f"[{source_tex_file.name}] stage: convert tables/lists/headings")
	text = convert_tables(text)
	text = convert_lists(text)
	text = convert_headings(text)
	_log(ctx, f"[{source_tex_file.name}] stage: finalize inline/display math spacing + cleanup")
	text = convert_inline_math(text)
	text = normalize_math_delimiter_spacing(text)
	text = normalize_display_math_blocks(text)
	text = cleanup_leftovers(text)
	_log(ctx, f"[{source_tex_file.name}] stage: markdown conversion complete")
	return text


def convert_file(tex_file: Path, ctx: ConversionContext) -> list[Path]:
	rel = tex_file.relative_to(ctx.source_dir)
	_log(ctx, f"Start file: {rel}")
	content = tex_file.read_text(encoding="utf-8", errors="ignore")
	ctx.tikz_counter = 0
	ctx.asymptote_counter = 0
	markdown = convert_latex_to_markdown(content, ctx, tex_file)

	chapter_chunks = split_by_chapter(markdown)
	written: list[Path] = []

	if chapter_chunks:
		split_dir = (ctx.output_dir / rel.parent / rel.stem)
		split_dir.mkdir(parents=True, exist_ok=True)
		_log(ctx, f"[{rel}] writing split chapters: {len(chapter_chunks)}")
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
		_log(ctx, f"[{rel}] wrote markdown: {out_path.relative_to(ctx.output_dir)}")

	_log(ctx, f"End file: {rel}")
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
		"--config",
		default="tex2md_config.json",
		help="Path to JSON config file (default: tex2md_config.json).",
	)
	parser.add_argument(
		"source",
		nargs="?",
		default=".",
		help="Source directory containing .tex files (default: current directory).",
	)
	args = parser.parse_args()

	config_path = Path(args.config)
	if not config_path.is_absolute():
		config_path = (Path.cwd() / config_path).resolve()
	initialize_config(config_path)

	source_dir = Path(args.source).resolve()
	if not source_dir.exists() or not source_dir.is_dir():
		raise SystemExit(f"Source directory does not exist: {source_dir}")

	output_dir = build_output_dir(source_dir)
	output_dir.mkdir(parents=True, exist_ok=True)
	log_path = output_dir / "tex2md.log"
	logger = ProcessLogger(log_path)
	logger.log("tex2md started")
	logger.log(f"Config path: {config_path}")
	logger.log(f"Source directory: {source_dir}")
	logger.log(f"Output directory: {output_dir}")

	graphics_source_dir = source_dir / ".."
	graphics_output_dir = output_dir / "graphics"
	graphics_output_dir.mkdir(parents=True, exist_ok=True)

	ctx = ConversionContext(
		source_dir=source_dir,
		output_dir=output_dir,
		graphics_source_dir=graphics_source_dir,
		graphics_output_dir=graphics_output_dir,
		logger=logger,
	)

	tex_files = find_tex_files(source_dir, output_dir)
	logger.log(f"Discovered tex files: {len(tex_files)}")
	if not tex_files:
		logger.log("No .tex files found.")
		logger.close()
		return

	written_files: list[Path] = []
	for tex_file in tex_files:
		written_files.extend(convert_file(tex_file, ctx))

	logger.log(f"Converted {len(tex_files)} tex files into {len(written_files)} markdown files.")
	logger.log(f"Output directory: {output_dir}")
	logger.log(f"Copied graphics: {len(ctx.copied_images)}")
	if ctx.warnings:
		logger.log("Warnings:")
		for warning in ctx.warnings:
			logger.log(f"- {warning}")
	logger.log(f"Log file: {log_path}")
	logger.log("tex2md finished")
	logger.close()


if __name__ == "__main__":
	main()
