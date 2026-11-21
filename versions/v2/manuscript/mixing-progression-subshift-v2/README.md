# Neighborhood two-shadowing for progression subshifts: an extension of Moothathu (2010) answering Meddaugh–Stephens, arXiv:2509.04312v1, Section 5, Question 5.6

Haobo Ma (ChronoAI Pte Ltd, Singapore), followed by Wenlin Zhang (National University of Singapore; ChronoAI Pte Ltd, Singapore). Licensed CC BY 4.0.

Moothathu (2010), Proposition 3(iv), supplies the fixed-length progression-exclusion, zero-gap mixing and repeated-return antecedent: https://doi.org/10.4064/cm120-1-9. Kwietniak–Li–Oprocha–Ye give a later forward presentation in Proposition 4.17 of https://arxiv.org/abs/1501.01491v3. The note proves that their fixed-length example cannot trace the indicated singleton pseudo-orbits with any finite family, explaining the role of the step-dependent length here. The rotation-coding and hereditary-deletion precedents are cited separately in the PDF; no priority is claimed.

## Result

For every positive integer p, forbid all-one arithmetic progressions of difference p and length p²+3 in the one-sided binary shift. The resulting compact system is continuous, surjective and mixing, has neighborhood 2-shadowing, and has a nonempty clopen set containing no nonempty set forward invariant under any positive power of the shift. This answers Question 5.6 of Meddaugh and Stephens, arXiv:2509.04312v1, affirmatively. A word obstruction also proves that it is not of quasi-finite type (Question 5.3). The note proves failure of ordinary shadowing directly.

Corollary 4 proves the same conclusions for every integer-valued progression-length function ell(p)>=3 with ell(p)/p tending to infinity, without monotonicity. These systems have no mixing number, are not sofic, and lack specification. Corollary 5 proves that each member of the fixed tracing pair can trace at a syndetic set of times. Thus syndetic two-point tracing does not imply quasi-finite type, addressing the discussion immediately before Question 5.3. Questions 5.1–5.6 and the relevant neighboring statements are mapped in the note's coverage table.

## Files

- `note.tex`: the complete mathematical source, with its bibliography embedded.
- `note.pdf`: the typeset note, delivered alongside the source archive.
- `metadata.json`: author, license and claim metadata.
- `verify.py`: independent finite examples using Python's standard library and exact integer arithmetic.
- `checks.json`: the finite check results.

## Build

Use Tectonic 0.17.0:

```sh
tectonic note.tex
```

Or use a standard LaTeX installation containing geometry, amsmath, amssymb, amsthm, booktabs, array, fontenc, lmodern and hyperref:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

No separate BibTeX file is needed. The bibliography is embedded in `note.tex`; BibTeX is unnecessary for this source.

Run the finite examples with Python 3.11 or later:

```sh
python3 verify.py > checks.json
```

## Mathematical coverage

The note contains complete written arguments for its infinite statements. At https://github.com/the-omega-institute/trureturing/blob/d9bb8a406783c5222849b798f3c2ab738f653d75/D5/S1/Dynamics/Shadowing/ProgressionExample.lean the declaration `D5.S1.Dynamics.Shadowing.quadratic_progression_example` states compactness, continuity, surjectivity, transitivity of the product, neighborhood 2-shadowing and the periodic-set obstruction. `progression_shift_mixing` in `ProgressionSubshift.lean` states mixing. The extra quasi-finite-type and ordinary-shadowing conclusions have written proofs in the note. The finite checks illustrate the arguments over their reported ranges; they are not proofs of the infinite statements.

The PDF links all five pinned Lean files used in its coverage mapping. `QuadraticRotationHitting.lean` supplies the lower bound and quarter-interval hitting statements; `ReturnDistanceShadowing.lean` defines the fixed-set neighborhood-two-shadowing property. The superlinear tracing extension and syndetic-time conclusion have written proofs, distinct from the quadratic tracing declaration.

## Reference

Jonathan Meddaugh and Elyssa Stephens, *Shadowing With Small Diameter Sets Of Bounded Cardinality*, arXiv:2509.04312v1, 4 September 2025: https://arxiv.org/abs/2509.04312v1. The relevant locators are Definition 2.1, Definition 3.5, Proposition 4.3 and Questions 5.1–5.6.

D. Carrasco-Olivera, K. Lee, C. A. Morales and H. Villavicencio, *Finite-expansivity and N-shadowing*, Bulletin of the Brazilian Mathematical Society, New Series 53 (2022), 107–126: https://doi.org/10.1007/s00574-021-00253-w. Its Definition 1.5 is a comparison of conventions, not a proof of the neighborhood-shadowing statements here.
