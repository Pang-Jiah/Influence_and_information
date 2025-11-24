import h5py
import numpy as np
import os

import time
import sys 
import infomeasure as im

if __name__ == "__main__":
    # enter the absolute path of this python filep
    path_of_this_file = os.path.split(__file__)[0]
    os.chdir(path_of_this_file)


    os.chdir("..")
    os.chdir("..")
    sys.path.append(".") 
    from h5py_process import H5PY_Processor

    
    # find the folder path from command line argument
    folder = sys.argv[1] # receieve the path
    print(folder,"start")
    os.chdir(folder)



    f = H5PY_Processor("Data-Vicsek_pairwise.hdf5","r")

    velocity            = f.f["velocity"][:,:,:] # The last dimension is "time"
    theta               = f.f["orientation"][:,:]
    interaction_matrix  = f.f["interaction_matrix"][:,:]
    position            = f.f["position"][:,:]
    influence           = f.f["influence"][:,:,:] 

    groupParameter = f.f["parameters"]
    time_resolution         = groupParameter["time_resolution"][:][0]
    number_of_steps         = groupParameter["number_of_steps"][:][0]
    wLF                     = groupParameter["wLF"][:][:]
    number_of_influencers   = groupParameter["number_of_influencers"][:][0]
    eta                     = groupParameter["noise_strength"][:][0]
    number_of_particles     = groupParameter["number_of_particles"][:][0]
    size_of_arena           = groupParameter["size_of_arena"][:][0]
    sense_radius            = groupParameter["sensing_radius"][:][0]
    speed                   = groupParameter["speed"][:][0]
    f.close()
    

    followerList = np.arange(number_of_influencers,number_of_particles)

    count = 0
    
    informationList = {
        # conditional entropy
        # "cE_box":16,
        # "cE_Guassian":16,

        #Kernel estimation method
        "MI_kernel":16,
        "TDMI_kernel":16,
        "TE_kernel":16,
            # normalized by mutual information
        "nTDMI_kernel":16,
        "nTE_kernel":16,

        # Kozachenko-Leonenko (KL)/ Metric/ kNN Entropy Estimation/ KSG method
        "MI_KL":16,
        "TDMI_KL":16,
        "TE_KL":16,
            # normalized by mutual information
        "nTDMI_KL":16,
        "nTE_KL":16,



        # # Ordinal mutual information between two time series
        # "MI_ordinal":16,
        # "TDMI_ordinal": 16,
        # "TE_ordinal":16,
        #     # normalized by mutual information
        # "nTDMI_ordinal": 16,
        # "nTE_ordinal":16,
        }       
    
    time_startall = time.time()  # record start time
    
    start_point = 1000 # start from the 1000th steps. This is to make sure everything reach stationary state
    
    dt = 1
    # obatin the distribution
    ## obtain time series
    xt = theta[0,start_point:-dt] 
    yt = theta[1,start_point:-dt]
    yt_tau = theta[1,start_point+dt:]
    
    '''kernel estimation method to estimate the probability density function'''
    # parameters for kernel method
    base = 2
    bandwidth_kernel = 0.05*(2*np.pi)  # bandwidth
    '''conditional entropy of yt_tau given by yt'''
    # informationList["cE_box"]=im.entropy(yt,yt_tau, approach="kernel", kernel="box", bandwidth=bandwidth_kernel, base=base)- im.entropy(yt, approach="kernel", kernel="box", bandwidth=bandwidth_kernel, base=base)
    
    # random_indices = np.random.choice(len(xt), size=int(2**15), replace=False)
    # xt = xt[random_indices]
    # yt = yt[random_indices]
    # yt_tau = yt_tau[random_indices]
    
    
    # informationList["cE_Guassian"]=im.entropy(yt,yt_tau, approach="kernel", kernel="gaussian", bandwidth=bandwidth_kernel, base=base)-im.entropy(yt, approach="kernel", kernel="gaussian", bandwidth=bandwidth_kernel, base=base)
    
    
    # TDMI
    tdmi_kernel = im.mutual_information(xt, yt_tau, approach="kernel", kernel="box", bandwidth=bandwidth_kernel, base=base)
    informationList["TDMI_kernel"] = tdmi_kernel
    # TE
    # te_kernel = im.transfer_entropy(xt, yt, approach="kernel", kernel="gaussian", bandwidth=bandwidth_kernel, step_size = 1, prop_time=0, src_hist_len = 1, dest_hist_len = 1, base=base)
    te_kernel = im.mutual_information(xt, yt_tau, cond = yt, approach="kernel", kernel="box", bandwidth=bandwidth_kernel, base=base)
    informationList["TE_kernel"] = te_kernel
    # total mutual information
    tmi_kernel = te_kernel + im.mutual_information(yt, yt_tau, approach="kernel", kernel="box", bandwidth=bandwidth_kernel, base=base)
    informationList["MI_kernel"] = tmi_kernel
    # normalized by mutual information
    informationList["nTDMI_kernel"] = tdmi_kernel / tmi_kernel if tmi_kernel != 0 else 0
    informationList["nTE_kernel"] = te_kernel / tmi_kernel if tmi_kernel != 0 else 0


    # '''Kozachenko-Leonenko (KL)/ Metric/ kNN Entropy Estimation/ KSG method'''
    # # parameters for KL method
    k = 4  # number of nearest neighbors
    base = 2
    # TDMI
    tdmin_KL = im.mutual_information(xt, yt_tau, approach="metric", k=k, base=base)
    informationList["TDMI_KL"] = tdmin_KL
    # TE
    # te_KL = im.transfer_entropy(xt, yt, approach="metric", k=k, step_size = 1, prop_time=0, src_hist_len = 1, dest_hist_len = 1, base=base)
    te_KL = im.mutual_information(xt, yt_tau, cond=yt, approach="metric", k=k,  base=base)
    informationList["TE_KL"] = te_KL
    # total mutual information
    tmi_KL = te_KL + im.mutual_information(yt, yt_tau, approach="metric", k=k, base=base)
    informationList["MI_KL"] = tmi_KL
    # normalized by mutual information
    informationList["nTDMI_KL"] = tdmin_KL / tmi_KL if tmi_KL != 0 else 0
    informationList["nTE_KL"] = te_KL / tmi_KL if tmi_KL != 0 else 0



    ''' Ordinal mutual information between two time series'''
    # # parameters for ordinal method
    # embedding_dim = 3
    # base = 2
    # # TDMI
    # tdmi_ordinal = im.mutual_information(xt, yt_tau, approach="ordinal", embedding_dim=embedding_dim,base=base)
    # informationList["TDMI_ordinal"] = tdmi_ordinal
    # # Transfer entropy
    # # te_ordinal = im.transfer_entropy(xt, yt, approach="ordinal", embedding_dim=embedding_dim,step_size = 1,prop_time=0, src_hist_len = 1, dest_hist_len = 1, base=base)
    # te_ordinal = im.transfer_entropy(xt, yt_tau ,cond=yt, approach="ordinal", embedding_dim=embedding_dim, base=base)
    # informationList["TE_ordinal"] = te_ordinal
    # # total mutual information
    # tmi_ordinal = te_ordinal + im.mutual_information(yt, yt_tau, approach="ordinal", embedding_dim=embedding_dim,base=base)
    # informationList["MI_ordinal"] = tmi_ordinal
    # # normalized by mutual information
    # informationList["nTDMI_ordinal"] = tdmi_ordinal / tmi_ordinal if tmi_ordinal != 0 else 0
    # informationList["nTE_ordinal"] = te_ordinal / tmi_ordinal if tmi_ordinal != 0 else 0


 
    time_endall = time.time()  # record end time
    
    time_sumall = time_endall - time_startall  # total time consumption
    print("the time consumption for running one group:",time_sumall)
    


    # save data
    file = h5py.File("Data_estimator"+".hdf5", 'w')
    

    number_of_particles = np.array([number_of_particles])
    number_of_influencers = np.array([number_of_influencers])  
    wLF = np.array([wLF])
    eta = np.array([eta])

    file.create_dataset("number_of_particles",    data=number_of_particles,     compression='gzip',   compression_opts=9)
    file.create_dataset("number_of_influencers",  data=number_of_influencers,   compression='gzip',   compression_opts=9)
    file.create_dataset("wLF",                    data=wLF,                     compression='gzip',   compression_opts=9)
    file.create_dataset("eta",                    data=eta,                     compression='gzip',   compression_opts=9)
    
    for keys in informationList:
        file.create_dataset(keys, data=np.array([informationList[keys]]), compression='gzip', compression_opts=9)
    
    
    file.close()
    print(folder,"done")
