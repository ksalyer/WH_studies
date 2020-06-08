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


#wh_samples = {'TTWJetsToLNu_a18v1':wh_samples['TTWJetsToLNu_a18v1'], 'W4Jets_NuPt200_a18v1':wh_samples['W4Jets_NuPt200_a18v1']}
#wh_samples = {'TTWJetsToLNu_f17v2':wh_samples['TTWJetsToLNu_f17v2']}
#wh_samples = {'W4Jets_NuPt200_f17v2':wh_samples['W4Jets_NuPt200_f17v2']}
#wh_samples = {'W2Jets_NuPt200_a18v1':wh_samples['W2Jets_NuPt200_a18v1'], 'W1Jets_NuPt200_a18v1':wh_samples['W1Jets_NuPt200_a18v1']}
#wh_samples = {'data_2018B_singlemu':wh_samples['data_2018B_singlemu']}

#wh_samples = {x:wh_samples[x] for x in wh_samples.keys() if 'data_2017' in x}
#wh_samples = {x:wh_samples[x] for x in wh_samples.keys() if ('f17v2' in x or 'data_2017' in x)}
#wh_samples = {x:wh_samples[x] for x in wh_samples.keys() if not ('data' in x)}
#wh_samples = {'data_2017B_met': wh_samples['data_2017B_met']}
wh_samples = {'data_2018D_singlemu': wh_samples['data_2018D_singlemu']}

#wh_samples = {x:wh_samples[x] for x in wh_samples.keys() if ('WplusH_HToBB_WToLNu' in x or 'WminusH_HToBB_WToLNu' in x)}
#wh_samples = {x:wh_samples[x] for x in wh_samples.keys() if 'JetsToLNu_a18v1' in x}

dryRun = True

incomplete_samples = []
missing_samples = []

MCversion6 = 'NanoAODv6'
MCversion7 = 'NanoAODv7'
DataVersion6 = '25Oct2019'
DataVersion7 = '02Apr2020'

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
            nanoAOD6 = getChild(miniAOD, MCversion6)
            nanoAOD7 = getChild(miniAOD, MCversion7)
            isData = False
        else:
            nanoAOD6 = getChild(miniAOD, DataVersion6)
            nanoAOD7 = getChild(miniAOD, DataVersion7)
            isData = True
    if not (nanoAOD6 or nanoAOD7):
        #missingNano.append(miniAOD)
        print "No nanoAOD sample found, exiting..."
        missing_samples.append(s)
        continue
        #raise NotImplementedError
    print nanoAOD6
    print nanoAOD7

    if nanoAOD6:
        sample6 = DBSSample(dataset=nanoAOD6)
    if nanoAOD7:
        sample7 = DBSSample(dataset=nanoAOD7)
    sample_mAOD = DBSSample(dataset=miniAOD)

    nAOD_events6 = 0
    nAOD_events7 = 0

    skip = False
    try:
        mAOD_events = sample_mAOD.get_nevents()
        if nanoAOD6:
            nAOD_events6 = sample6.get_nevents()
        if nanoAOD7:
            nAOD_events7 = sample7.get_nevents()
    except TypeError:
        print "Sample instance failed. Skipping sample for now."
        skip = True

    if skip: continue

    nAOD_events = nAOD_events7 if nAOD_events6 < nAOD_events7 else nAOD_events6
    sample = sample7 if nAOD_events6 < nAOD_events7 else sample6
    nanoAOD = nanoAOD7 if nAOD_events6 < nAOD_events7 else nanoAOD6
    print "Using nanoAODv7" if nAOD_events6 < nAOD_events7 else "Using nanoAODv6"

    if not nAOD_events == mAOD_events:
        print "### WARNING ###"
        print "    |---> Number of events in NanoAOD: %s"%nAOD_events
        print "    |---> Number of events in MiniAOD: %s"%mAOD_events
        print "             |---> %s percent of events missing in NanoAOD"%(float(mAOD_events-nAOD_events)/mAOD_events*100)
        incomplete_samples.append(nanoAOD)


    #raise NotImplementedError

    year = getYearFromDAS(nanoAOD)

    print "Found year:",year

    tag = 'WHv1p1'
    #raise NotImplementedError
    isData = 1 if isData else 0

    if not dryRun:
        maker_task = CondorTask(
            sample = sample,
                #'/hadoop/cms/store/user/dspitzba/nanoAOD/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8__RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20_ext1-v1/',
            # open_dataset = True, flush = True,
            executable = "executable.sh",
            arguments = "WHv1p2 %s %s"%(year, isData),
            #tarfile = "merge_scripts.tar.gz",
            files_per_output = 1,
            #output_dir = os.path.join(outDir, sample.get_datasetname()),
            outdir_name = "stopNano_" + s,
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



    if not dryRun:
        merge_task = CondorTask(
            sample = DirectorySample(
                dataset="merge_"+sample.get_datasetname(),
                location=maker_task.get_outputdir(),
            ),
            # open_dataset = True, flush = True,
            executable = "merge_executable.sh",
            arguments = "WHv1p2 %s %s"%(year, isData),
            #tarfile = "merge_scripts.tar.gz",
            files_per_output = 10,
            output_dir = maker_task.get_outputdir() + "/merged",
            output_name = s+".root",
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
            min_completion_fraction = 1.00,
        )
    
        merge_tasks.append(merge_task)
    
if not dryRun:
    for i in range(100):
        total_summary = {}
        
        if not os.path.isdir(maker_task.get_outputdir()):
            os.makedirs(maker_task.get_outputdir())
        if not os.path.isdir(maker_task.get_outputdir()+'/merged'):
            os.makedirs(maker_task.get_outputdir()+'/merged')
            os.makedirs(maker_task.get_outputdir()+'/skimmed')
        #do_cmd("mkdir -p {}".format(maker_task.get_outputdir()))
        #do_cmd("mkdir -p {}/merged".format(maker_task.get_outputdir()))
        #do_cmd("mkdir -p {}/skimmed".format(maker_task.get_outputdir()))
        
        for maker_task, merge_task in zip(maker_tasks,merge_tasks):
        #for maker_task in maker_tasks:
            maker_task.process()
    
            frac = maker_task.complete(return_fraction=True)
            if frac >= maker_task.min_completion_fraction:
            # if maker_task.complete():
            #    do_cmd("mkdir -p {}/merged".format(maker_task.get_outputdir()))
            #    do_cmd("mkdir -p {}/skimmed".format(maker_task.get_outputdir()))
                merge_task.reset_io_mapping()
                merge_task.update_mapping()
                merge_task.process()
    
            total_summary[maker_task.get_sample().get_datasetname()] = maker_task.get_task_summary()
            total_summary[merge_task.get_sample().get_datasetname()] = merge_task.get_task_summary()
 
        print (frac)
   
        # parse the total summary and write out the dashboard
        StatsParser(data=total_summary, webdir="~/public_html/dump/metis_WH_1l_nano/").do()
    
        # 15 min power nap
        time.sleep(15.*60)



