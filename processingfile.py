# starting function
# tui commands in strings
chCN = "/solve/set/c-n "
# hyperdrive directoryies
fluentfolder = r'H:\VortexTube\CFD - Cavender Vortex tube\RunningFolder'
readcasefile = 'rc "' + fluentfolder + "\Read CaseData Files\\"
readdatafile = 'rd "' + fluentfolder + "\Read CaseData Files\\"


def startjournal(casefile, datafile):
    output = "; Journal File created in python for fluent input" + "\n" + \
        "chdir\nchdir Desktop\Working Directory" + "\n" + "pwd" + "\n" + \
        readcasefile + casefile + '"' + "\n" + \
        readdatafile + datafile + '"' + "\n" + \
        "/solve/set/s-s no" + "\n" + \
        "/solve/set/f-w no\n" + \
        "/define/models/solver/d-b-i yes\n"  # set to the implicit solver
    return output


def defineparameters(parameter_string, parameter_value):
    parameters_tui_command = "/define/parameters/input-parameters/edit"
    output = parameters_tui_command + ' "' + str(parameter_string) + '" "' + str(parameter_string) + '" ' + \
             str(parameter_value)
    return output


def inputp(numpa):
    output = defineparameters("Input Pressure", numpa)
    return output


def hotoutp(numpa):
    output = defineparameters("Hot Outlet Pressure", numpa)
    return output


def coldoutp(numpa):
    output = defineparameters("Cold Outlet Pressure", numpa)
    return output


def inputt(numk):
    output = defineparameters("Inlet Temperature", numk)
    return output


def runnum(batch_num, run_num):
    if batch_num >= 100:
        output1 = "" + str(batch_num)
    elif batch_num >= 10:
        output1 = "0" + str(batch_num)
    else:
        output1 = "00" + str(batch_num)
    if run_num >= 100:
        output2 = "_" + str(run_num)
    elif run_num >= 10:
        output2 = "_0" + str(run_num)
    else:
        output2 = "_00" + str(run_num)
    finaloutput = output1 + output2
    return finaloutput


def export(batch_num, run_num):
    number = runnum(batch_num, run_num)
    out1 = 'wc "' + fluentfolder + '\CaseData Files\Case_' + number + '" ok\n'
    out2 = 'wd "' + fluentfolder + '\CaseData Files\Case_' + number + '" ok\n'
    out3 = '/report/summary yes "' + fluentfolder + '\Report Files\Report_' + number + '.sum" ok\n'
    out4 = '/define/parameters/o-p/w-a-t-f "' + fluentfolder + '\Parameter Files\Parameters_' + number + '.out" yes'
    exported = out1+out2+out3+out4
    return exported


def single_run_script(batch_number, run_number, output_hot_pressure):
    firstline = "; run " + runnum(batch_number, run_number) + \
                ".........................................................................................."
    changed_parameters = '\n' + hotoutp(output_hot_pressure) + '\n'
    iterations = chCN + ".1\n" + "it 500\n" + \
                 chCN + "1\n" + "it 2000\n" + \
                 chCN + "5\n" + "it 100000\n"
    export_results = export(batch_number, run_number)

    return firstline + changed_parameters + iterations + export_results + "\n"


# define parameters here for the journal file


b_num = str("017")  # batch number (includes three characters)
cores = 5  # number of cores used on a run
read_filename = "In13898KpaPr2CF25"
starting_hot_pressure = 7469242
increment = 19000
sweep_direction = "down"
runs_in_batch = 5

f = open("Journal_" + b_num + ".JOU", "w")
f.write(str(startjournal(read_filename + ".cas", read_filename + ".dat")))
for x in range(0, runs_in_batch):
    if sweep_direction.lower() == "down":
        hot_pressure = starting_hot_pressure - x * increment
    elif sweep_direction.lower() == "up":
        hot_pressure = starting_hot_pressure + x * increment
    else:
        print("error: select either up or down for sweep direction")
    f.write(str(single_run_script(int(b_num), (x+1), hot_pressure)))
f.write("exit\nyes")  # exit fluent

b = open("Batch_" + b_num + ".bat", "w")
b.write("TITLE Vortex Tube Fluent Batch " + b_num + "\n"
        r"cd C:\Program Files\ANSYS Inc\v171\fluent\ntbin\win64\ " + "\n" + \
        "fluent 2ddp -t" + str(cores) + " -g -i \"" + fluentfolder + '\BatchJournal Files\Journal_' + b_num + '.JOU"')
f.close()
b.close()