#!/usr/bin/python
# coding: utf-8

""" compose melody from parameter packet """

# python libs
import sys
import shutil
import os.path

# our modules
print "importing paramIO\n"
import paramIO
print "importing Pitch\n"
import pitch
print "importing score\n"
import score
print "importing vocal\n"
import vocal
print "importing melodyio\n"
import melodyio # for first generated melody dump
print "importing output\n"
import output
print "importing pregenrhythm\n"
import pregenrhythm
print 'Done importing...\n'

# Import necessary binaries into PATH on mac /Parham
import os
os.environ["PATH"] += ":/Users/pfh/skald/src/orpheus_v3.4/bin"

SKALD_FORMAT = "stdout"
# SKALD_FORMAT = "python"
def _main():
    
    # read parameter packet
    compositionID = "samples/sample.pk"
    params = paramIO.read(compositionID)
    # execute composition for each composition division ( 8 bars )
    # and then append into list
    composition_data_list = [] # list which composed data are appended
    div = int(params["div"]) # obtain number of divisions
    # for each division
    params["skald_format"] = SKALD_FORMAT
    print "Number of sections is: ",div 
    for n in range(1,div+1):
        # prepare constraints for composing melody
        melodyinfo, compose_melody = pitch.prepare( params, n ) 
        preparedrhythm = pregenrhythm.prepare( params, n )
        if preparedrhythm:
            melodyinfo["melody"] = preparedrhythm

        if compose_melody:
            composed_data, entropy = pitch.design(melodyinfo, params, n)
            melodyinfo["melody"] = composed_data
            sys.stderr.write("div:"+str(n)+" entropy="+str(entropy)+"\n")
        else:
            sys.stderr.write("div:"+str(n)+" (instrumental)\n")
        data = melodyinfo
        data.update( {"compose_melody":compose_melody} )

        # append composed info into list
        composition_data_list.append( data )
        
    ## loop for each division ends here ##

    sys.stderr.write("generating accompaniment wav file and score ..\n")
    accmpwav_fname, accompmid_fname, figure_fname = score.create( composition_data_list, params )
    sys.stderr.write("generating vocal wav file ..\n")
    vocalwav_fname = vocal.create( composition_data_list, params )
    sys.stderr.write("mix and encoding ..\n")
    wavfname, mp3fname = output.sound( vocalwav_fname, accmpwav_fname )
    sys.stderr.write("encoding score in jpg ..\n")
    jpgfname = output.figure( figure_fname )
    # output.filecopy( compositionID, mp3fname, accompmid_fname, figure_fname+".pdf", figure_fname+".ps", jpgfname, figure_fname+".ly", mode="LOCALmode" )
    sys.stderr.write("FILE TMP Location: "+vocalwav_fname+" "+mp3fname+" "+jpgfname+"\n\n")
    move_files(vocalwav_fname, mp3fname, jpgfname)

def move_files(wav_path, mp3_path, jpg_path):
    if os.path.isfile(wav_path):
        sys.stderr.write("Moving tmp wav file at {0}\n".format(wav_path))
        shutil.move(wav_path,"/Users/pfh/skald/src/orpheus_v3.4/output/{0}/orpheus_{0}.wav".format(SKALD_FORMAT))
    if os.path.isfile(mp3_path):
        sys.stderr.write("Moving tmp mp3 file at {0}\n".format(mp3_path))
        shutil.move(mp3_path,"/Users/pfh/skald/src/orpheus_v3.4/output/{0}/orpheus_{0}.mp3".format(SKALD_FORMAT))
    if os.path.isfile(jpg_path):
        pdf_path = ".".join([jpg_path.split('.')[0],"pdf"])
        if os.path.isfile(pdf_path):
            sys.stderr.write("Moving tmp pdf file at {0}\n".format(pdf_path))
            shutil.move(pdf_path,"/Users/pfh/skald/src/orpheus_v3.4/output/{0}/orpheus_{0}.pdf".format(SKALD_FORMAT))

if __name__ == "__main__": _main()
