import subprocess


def do_it(cmd, debug=False, dry=False):
    if (debug):
        print(cmd)
    if (not dry):
        subprocess.call([cmd], shell=True)


do_it("ls -al", True)


def check_output(cmd):
    cmdstr = " ".join(cmd)
    print(cmdstr)
    out = subprocess.check_output(cmd, universal_newlines=True)
    print(out, end='')
    return(cmdstr, out)


print("")
cmdstr, output = check_output(["ls", "-al"])


# This function is inspired from
# https://github.com/harelba/q/blob/master/test/test-suite
# It returns 3 items: returncode, output, error. Both output and error are
# arrays with each element corresponding to one line.
def run_command(cmd_to_run, debug=False):
    from subprocess import PIPE, Popen
    import os

    if (debug):
        # If the command contains newline characters, we want to print it as \n
        # instead of printing a new line character. This is achieved by repr()
        print(repr(cmd_to_run))

    p = Popen(cmd_to_run, stdout=PIPE, stderr=PIPE, shell=True)
    o, e = p.communicate()
    # remove last newline
    o = o.decode().rstrip()
    e = e.decode().strip()
    # split rows
    if o != '':
        o = o.split(os.linesep)
    else:
        o = []
    if e != '':
        e = e.split(os.linesep)
    else:
        e = []

    if (debug):
        print("returncode:", p.returncode)
        print("output:", o)
        print("error:", e)
    return (p.returncode, o, e)


print("")
retcode, output, error = run_command("seq 1 10 | tr '\n' ', '", debug=True)
print("")
retcode, output, error = run_command('ls | grep py', debug=True)
