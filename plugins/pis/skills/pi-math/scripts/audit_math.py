#!/usr/bin/env python3
"""Candidate-level notation audit for Markdown containing TeX math."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


MATH_RE = re.compile(
    r"\\\[(?P<bracket>.*?)\\\]|\$\$(?P<dollar>.*?)\$\$|\\\((?P<inline>.*?)\\\)",
    re.DOTALL,
)
SYMBOL_RE = re.compile(
    r"(?:\\(?:mathcal|mathbb|mathbf|mathrm)\s*\{[^{}]+\}|\\[A-Za-z]+|(?<!\\)[A-Za-z])"
    r"(?:\s*[_^](?:\{[^{}]*\}|\\[A-Za-z]+|[A-Za-z0-9]))*"
)
INTRO_BEFORE_RE = re.compile(
    r"\b(?:let|where|with|write|denote|denotes|called|define|defined|set|represented by|"
    r"parameters?|variables?|indices|constants?|densit(?:y|ies)|potentials?|functions?|"
    r"operators?|domains?|regions?|surfaces?|basins?|states?|variants?|temperature)\b",
    re.IGNORECASE,
)
STRONG_INTRO_RE = re.compile(
    r"\b(?:let|where|write|denote|denotes|define|defined|set|represented by)\b",
    re.IGNORECASE,
)
ENUMERATION_RE = re.compile(
    r"\b(?:the|following)\b[^.!?]*(?:parameters|variables|indices|constants|densities|"
    r"potentials|functions|operators|domains|regions|surfaces|basins|states|variants)"
    r"\s*[,:]\s*$",
    re.IGNORECASE,
)
INTRO_AFTER_RE = re.compile(r"^\s*(?:is|are|denotes?|represents?|means?)\b", re.IGNORECASE)

IGNORED_COMMANDS = {
    "begin", "end", "boxed", "left", "right", "big", "Big", "bigg", "Bigg",
    "frac", "tfrac", "dfrac", "sqrt", "text", "operatorname", "mathrm", "mathbf",
    "mathcal", "mathbb", "rm", "bf", "tag", "label", "ref", "eqref", "qquad",
    "quad", "hspace", "vspace", "phantom", "underbrace", "overbrace", "overline",
    "bar", "hat", "tilde", "dot", "ddot", "vec", "boldsymbol", "substack",
    "begin", "end", "aligned", "array", "cases", "split", "gathered", "matrix",
    "cdot", "times", "otimes", "oplus", "pm", "mp", "le", "leq", "ge", "geq",
    "ll", "gg", "neq", "approx", "simeq", "sim", "propto", "equiv", "in", "notin",
    "subset", "subseteq", "supset", "supseteq", "cup", "cap", "setminus", "to",
    "rightarrow", "leftarrow", "mapsto", "iff", "implies", "forall", "exists",
    "neg", "land", "lor", "wedge", "vee", "nabla", "partial", "Delta", "delta",
    "sum", "prod", "int", "iint", "iiint", "oint", "lim", "min", "max", "inf",
    "sup", "ln", "log", "exp", "sin", "cos", "tan", "sinh", "cosh", "tanh",
    "det", "ker", "dim", "tr", "Re", "Im", "Pr", "arg", "mod", "pmod",
    "langle", "rangle", "lVert", "rVert", "vert", "mid", "infty", "emptyset",
    "dagger", "ddagger", "circ", "ast", "star", "prime", "nonumber", "pi",
    "ldots", "cdots", "dots",
}
IGNORED_BASES = {"d", "e", "i", "j", "cal:R", "bb:R", "bb:C", "bb:N", "bb:Z"}
WILDCARD_SUBSCRIPTS = {"i", "j", "k", "s", "v"}


@dataclass(frozen=True)
class Span:
    start: int
    end: int
    line: int
    tex: str
    display: bool


def canonical(raw: str) -> str:
    raw = re.sub(r"\s+", "", raw)
    raw = re.sub(r"\\mathrm\{([^{}]+)\}", r"\1", raw)
    raw = re.sub(r"\\mathbf\{([^{}]+)\}", r"\1", raw)
    raw = re.sub(r"\\mathcal\{([^{}]+)\}", r"cal:\1", raw)
    raw = re.sub(r"\\mathbb\{([^{}]+)\}", r"bb:\1", raw)
    return raw


def base_of(symbol: str) -> str:
    return re.split(r"[_^]", symbol, maxsplit=1)[0]


def meaningful(raw: str) -> bool:
    symbol = canonical(raw)
    base = base_of(symbol)
    if base.startswith("\\") and base[1:] in IGNORED_COMMANDS:
        return False
    return base not in IGNORED_BASES and not base.isdigit()


def clean_tex(tex: str) -> str:
    previous = None
    while tex != previous:
        previous = tex
        tex = re.sub(r"\\(?:text|operatorname)\s*\{[^{}]*\}", "", tex)
    tex = re.sub(r"\\(?:begin|end)\s*\{[^{}]*\}", "", tex)
    tex = re.sub(
        r"\\(bar|hat|tilde|vec|dot|ddot|overline)\s*(?:\{(\\[A-Za-z]+|[A-Za-z])\}|(\\[A-Za-z]+|[A-Za-z]))",
        lambda match: f"{match.group(2) or match.group(3)}^{{{match.group(1)}}}",
        tex,
    )
    tex = re.sub(r"\\(?:tag|label)\s*\{[^{}]*\}", "", tex)
    tex = re.sub(r"\\(?:mathrm|mathbf)\s*\{([^{}]+)\}", r"\1", tex)
    tex = re.sub(r"\\(?:mathrm|mathbf)\s*([A-Za-z])", r"\1", tex)
    tex = re.sub(r"\\mathcal\s*\{([A-Za-z])\}", r"\1", tex)
    tex = re.sub(r"\\mathcal\s*([A-Za-z])", r"\1", tex)
    # Preserve integration domains; otherwise they are swallowed as \int's subscript.
    tex = re.sub(r"\\(?:int|iint|iiint|oint)\s*_\s*\{([^{}]+)\}", r" \1 ", tex)
    return tex


def symbols(tex: str) -> list[tuple[str, int, int]]:
    clean = clean_tex(tex)
    return [
        (canonical(match.group()), match.start(), match.end())
        for match in SYMBOL_RE.finditer(clean)
        if meaningful(match.group())
    ]


def spans(text: str) -> list[Span]:
    result = []
    for match in MATH_RE.finditer(text):
        tex = next(value for value in match.groupdict().values() if value is not None)
        result.append(
            Span(
                match.start(),
                match.end(),
                text.count("\n", 0, match.start()) + 1,
                tex,
                match.group("inline") is None,
            )
        )
    return result


def split_symbol(symbol: str) -> tuple[str, list[tuple[str, str]]]:
    base = base_of(symbol)
    decorations = []
    for match in re.finditer(r"([_^])(?:\{([^{}]*)\}|(\\[A-Za-z]+|[A-Za-z0-9]+))", symbol[len(base):]):
        decorations.append((match.group(1), match.group(2) or match.group(3)))
    return base, decorations


def template_matches(template: str, candidate: str) -> bool:
    left_base, left_parts = split_symbol(template)
    right_base, right_parts = split_symbol(candidate)
    if left_base != right_base or len(left_parts) != len(right_parts):
        return False
    for (left_kind, left), (right_kind, right) in zip(left_parts, right_parts):
        if left_kind != right_kind:
            return False
        left_items = left.split(",")
        right_items = right.split(",")
        if len(left_items) != len(right_items):
            return False
        for left_item, right_item in zip(left_items, right_items):
            if left_item in WILDCARD_SUBSCRIPTS:
                if not re.fullmatch(r"[A-Za-z]|\\[A-Za-z]+", right_item):
                    return False
            elif left_item != right_item:
                return False
    return True


def definitions(span: Span) -> list[dict]:
    clean = clean_tex(span.tex)
    found = []
    for symbol, start, end in symbols(clean):
        relation = re.match(
            r"\s*(?:\([^)]*\))?\s*(?P<relation>&?=|\\equiv|\\coloneqq|:=)",
            clean[end:],
        )
        if not relation:
            continue
        clause_start = max(clean.rfind("\n", 0, start), clean.rfind(";", 0, start)) + 1
        if symbols(clean[clause_start:start]):
            continue
        rhs_start = end + relation.end()
        rhs = re.split(r"\\\\|\\qquad|;", clean[rhs_start:], maxsplit=1)[0].strip()
        found.append(
            {
                "symbol": symbol,
                "line": span.line,
                "position": span.start,
                "relation": relation.group("relation").lstrip("&"),
                "rhs": rhs,
            }
        )
    return found


def introduced_by_context(text: str, span: Span) -> bool:
    before = text[max(0, span.start - 140):span.start]
    after = text[span.end:min(len(text), span.end + 80)]
    if span.display:
        return bool(
            STRONG_INTRO_RE.search(before)
            or ENUMERATION_RE.search(before)
            or INTRO_AFTER_RE.search(after)
        )
    before = re.split(r"[.!?]\s|\n\n", before)[-1]
    return bool(INTRO_BEFORE_RE.search(before) or INTRO_AFTER_RE.search(after))


def immediate_after(text: str, span: Span, symbol: str, introductions: dict[str, list[int]]) -> bool:
    tail = text[span.end:min(len(text), span.end + 260)]
    paragraph = tail.split("\n\n", 1)[0]
    if not re.search(r"\bwhere\b", paragraph, re.IGNORECASE):
        return False
    return any(span.end <= position <= span.end + len(paragraph) for position in introductions.get(symbol, []))


def bound_symbols(tex: str) -> set[str]:
    bound = set()
    for match in re.finditer(r"\\(?:sum|prod)\s*_\s*(?:\{)?([A-Za-z]|\\[A-Za-z]+)", tex):
        bound.add(canonical(match.group(1)))
    for symbol, _, end in symbols(tex):
        if re.match(r"\s*\\in\b", tex[end:]):
            bound.add(symbol)
    return bound


def audit(text: str) -> dict:
    math = spans(text)
    all_occurrences: dict[str, list[tuple[int, int]]] = defaultdict(list)
    introductions: dict[str, list[int]] = defaultdict(list)
    definition_rows = []

    for span in math:
        span_symbols = symbols(span.tex)
        for symbol, _, _ in span_symbols:
            all_occurrences[symbol].append((span.start, span.line))
        for row in definitions(span):
            definition_rows.append(row)
            introductions[row["symbol"]].append(span.start)
        if introduced_by_context(text, span):
            for symbol, _, _ in span_symbols:
                introductions[symbol].append(span.start)

    issues = []
    seen_issues = set()
    known: list[tuple[str, int]] = []
    for span in math:
        contextual_introductions = {
            symbol for symbol, _, _ in symbols(span.tex)
        } if introduced_by_context(text, span) else set()
        local_definitions = {row["symbol"] for row in definitions(span)} | contextual_introductions
        local_bound = bound_symbols(span.tex)
        for symbol, _, _ in symbols(span.tex):
            if symbol in local_definitions or symbol in local_bound:
                continue
            if any(position <= span.start and template_matches(template, symbol) for template, position in known):
                continue
            if immediate_after(text, span, symbol, introductions):
                continue
            later = [
                position
                for template, positions in introductions.items()
                if template_matches(template, symbol)
                for position in positions
                if position > span.start
            ]
            key = ("unresolved", symbol)
            if key not in seen_issues:
                issues.append(
                    {
                        "kind": "forward-definition" if later else "undefined-candidate",
                        "symbol": symbol,
                        "line": span.line,
                        "severity": "warning" if later else "error",
                    }
                )
                seen_issues.add(key)
        for symbol in local_definitions:
            known.append((symbol, span.start))
        if introduced_by_context(text, span):
            known.extend((symbol, span.start) for symbol, _, _ in symbols(span.tex))

    definition_symbols = {row["symbol"] for row in definition_rows}
    for row in definition_rows:
        rhs_symbols = [symbol for symbol, _, _ in symbols(row["rhs"]) if symbol != row["symbol"]]
        uses = sum(1 for position, _ in all_occurrences[row["symbol"]] if position > row["position"])
        row["uses_after_definition"] = uses
        row["rhs_symbols"] = sorted(set(rhs_symbols))
        row["candidate"] = "inline" if uses <= 1 and len(set(rhs_symbols)) <= 3 else "keep-or-review"

    by_symbol: dict[str, set[str]] = defaultdict(set)
    for row in definition_rows:
        if row["relation"] != "=":
            by_symbol[row["symbol"]].add(re.sub(r"\s+", "", row["rhs"]))
    for symbol, right_sides in by_symbol.items():
        if len(right_sides) > 1:
            issues.append({"kind": "possible-collision", "symbol": symbol, "severity": "warning"})

    combined_math = "\n".join(span.tex for span in math)
    particle_scale = re.search(r"k\s*_\s*\{?\s*B", clean_tex(combined_math))
    molar_scale = re.search(r"(?<![A-Za-z])R\s*T(?![A-Za-z])", clean_tex(combined_math))
    if particle_scale and molar_scale:
        issues.append(
            {
                "kind": "unit-convention",
                "symbols": ["k_B", "R"],
                "severity": "warning",
                "message": "Both particle-scale k_B T and molar-scale RT occur; state or reconcile the convention.",
            }
        )

    graph = {
        row["symbol"]: [symbol for symbol in row["rhs_symbols"] if symbol in definition_symbols]
        for row in definition_rows
    }

    def depth(symbol: str, path: frozenset[str] = frozenset()) -> int:
        if symbol in path:
            return 0
        return 1 + max((depth(child, path | {symbol}) for child in graph.get(symbol, [])), default=0)

    counts = Counter(symbol for span in math for symbol, _, _ in symbols(span.tex))
    return {
        "issues": issues,
        "definitions": definition_rows,
        "metrics": {
            "equations": sum(span.display for span in math),
            "definitions": len(definition_rows),
            "unique_semantic_symbols": len(counts),
            "single_occurrence_symbols": sum(count == 1 for count in counts.values()),
            "max_definition_chain": max((depth(symbol) for symbol in graph), default=0),
        },
        "note": "Regex audit: confirm candidates semantically; never add notation merely to clear a warning.",
    }


def self_test() -> None:
    sample = r"""
Let \(n\) be positive and let \(x_i\) be data.
\[N=\sum_{i=1}^n x_i.\]
\[M=\frac{1}{n}N.\]
The result is \(M\). Under \(|\beta z_i e\phi|\ll1\), continue.
\[\beta=(k_{\mathrm B}T)^{-1}.\]
\[\Delta G=-RT\ln k.\]
\[\int_{\Omega_E}\rho_E(\mathbf r)\,d\mathbf r.\]
\[H=G_{\mathrm{self/reaction}}^\ddagger.\]
"""
    report = audit(sample)
    assert any(row["symbol"] == "M" and row["candidate"] == "inline" for row in report["definitions"])
    assert any(row.get("symbol") == "z_i" for row in report["issues"])
    assert any(row.get("symbol") == "\\Omega_E" for row in report["issues"])
    assert any(row.get("symbol") == "G_{self/reaction}^\\ddagger" for row in report["issues"])
    assert any(row["kind"] == "unit-convention" for row in report["issues"])
    good = audit(
        r"Let \(n\) be positive and \(x_i\) be data for \(i=1,\ldots,n\). "
        r"Define \[\bar{x}=\frac1n\sum_{i=1}^n x_i.\]"
    )
    assert not good["issues"]
    assert any(row["symbol"] == "x^{bar}" for row in good["definitions"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", help="Markdown file; omit to read stdin")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        print("ok")
        return 0
    text = Path(args.path).read_text(encoding="utf-8") if args.path else sys.stdin.read()
    json.dump(audit(text), sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
