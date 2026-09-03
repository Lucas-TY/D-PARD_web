# D-PARD Web Brief Design

## Goal

Create a concise, English-only technical page for D-PARD that can be shared
with external research teams. The page follows the argument and evidence in
the current D-PARD paper while borrowing the readable, long-form presentation
style of the D-Cut documentation page.

## Audience and message

The audience is researchers who know speculative decoding but have not seen
D-PARD. The page should communicate one message: exact TV acceptance should
determine where training effort matters, while Direct Rényi-half supplies a
stronger local distribution-fitting direction.

## Information architecture

1. Hero and TL;DR: define D-PARD and report the T0/T1 gains over the original
   static CE+TV objective.
2. TV and existing remedies: explain exact stochastic acceptance, weak TV
   gradients at initialization, fused CE/KL+TV objectives, gradient conflict,
   and the gradient reallocation induced by log acceptance.
3. Acceptance certificate: state and prove the Rényi-TV lower bound before
   using it in the method.
4. D-PARD method: explain TV-derived detached position credit as cumulative
   reach times continuation value, then define the Direct Rényi-half local loss.
5. Evidence: show the six-benchmark table and the position-wise acceptance
   certificate without dense numeric narration.
6. Minimal loss code: show only the core static CE+TV and dynamic D-PARD loss
   computations, with no internal framework or commit references.

## Visual design

- A narrow top bar, generous white space, and a sticky right-side table of
  contents evoke the reference documentation page without copying its content.
- Soft blue, peach, green, and cream accents match the paper figures.
- Use the three existing English figures: gradient conflict, position credit,
  and position-wise acceptance lower bound.
- Tables use minimal rules and restrained highlighting.
- Desktop uses article plus contents rail; mobile collapses to one column.

## Technical design

- Plain HTML and CSS; no framework, package manager, build step, or custom
  runtime JavaScript. MathJax is the only page script.
- MathJax renders equations from a public CDN, with readable raw TeX as a
  fallback before loading.
- Figures are copied from the paper source into `assets/` so the site is
  self-contained apart from MathJax.
- A standard-library Python test parses the HTML and verifies the content and
  asset contract.
- Local preview uses `python3 -m http.server`.

## Content constraints

- English only.
- No confidence extension, internal codebase details, commit identifiers, or
  exhaustive protocol provenance.
- Do not call Rényi-half an acceptance probability. It is a local divergence
  whose value yields a certified lower bound on exact acceptance.
- Keep all claims aligned with the current paper and verified benchmark table.
