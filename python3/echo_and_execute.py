import subprocess


def do_it(cmd, debug=0, dry=0):
    if (debug):
        print(cmd)
    if (not dry):
        subprocess.call([cmd], shell=True)

def check_output(cmd):
    cmdstr = " ".join(cmd)
    print(cmdstr)
    out = subprocess.check_output(cmd, universal_newlines=True)
    print(out, end='')
    return(cmdstr, out)

do_it("ls -al", 1)

cmdstr, output = check_output(["ls", "-al"])
