import math
import random
import copy
from model.shapes import Cube, Sphere, Pyramid
from model.base_math_objfunction_updated import objective

# ------------------------------------------------------------
# FIXED collision function
# ------------------------------------------------------------
def collision(obj1, obj2):
    if isinstance(obj1, Sphere) and isinstance(obj2, Sphere):
        dist = math.sqrt(
            (obj1.x - obj2.x) ** 2 +
            (obj1.y - obj2.y) ** 2 +
            (obj1.z - obj2.z) ** 2
        )
        return max(0.0, (obj1.r + obj2.r) - dist)

    sx1, sy1, sz1 = obj1.half_size()
    sx2, sy2, sz2 = obj2.half_size()

    overlap_x = (sx1 + sx2) - abs(obj1.x - obj2.x)
    overlap_y = (sy1 + sy2) - abs(obj1.y - obj2.y)   # fixed
    overlap_z = (sz1 + sz2) - abs(obj1.z - obj2.z)

    if overlap_x > 0 and overlap_y > 0 and overlap_z > 0:
        return min(overlap_x, overlap_y, overlap_z)

    return 0.0


# ------------------------------------------------------------
# FIXED objective function
# ------------------------------------------------------------
def objective(objs, W, D, H, lam):
    def occupied_space(objs):
        min_x = float("inf")
        min_y = float("inf")
        min_z = float("inf")

        max_x = float("-inf")
        max_y = float("-inf")
        max_z = float("-inf")

        for o in objs:
            sx, sy, sz = o.half_size()

            min_x = min(min_x, o.x - sx)
            min_y = min(min_y, o.y - sy)
            min_z = min(min_z, o.z - sz)

            max_x = max(max_x, o.x + sx)
            max_y = max(max_y, o.y + sy)
            max_z = max(max_z, o.z + sz)

        return (max_x - min_x) * (max_y - min_y) * (max_z - min_z)

    occupied_vol = occupied_space(objs)
    penalty = 0.0

    for i in range(len(objs)):
        for j in range(i + 1, len(objs)):
            penalty += collision(objs[i], objs[j]) ** 2

    for o in objs:
        sx, sy, sz = o.half_size()

        penalty += max(0, sx - o.x) ** 2
        penalty += max(0, o.x + sx - W) ** 2

        penalty += max(0, sy - o.y) ** 2
        penalty += max(0, o.y + sy - D) ** 2

        penalty += max(0, sz - o.z) ** 2
        penalty += max(0, o.z + sz - H) ** 2

    return occupied_vol + lam * penalty

# ------------------------------------------------------------
# Random valid position
# ------------------------------------------------------------
def random_pos(o, W, D, H):
    sx, sy, sz = o.half_size()
    x = random.uniform(sx, W - sx)
    y = random.uniform(sy, D - sy)
    z = random.uniform(sz, H - sz)
    return x, y, z


# ------------------------------------------------------------
# Deep copy helper
# ------------------------------------------------------------
def clone_objects(objs):
    return copy.deepcopy(objs)


# ------------------------------------------------------------
# Small random move for one object
# ------------------------------------------------------------
def perturb_object(o, W, D, H, step=2.0):
    new_o = copy.deepcopy(o)

    new_o.x += random.uniform(-step, step)
    new_o.y += random.uniform(-step, step)
    new_o.z += random.uniform(-step, step)

    # clamp inside box
    sx, sy, sz = new_o.half_size()
    new_o.x = min(max(new_o.x, sx), W - sx)
    new_o.y = min(max(new_o.y, sy), D - sy)
    new_o.z = min(max(new_o.z, sz), H - sz)

    return new_o
 


# ------------------------------------------------------------
# Monte Carlo optimizer
# ------------------------------------------------------------
def monte_carlo_optimization(objects, W=38.0, D=28.4, H=38.0 , lam=50000, iterations=10000, step=5.0):
    #random.seed(seed)

    # start from random placement
    current = clone_objects(objects)
    for o in current:
        o.x, o.y, o.z = random_pos(o, W, D, H)

    current_score = objective(current, W, D, H, lam)

    best = clone_objects(current)
    best_score = current_score

    history = [best_score]

    for it in range(iterations):
        candidate = clone_objects(current)

        # choose one random object to move
        idx = random.randint(0, len(candidate) - 1)
        candidate[idx] = perturb_object(candidate[idx], W, D, H, step)

        candidate_score = objective(candidate, W, D, H, lam)

        # accept only if better
        if candidate_score < current_score:
            current = candidate
            current_score = candidate_score

            if candidate_score < best_score:
                best = clone_objects(candidate)
                best_score = candidate_score

        history.append(best_score)
        
    return best, best_score #, history da nur die besten appended --> nicht die volle history


# ------------------------------------------------------------
# Example run
# ------------------------------------------------------------
#if __name__ == "__main__":
#    objects = [
#        Cube(a=5.0),
#        Cube(a=3.0),
#        Sphere(r=3.0),
#        Sphere(r=2.0),
#        Pyramid(b=4.0, h=6.0),
#        Pyramid(b=3.0, h=4.0),
#    ]

#    W, D, H = 38.0, 28.4, 38.0

#    best_objects, best_score = monte_carlo_optimization(
#        objects
#    )

#    print(f"Best objective value: {best_score:.2f}")
#    print(best_objects)
#    for i, o in enumerate(best_objects):
#        print(f"Object {i+1}: x={o.x:.2f}, y={o.y:.2f}, z={o.z:.2f}")

#best_objects