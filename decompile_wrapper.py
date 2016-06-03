
import unpyc3
import os
import sys
import traceback
import zipfile

#Edit these variables to reflect your paths.
TEMPDIR = 'c:/temp/'
SIMSINSTALLDIR = 'c:/Program Files (x86)/Origin Games/The Sims 4/'


#Don't edit anything after this line.
def unzip(installdir):

    print("Install dir: %s\n" % (SIMSINSTALLDIR))
    BASE = installdir +'Data/Simulation/Gameplay/base.zip'
    print("Unziping %s" % (BASE))
    with zipfile.ZipFile(BASE) as zf:
        zf.extractall(TEMPDIR)

    CORE = installdir +'Data/Simulation/Gameplay/core.zip'
    print("Unzipping %s" % (CORE))
    with zipfile.ZipFile(CORE) as zf:
        zf.extractall(TEMPDIR)

    SIMULATION = installdir +'Data/Simulation/Gameplay/simulation.zip'
    print("Unzipping %s" % (SIMULATION))
    with zipfile.ZipFile(SIMULATION) as zf:
        zf.extractall(TEMPDIR)
    input("Press enter to continue.")


def process_file(input_file):
              
    outputfilename = input_file + '.py'
    outputfile = open(outputfilename, 'w')

    #print("Writing to %s" % (outputfilename))
    try:
        output = str(unpyc3.decompile(input_file))
        outputfile.write(output)
        outputfile.close()
    except (AttributeError, UnicodeEncodeError):
        logfilename = os.path.join(TEMPDIR, 'error.log.txt')
        logfile = open(logfilename, 'a')
        logfile.write("Unable to decompile %s\n" % (input_file))
        tb_entries = traceback.extract_tb( sys.exc_info()[ 2 ] )
        for tb_entry in tb_entries:
            ( tb_file_name, tb_line_number, tb_function, tb_line ) = tb_entry
            ( traceback_file_name, traceback_line_number, traceback_function, traceback_line ) = traceback.extract_tb( sys.exc_info()[ 2 ] )[ -1 ]
            logfile.write( "  EXCEPTION: while decompiling file %s with (%s:%d): %s: %s \n" % ( input_file, traceback_file_name, traceback_line_number, sys.exc_info()[ 0 ], sys.exc_info()[ 1 ] ))

        logfile.close()
    

def process_subdir(subdir):
    for subdir_item in os.listdir(subdir):
        subdir_filename_fields = subdir_item.split('.')
        subdir_filename_extension = subdir_filename_fields[-1]
        if os.path.isdir(os.path.join(subdir, subdir_item)):
            subdir_subdir = os.path.join(subdir, subdir_item)
            print("Processing directory %s" % (subdir_subdir))
            process_subdir(subdir_subdir)
            
        if subdir_filename_extension == 'pyo':
            sourcepath = os.path.join(TEMPDIR, subdir, subdir_item)
            process_file(sourcepath)
            
        else:
            continue
    print("Finished processing directory %s" % (subdir))


def process_dir(input_dir):
    for dir_item in os.listdir(input_dir):
        if os.path.isdir(os.path.join(input_dir, dir_item)):
            dir_name = os.path.join(input_dir, dir_item)
            print("Processing directory %s" % dir_name)
            process_subdir(os.path.join(input_dir, dir_item))
        else:
            filename_fields = dir_item.split('.')
            dir_item_extension = filename_fields[-1]
            if dir_item_extension == 'pyo':
           
                sourcepath = os.path.join(TEMPDIR, dir_item)
                process_file(sourcepath)
                
            else:
                continue

    print("Finished processing directory %s" % (input_dir))


unzip(SIMSINSTALLDIR)

process_dir(TEMPDIR)


print("Errors written to %s%s" % (TEMPDIR, "error.log.txt"))

input( "Hit Enter or Return to exit ..." )
