def generate(n):
    from random import random
    from datetime import datetime
    from datetime import date
    import math
    pi = math.pi
    #initilaziton of the ll---------------------------------------------------------
    ll = open("data.init","w")

    #takin inputs and boundary calculation------------------------------------------

    btf = 0
    tf = 0

    #boundaries---------------------------------------------------------------------
    basepair = 4.6*10**6 #bp
    volume = 6.7*10**(-19) #m3
    bp_dens = basepair/volume #bp/m3
    realN = n*10 #my polymer bp
    sysVol = realN/bp_dens*20000#bp/(bp/m3)
    sigma = 34*10**(-10) #1 sigma corresponds to 10 bp and 10bp length is 34 armstrong
    short_side = (sysVol/2)**(1/3) #2a^3 = m3, a = (m3/2)^(1/3)
    b = short_side/sigma #converting length of short side from meters to sigmas
    r = n/(2*pi)
    rsys = r +10
    print("Converting from microomolar to Number------------------------------DONE")
    #setting up the command line of the data file-----------------------------------
    now = datetime.now()
    ct = now.strftime("%H:%M:%S")
    today = date.today()
    td = today.strftime("%d/%m/%Y")

    #writing starts here
    ll.write(str(n) +" DNA monomers ")
    ll.write(str(btf) + " binding sites ")
    ll.write("Date: " + td + " Time: " + ct)

    ll.write("\n\n") #writing starts here
    #initialization of bonds, atoms and angles--------------------------------------

    atoms = str(n) + " atoms\n"
    ll.write(atoms)
    bonds = str(n)+" bonds\n"
    ll.write(bonds)
    angles = str(n)+" angles\n\n"
    ll.write(angles)

    print("initializating of bonds, atoms and angles--------------------------DONE")
    #initialization of bond, atom and angle types-----------------------------------
    ll.write("5 atom types\n")
    ll.write("5 bond types\n")
    ll.write("2 angle types\n\n")

    print("initializating bond, atom and angle types--------------------------DONE")

    # boundaries of the system------------------------------------------------------

    xlh = str(-rsys) + " " + str(rsys) + " " + "xlo" + " " + "xhi" + "\n"
    ylh = str(-rsys) + " " + str(rsys) + " " + "ylo" + " " + "yhi" + "\n"
    zlh = str(-b/20) + " " + str(b/20) + " " + "zlo" + " " + "zhi" + "\n"

    ll.write(xlh + ylh + zlh)
    ll.write("\n")

    print("Boundaries-----------------------------------------------CALCULATED/SET")
    #mass declaration---------------------------------------------------------------
    ll.write("Masses\n\n")
    ll.write("1 1\n")
    ll.write("2 1\n")
    ll.write("3 2\n")
    ll.write("4 2\n")
    ll.write("5 2\n")
    ll.write("\n")

    print("Declaring Masses---------------------------------------------------DONE")
    #Bond Coeffs--------------------------------------------------------------------
    ll.write("Bond Coeffs\n\n")
    bond_coeff =  "1" + " " + "30.0" + " " + "1.5" + " " + "1.0" + " " + "1.0" + "\n"
    bond_coeff2 = "2" + " " + "30.0" + " " + "1.5" + " " + "1.0" + " " + "1.0" + "\n"
    bond_coeff3 = "3" + " " + "30.0" + " " + "1.5" + " " + "1.0" + " " + "1.0" + "\n"
    bond_coeff4 = "4" + " " + "30.0" + " " + "1.5" + " " + "1.0" + " " + "1.0" + "\n"
    bond_coeff5 = "5" + " " + "30.0" + " " + "2.0" + " " + "1.5" + " " + "1.5" + "\n"
    bbc = bond_coeff + bond_coeff2 + bond_coeff3 + bond_coeff4 + bond_coeff5
    ll.write(bbc)
    ll.write("\n\n")

    print("Bond Coeffs---------------------------------------------------------SET")
    #atoms--------------------------------------------------------------------------
   
    ll.write("Atoms\n\n")
    zco = 0
    for x in range(1,n+1):

        xco = math.cos(0.01 + 2*pi/n*x)*r
        yco = math.sin(0.01 + 2*pi/n*x)*r

        #setting the secondary atom type--------------------------------------------
        if (x%20 == 1):
            sec = 2
        elif (x%20 == 2):
            sec = 2
        else:
            sec = 1
        mahmut = str(x) + "\t" + str(sec) + "\t" + str(sec) + "\t" +str(xco) + "\t" + str(yco) + "\t" + str(zco) + "\n"

        ll.write(mahmut)


    print("DNA monomer coordinates---------------------------------------------SET")
    #free Tf core/site atom random position genereation-----------------------------
    # x = 0
    # y = 0
    # z = 0
    # for scx in range (n+1,n+tf*3,3):
    #     x = (b)/0.98*(random()-0.5001)
    #     y = (b)*0.49*(random()-0.5001)
    #     z = (b)*0.49*(random()-0.5001)
    #     ll.write(str(scx) + "\t" + "3" + "\t" +"3" + "\t" +str(x) + "\t" + str(y) + "\t" + str(z) + "\n")
    #     ll.write(str(scx+1) + "\t" + "5" + "\t" +"5" + "\t" + str(x-0.66) + "\t" + str(y+0.96) + "\t" + str(z+0.81) + "\n")
    #     ll.write(str(scx+2) + "\t" + "3" + "\t" +"3" + "\t" + str(x+0.66) + "\t" + str(y+0.67) + "\t" + str(z+0.48) + "\n")

    # print("TF homodimer random coordinates-------------------------------------SET")
    #bound tfs core / site atom near pormoter sites---------------------------------
    """
    oo = tf*3 + n
    r2 = r + 1.35
    zc =0
    for y in range(1,n+1):

        xc = math.cos(0.01 + 2*pi/n*y)*r2
        yc = math.sin(0.01 + 2*pi/n*y)*r2

        #setting the bound tfs atom type--------------------------------------------
        if (y%20 == 1):
            oo +=1
            bec = 4
            bagl = str(oo) + "\t" + str(bec) + "\t" + str(bec) +  "\t" +str(xc) + "\t" + str(yc) + "\t" + str(zc) + "\n"
            ll.write(bagl)
            oo +=1
            bagl2 = str(oo) + "\t" + str(5) + "\t" + str(5) +  "\t" +str(xc) + "\t" + str(yc) + "\t" + str(zc+1.0) + "\n"
            ll.write(bagl2)
        elif (y%20 == 2):
            oo +=1
            bec = 4
            bagl = str(oo) + "\t" + str(bec) + "\t" + str(bec) +  "\t" +str(xc) + "\t" + str(yc) + "\t" + str(zc) + "\n"

            ll.write(bagl)

        else:
            sec = 1

    ll.write("\n\n")

    print("Bound TF homodimer coordinates--------------------------------------SET")
    """

    #bonds--------------------------------------------------------------------------
    ll.write("\nBonds\n\n")

    for i in range(1,n):

        bid = str(i) + "\t"
        bt = "1" + "\t"
        bo = str(i) + "\t" + str(i+1) + "\n"

        ll.write(bid+bt+bo)

    lbond = str(n) + "\t" + "1" + "\t" + "1" + "\t"+ str(n)
    ll.write(lbond)
    ll.write("\n\n")

    print("Bonds for DNA polymer-----------------------------------------------SET")
    #free tf core and site atom bonds----------------------------------------------------
    # b = 0
    # for bound in range (n+1,n+tf*3+1,3):
    #     ilk = str(bound )
    #     iki = str(bound + 1)
    #     ucc = str(bound + 2)
    #     ll.write(str(bound+b) + "\t" + "5" + "\t" +ilk + "\t" + iki + "\n")
    #     ll.write(str(bound+b+1) + "\t" + "5" + "\t" +iki + "\t" + ucc + "\n")
    #     b -=1

    #print("Bonds for free TF homodimers----------------------------------------SET")
    #bound tf core and site atom bonds----------------------------------------------
    """
    b = 0
    for botf in range (n+tf*3+1,n+3*tf+btf*3+1,3):
        il = str(botf)
        ik = str(botf + 1)
        ll.write(str(botf+b) + "\t" + "5" + "\t" +il + "\t" + ik + "\n")
        uc = str(botf+2)
        ll.write(str(botf+b+1) + "\t" + "5" + "\t" +ik + "\t" + uc + "\n")
        b -=1

    print("Bonds for bound TF homodimers---------------------------------------SET")
    ll.write("\n\n")
    """

    #angles-------------------------------------------------------------------------
    ll.write("Angles\n\n")

    for j in range(1,n-1):

        aid = str(j) + "\t"
        at = "1" + "\t"
        ang = str(j) + "\t" + str(j+1) + "\t" + str(j+2) +"\n"

        ll.write(aid+at+ang)

    langle = str(n-1) + "\t" + "1" + "\t" + str(n-1) + "\t"+ str(n) +"\t"+ "1" "\n"
    langle2 = str(n) + "\t" + "1" + "\t" + str(n) + "\t" "1" +"\t"+ "2" + "\n"
    ll.write(langle + langle2)

    print("DNA polymer Angles--------------------------------------------------SET\n\n")

    #angles for freeTFs-----------------------------------------------------------
    # ff = 0
    # for k in range (1,tf +1):
    #     index = n + k
    #     lb = str(index+ff) + "\t" + str(index+ff+1) + "\t" + str(index+ff+2)
    #     ff +=2
    #     ll.write(str(index) + "\t" + "2" + "\t" + lb + "\n")

    #angles for boundTF-----------------------------------------------------------
    #kk = 0
    """
    for d in range(1,btf+1):
        index = n + tf + d
        index1 = n +tf*3 +d
        agar = str(index1+kk) + "\t" + str(index1+kk+1) + "\t" + str(index1+kk+2)
        kk+=2
        ll.write(str(index) + "\t" + "2" + "\t" + agar + "\n")

    print("--------------ALL DONE and DATA FILE is READY TO GO--------------------")
    ll.close()
    print("\n\n")
    """
    return

def inputfile():
    tt = open("in.init","w")
    tt.write("units lj\n")
    tt.write("dimension 3\n")
    tt.write("boundary p p p\n\n")

    tt.write("atom_style angle\n")
    tt.write("pair_style lj/cut 2.5\n")
    tt.write("pair_modify shift yes\n")
    tt.write("bond_style fene\n")
    tt.write("angle_style harmonic\n\n")

    tt.write("special_bonds lj 0.0 1.0 1.0 coul 0.0 1.0 1.0\n\n")

    tt.write("read_data data.init\n\n")

    tt.write("pair_coeff * * 12.0 1.0\n")
    tt.write("pair_coeff 2 4 10.0 1.0 2.5\n\n")

    tt.write("angle_coeff 1 1.0 109.5\n")
    tt.write("angle_coeff 2 12.0 40.0\n\n")

    tt.write("neighbor 0.4 bin\n")
    tt.write("neigh_modify delay 10\n\n")

    tt.write("timestep      0.005\n\n")

    tt.write("thermo_style  multi\n")
    tt.write("thermo        5000\n\n")

    tt.write("fix           1 all nvt temp 1.0 1.0 0.5\n")
    tt.write("fix           2 all langevin 1.0 1.0 0.5 7213981\n\n")

    tt.write("minimize      0.0001 0.000001 100 1000\n\n")

    tt.write("run           20000000\n\n")

    tt.write("write_data    data.collapse")

    print("DONE")

    return