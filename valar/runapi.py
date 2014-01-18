import pycgm

def main():
    with open('hosts.txt') as ifile:
        for l in ifile.readlines():
            cgminer = pycgm.CgminerAPI(host=l.strip())
            data = cgminer.summary()
            print data

if __name__ == '__main__':
    main()
