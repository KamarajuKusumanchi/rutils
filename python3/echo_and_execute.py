import subprocess


def do_it(cmd, debug=1):
    if (debug):
        print(cmd)
    subprocess.call([cmd], shell=True)

def check_output(cmd):
    cmdstr = " ".join(cmd)
    print(cmdstr)
    out = subprocess.check_output(cmd, universal_newlines=True)
    print(out, end='')
    return(cmdstr, out)

do_it("ls -al")

cmdstr, output = check_output(["ls", "-al"])
