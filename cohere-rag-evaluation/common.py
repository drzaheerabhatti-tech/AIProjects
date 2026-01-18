# common.py
import time

def timed(label, fn, bucket=None):
    t0 = time.time()
    out = fn()
    dt = (time.time() - t0) * 1000
    if bucket is not None:
        bucket.append(dt)
    print(f"\n[{label}] {dt:.0f} ms")
    return out

def summarize_bucket(name, bucket):
    if not bucket:
        print(f"{name}: no samples")
        return

    xs = sorted(bucket)
    n = len(xs)
    avg = sum(xs) / n
    p50 = xs[int(0.50 * (n - 1))]
    p95 = xs[int(0.95 * (n - 1))]
    mx = xs[-1]

    print(f"{name}: runs={n}  avg={avg:.0f} ms  p50={p50:.0f} ms  p95={p95:.0f} ms  max={mx:.0f} ms")
