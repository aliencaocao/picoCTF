from random import getrandbits
flag = b'actf{tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt}'

flagbits = len(flag) * 8  # len(flag) = 110
flag = int(flag.hex(),16)

q = 127049168626532606399765615739991416718436721363030018955400489736067198869364016429387992001701094584958296787947271511542470576257229386752951962268029916809492721741399393261711747273503204896435780180020997260870445775304515469411553711610157730254858210474308834307348659449375607755507371266459204680043
p = q * 2^1024 + 1  # 22839541822988239592242513354251312856142228611561079588491762559650184068095209431602625349455778047961916368945347343860469956123417607658637164070435476397037255457947126486435229957558136068691330948288556040884696250599976425227671236061926300819649941534443801676467576356649416106710085765924691992810090768738719434913627640254442013130866794698101610718594378388872899823902219125986951905693274556110441490302637988516317003159971974336016839562524349759603023972659262875761842362562877860006178151858439189522602531968167623626739605023208133351641100880231885358925191825910399671986026322808391008780289

assert p in Primes()

nbits = p.nbits()-1  # 2048 - 1 = 2047

e = getrandbits(nbits-flagbits)  # randbits(2047-880 = 1167)
e <<= flagbits
e |= flag

K = GF(p)
g = K.multiplicative_generator()
a = g^e # 3^e
print(discrete_log(a, g, K.order()-1))
print(hex(p))  # 0xb4ec8caf1c16a20c421f4f78f3c10be621bc3f9b2401b1ecd6a6b536c9df70bdbf024d4d4b236cbfcb202b702c511aded6141d98202524709a75a13e02f17f2143cd01f2867ca1c4b9744a59d9e7acd0280deb5c256250fb849d96e1e294ad3cf787a08c782ec52594ef5fcf133cd15488521bfaedf485f37990f5bd95d5796b0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001

print(g)  # 3
print(hex(a))  # 0xaf99914e5fb222c655367eeae3965f67d8c8b3a0b3c76c56983dd40d5ec45f5bcde78f7a817dce9e49bdbb361e96177f95e5de65a4aa9fd7eafec1142ff2a58cab5a755b23da8aede2d5f77a60eff7fb26aec32a9b6adec4fe4d5e70204897947eb441cc883e4f83141a531026e8a1eb76ee4bff40a8596106306fdd8ffec9d03a9a54eb3905645b12500daeabdb4e44adcfcecc5532348c47c41e9a27b65e71f8bc7cbdabf25cd0f11836696f8137cd98088bd244c56cdc2917efbd1ac9b6664f0518c5e612d4acdb81265652296e4471d894a0bd415b5af74b9b75d358b922f6b088bc5e81d914ae27737b0ef8b6ac2c9ad8998bd02c1ed90200ad6fff4a37
print(flagbits)  # 880
