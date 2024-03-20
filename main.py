import random


# y**2 = x**3 + a * x + b
def add_points(P, Q, p):
    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and y1 == y2:
        beta = (3 * x1 * x2 + a) * pow(2 * y1, -1, p)
    else:
        beta = (y2 - y1) * pow(x2 - x1, -1, p)

    x3 = (beta * beta - x1 - x2) % p
    y3 = (beta * (x1 - x3) - y1) % p

    is_on_curve((x3, y3), p)

    return x3, y3


def is_on_curve(P, p):
    x, y = P
    assert (y * y) % p == (pow(x, 3, p) + a * x + b) % p


def apply_double_and_add_method(G, k, p):
    target_point = G

    k_binary = bin(k)[2:]  # 0b1111111001

    for i in range(1, len(k_binary)):
        current_bit = k_binary[i: i + 1]

        # doubling - always
        target_point = add_points(target_point, target_point, p)

        if current_bit == '1':
            target_point = add_points(target_point, G, p)

    is_on_curve(target_point, p)

    return target_point


# Secp256k1
a = 0
b = 7
G = (55066263022277343669578718895168534326250603453777594175500187360389116729240,
     32670510020758816978083085130507043184471273380659243275938904335757337482424)
p = pow(2, 256) - pow(2, 32) - pow(2, 9) - pow(2, 8) - pow(2, 7) - pow(2, 6) - pow(2, 4) - pow(2, 0)
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337

is_on_curve(G, p)

# Elliptic Curve ElGamal

# alice
ka = random.getrandbits(256)  # private of Alice
Qa = apply_double_and_add_method(G=G, k=ka, p=p)

# Encryption

# bob
m = 23061912
s = apply_double_and_add_method(G=G, k=m, p=p)

r = random.getrandbits(128)
c1 = apply_double_and_add_method(G=G, k=r, p=p)

c2 = apply_double_and_add_method(G=Qa, k=r, p=p)
c2 = add_points(c2, s, p)

# Decryption

# s_prime = c2 - ka * c1
# s_prime = c2 + (-ka * c1)
# (x, y) + (x, -y) = 0

c1_prime = c1[0], (-1 * c1[1]) % p

s_prime = apply_double_and_add_method(G=c1_prime, k=ka, p=p)
s_prime = add_points(P=c2, Q=s_prime, p=p)

print(s_prime, s)
