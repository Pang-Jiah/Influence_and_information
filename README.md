Investigate the relationship between influence (physical causal relationship) and information (information-theoretic quantities)



Python: 3.6

package:
- numpy
- [dit](https://github.com/dit/dit?tab=readme-ov-file) for information computation
- progressbar2
- openpyxl
- h5py
- matplotlib
- ffmpeg
- [infomeasure](https://github.com/cbueth/infomeasure) for different estimators (python 3.11 + )


Workflow:

Collect collective data: 
- Run "Vicsek_collective\parallel_master_Vicsek_collective.py" to run "Vicsek_collective\Vicsek_collective.py" to obtain the collective data. 
- To calculate those information-theoretic quantities, run "Vicsek_collective\parallel_master_inf_collective.py" to run "Vicsek_collective\information_quantities.py" to obtain these data.
- To obtain relevant order parameters, run "Vicsek_collective\order_parameters.py"
- Run "Vicsek_collective\collect_information.py" to store information-theoretic data into a xlsx file called "inf_collective_8.xlsx". _8 means the number of bins you select is 8.
- Run "Vicsek_collective\collect_order_parameters.py" to store order parameter  data into a xlsx file named "order_parameters.xlsx".

Collect pairwise data:
- Run "Vicsek_pairwise\parallel_master_Vicsek_pairwise.py" to run "Vicsek_pairwise\Vicsek_pairwise.py" to obtain the pairwise data. 
- To calculate those information-theoretic quantities and influence data, run "Vicsek_pairwise\parallel_master_inf_pairwise.py" to run "Vicsek_pairwise\inf_quantities.py" to obtain these data.
- Run "Vicsek_pairwise\collect_data.py" to store relevant information-theoretic quantities and influence quantities into a xlsx file named "inf_pairwise_8.xlsx". _8 means the number of bins you select is 8.
- To calculate information-theoretic quantities using different distribution estimators:
  - Run "Vicsek_pairwise\Entropy_estimator\parallel_master_information_pairwise.py" to run "Vicsek_pairwise\Entropy_estimator\information_quantities.py" to obtain these data.
  - Run "Vicsek_pairwise\Entropy_estimator\collect_data.py" to store relevant information-theoretic quantities into a xlsx file named "entropy_estimator.xlsx".



Generate Video:

Run Vicsek_video.py
