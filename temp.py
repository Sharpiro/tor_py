__all__ = ['smult_curve25519_base', 'smult_curve25519']

P = 2 ** 255 - 19
A = 486662

def expmod(b, e, m):
  if e == 0: return 1
  t = expmod(b, e / 2, m) ** 2 % m
  if e & 1: t = (t * b) % m
  return t

def inv(x):
  return expmod(x, P - 2, P)

# Addition and doubling formulas taken from Appendix D of "Curve25519:
# new Diffie-Hellman speed records".

# def add((xn,zn), (xm,zm), (xd,zd)):
def add(a, b, c):
  x = 4 * (b[0] * a[0] - b[1] * a[1]) ** 2 * c[1]
  z = 4 * (b[0] * a[1] - b[1] * a[0]) ** 2 * c[0]
  return (x % P, z % P)

# def double((xn,zn)):
def double(a):
  x = (a[0] ** 2 - a[1] ** 2) ** 2
  z = 4 * a[0] * a[1] * (a[0] ** 2 + A * a[0] * a[1] + a[1] ** 2)
  return (x % P, z % P)

def curve25519(n, base):
  one = (base,1)
  two = double(one)
  # f(m) evaluates to a tuple containing the mth multiple and the
  # (m+1)th multiple of base.
  def f(m):
    if m == 1: return (one, two)
    (pm, pm1) = f(m / 2)
    if (m & 1):
      return (add(pm, pm1, one), double(pm1))
    return (double(pm), add(pm, pm1, one))
  ((x,z), _) = f(n)
  return (x * inv(z)) % P

def unpack(s):
  if len(s) != 32: raise ValueError('Invalid Curve25519 argument')
  return sum(s[i] << (8 * i) for i in range(32))

def pack(n):
  return ''.join([chr((n >> (8 * i)) & 255) for i in range(32)])

def clamp(n):
  n &= ~7
  n &= ~(128 << 8 * 31)
  n |= 64 << 8 * 31
  return n

def smult_curve25519(n, p):
  n = clamp(unpack(n))
  p = unpack(p)
  return pack(curve25519(n, p))

def smult_curve25519_base(n):
  n = clamp(unpack(n))
  return pack(curve25519(n, 9))
