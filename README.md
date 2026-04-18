# 3D Irregular Packing Optimization for 3D Printing

## Problem Definition

This project addresses a **3D Irregular Packing Problem** — determining how to place a set of geometrically distinct objects into a fixed 3D print volume while minimizing the unused (empty) space between the objects.

Unlike the classical *Bin Packing Problem*, which deals exclusively with uniform rectangular objects, this problem involves objects of 3 different shapes. This increases the problem's complexity, as collision detection and spatial constraints depend on the specific combinations of each object pair.

The objects considered in this project are:

- **Cube** — axis-aligned box with side length `a`
- **Sphere** — round object with radius `r`
- **Square Pyramid** — pyramid with base length `b` and height `h`

---

## Objective Function

The goal is to find a placement configuration `P = {(x₁,y₁,z₁), ..., (xₙ,yₙ,zₙ)}` for all `n` objects that minimizes the wasted space inside the print volume.

Since object volumes are fixed (shapes and sizes do not change), minimizing empty space is equivalent to finding the most **compact, non-overlapping arrangement**.

The objective function is formulated as a **penalty-based formula**:
```
f(P) = V_control + λ · (overlap_penalty + boundary_penalty)
```

Where:
- `V_control` — volume of bounding box enclosing all objects (to be minimized)
- `overlap_penalty = Σᵢ＜ⱼ collision(i, j)²` — penalizes objects intersecting each other
- `boundary_penalty` — penalizes objects placed outside the print volume
- `λ` — weighting factor for constraint violations

### Volume Formulas

| Shape    | Formula              |
|----------|----------------------|
| Cube     | `V = a³`             |
| Sphere   | `V = (4/3) · π · r³` |
| Pyramid  | `V = (1/3) · b² · h` |

---

## Collision Detection

Because objects have different shapes, the collision detection strategy depends on the type combination:

- **Sphere–Sphere**: exact Euclidean distance check
  `overlap = (r₁ + r₂) − √(Δx² + Δy² + Δz²)`

- **All other combinations** (Cube–Cube, Cube–Pyramid, Sphere–Pyramid, etc.): conservative **AABB** (Axis-Aligned Bounding Box) approximation

---
## Optimization Algorithms

This project implements three optimization algorithms:

- **Monte Carlo Optimization (MC)**
- **Simulated Annealing (SA)**
- **Genetic Algorithm**

All algorithms operate on the same objective function, while taking different approaches to exploring the solution space.
They are evaluated through repeated experiments using pipeline.py:
- runs each algorithm multiple times
- records objective scores and runtime
- generates visualtizations of object placement
- exports results for further analysis
