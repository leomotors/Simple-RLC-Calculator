
# * Range where if the different of real imag is more than this,
# * Complex Number will have the small part become 0
ACCEPTABLE_RANGE = 10**6


def RoundComplex(z: complex):
    if abs(z.real) > abs(ACCEPTABLE_RANGE * z.imag):
        return z.real
    elif abs(z.imag) > abs(ACCEPTABLE_RANGE * z.real):
        return z.imag * 1j

    return z
