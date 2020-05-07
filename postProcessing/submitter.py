import os
import time

from metis.Sample import DirectorySample, DBSSample
from metis.CondorTask import CondorTask
from metis.StatsParser import StatsParser
from metis.Utils import do_cmd

from whSamples import wh_samples

def _dasPopen(dbs):
    return os.popen(dbs)

def getChild(DASname, versionFilter='NanoAODv7'):
    sampleName = DASname.rstrip('/')
    query, qwhat = sampleName, "dataset"

    dbs='dasgoclient -query="child %s=%s"'%(qwhat,query)
    dbsOut = _dasPopen(dbs).readlines()

    nanoDAS = False
    for line in dbsOut:
        if line.count(versionFilter):
            nanoDAS = line.replace('\n','')

    return nanoDAS

def getYearFromDAS(DASname):
    if DASname.count('Autumn18') or DASname.count('Run2018'):
        return 2018
    elif DASname.count('Fall17') or DASname.count('Run2017'):
        return 2017
    elif DASname.count('Summer16') or DASname.count('Run2016'):
        return 2016
    else:
        return -1

maker_tasks = []
merge_tasks = []


#wh_samples = {'TTWJetsToLNu_a18v1':wh_samples['TTWJetsToLNu_a18v1']}
wh_samples = {'TTWJetsToLNu_f17v2':wh_samples['TTWJetsToLNu_f17v2']}
#wh_samples = {'data_2018B_singlemu':wh_samples['data_2018B_singlemu']}


incomplete_samples = []
missing_samples = []

MCversion = 'NanoAODv6'
#MCversion = 'NanoAODv7'
DataVersion = '25Oct2019'
#DataVersion = '02Apr2020'

#if True:
for s in wh_samples.keys():

    print
    print s
    miniAOD = wh_samples[s]
    if "NANOAOD" in miniAOD:
        nanoAOD = miniAOD
        print "Already have nanoAOD"
    else:
        print miniAOD
        if 'SIM' in miniAOD:
            nanoAOD = getChild(miniAOD, MCversion)
            isData = False
        else:
            nanoAOD = getChild(miniAOD, DataVersion)
            isData = True
    if not nanoAOD:
        #missingNano.append(miniAOD)
        print "No nanoAOD sample found, exiting..."
        missing_samples.append(s)
        continue
        #raise NotImplementedError
    print nanoAOD

    sample = DBSSample(dataset=nanoAOD)
    sample_mAOD = DBSSample(dataset=miniAOD)

    if not sample.get_nevents() == sample_mAOD.get_nevents():
        print "### WARNING ###"
        print "    |---> Number of events in NanoAOD: %s"%sample.get_nevents()
        print "    |---> Number of events in MiniAOD: %s"%sample_mAOD.get_nevents()
        
        incomplete_samples.append(nanoAOD)


    #raise NotImplementedError

    tag = 'WHv0'
    
    if False:
        maker_task = CondorTask(
            sample = sample,
                #'/hadoop/cms/store/user/dspitzba/nanoAOD/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8__RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20_ext1-v1/',
            # open_dataset = True, flush = True,
            executable = "executable.sh",
            arguments = "WHv0 2018",
            #tarfile = "merge_scripts.tar.gz",
            files_per_output = 1,
            #output_dir = os.path.join(outDir, sample.get_datasetname()),
            outdir_name = "stopNano_" + babyname,
            output_name = "stopNano.root",
            output_is_tree = True,
            # check_expectedevents = True,
            tag = tag,
            condor_submit_params = {"sites":"T2_US_UCSD,UAF"},
            cmssw_version = "CMSSW_10_2_9",
            scram_arch = "slc6_amd64_gcc700",
            # recopy_inputs = True,
            # no_load_from_backup = True,
            min_completion_fraction = 0.99,
        )
        
        maker_tasks.append(maker_task)



    if False:
        merge_task = CondorTask(
            sample = DirectorySample(
                dataset="merge_"+sample.get_datasetname(),
                location=maker_task.get_outputdir(),
            ),
            # open_dataset = True, flush = True,
            executable = "merge_executable.sh",
            arguments = "WHv0 2018",
            #tarfile = "merge_scripts.tar.gz",
            files_per_output = 3,
            output_dir = maker_task.get_outputdir() + "/merged",
            output_name = babyname+".root",
            output_is_tree = True,
            # check_expectedevents = True,
            tag = tag,
            # condor_submit_params = {"sites":"T2_US_UCSD"},
            # cmssw_version = "CMSSW_9_2_8",
            # scram_arch = "slc6_amd64_gcc530",
            condor_submit_params = {"sites":"T2_US_UCSD,UAF"},
            cmssw_version = "CMSSW_10_2_9",
            scram_arch = "slc6_amd64_gcc700",
            # recopy_inputs = True,
            # no_load_from_backup = True,
            min_completion_fraction = 0.99,
        )
    
        merge_tasks.append(merge_task)
    
if False:
    for i in range(100):
        total_summary = {}
    
        for maker_task, merge_task in zip(maker_tasks,merge_tasks):
        #for maker_task in maker_tasks:
            maker_task.process()
    
            frac = maker_task.complete(return_fraction=True)
            if frac >= maker_task.min_completion_fraction:
            # if maker_task.complete():
                do_cmd("mkdir -p {}/merged".format(maker_task.get_outputdir()))
                do_cmd("mkdir -p {}/skimmed".format(maker_task.get_outputdir()))
                merge_task.reset_io_mapping()
                merge_task.update_mapping()
                merge_task.process()
    
            total_summary[maker_task.get_sample().get_datasetname()] = maker_task.get_task_summary()
            total_summary[merge_task.get_sample().get_datasetname()] = merge_task.get_task_summary()
 
        print (frac)
   
        # parse the total summary and write out the dashboard
        StatsParser(data=total_summary, webdir="~/public_html/dump/metis_tW_scattering/").do()
    
        # 15 min power nap
        time.sleep(15.*60)



