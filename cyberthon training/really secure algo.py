import gmpy2
from Crypto.Util.number import bytes_to_long, long_to_bytes

p = 128785808677562889201043725021704786625425679748857424269685143553640818294468760258783217357058119328569474331389625776294460048627696865806382571012408845787917490600784383927571308416075387817905775593831794371581177358722603076688725105853034185951477893879350951987639947097259880266707731824831545988073
q = 149755963018062845575720545507627246745601179356028500178591549396645402665589195858177615208795559386366735565644306243038482729155292357735225643985678923268499544104151274109630314195513148216033970210063060808890190608788500153416694006160692745350642308667320036969902940792359169094816921645496892109441
n = p*q
e = 65537
# with open('flag.txt.encrypted', 'rb') as f:
#     c = bytes_to_long(f.read())
c = 17815667777642148965598569785460813186101176134683169780526381690321929922882961986902158041773751195935926609186811399432210224294428548995230967568734785708584085064316392923620214474739727220149587436468068823834894521739020355576933537909004199209532685402440561246157201642361473761156483211338439729048835461307274405018039155079111278674786858126762624185154930466233371779760592309869075361202129213347100038185836922888975324528017196765666570965098507255071468069839686375381198391536379491608940055366869331098161734189839758148229565329429917379261375121221042735977682627877089227743843296658319121601486
d = gmpy2.invert(e, (p - 1) * (q - 1))
m = pow(c, d, n)
byt = long_to_bytes(m)
print(byt.decode('ascii', errors='ignore'))
