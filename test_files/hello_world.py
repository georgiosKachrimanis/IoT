# this is a test for connecting my RPi virtually


def gcd(a, b):

    if b == 0 :
        return a
    else :
        print("a = ", a, "b = ", b)
        return gcd(b, a % b)



d = gcd(71, 1560)

n = 31*53
print(n)



t= 30*52
print(t)

print(gcd(71, 1560))
print(gcd(71, 1643))
print(71^(-1))
print(((1/71)%1560))
print(0.014084507042253521*71)
print((345^71)%1643)
print((112^71)%1643)
print((289^71)%1643)
print((19^71)%1643)
print("************************")
print((286^791)%1643)
print((55^791)%1643)
print((358^791)%1643)
print((84^791)%1643)