# single-server-queueing-system-simulation  

This repository contains all the programs coded for assignment on single-server queueing system simulation **(Offline-1)**.  



## navigation  

- `inputdir/` contains sample input file `inputs.txt`  
- `report/` contains report on different simulations and statistics  
- `spec/` contains **Offline-1** specification `offline1-spec.pdf`  

- `src/` contains python script `simulator.py`  



## input file format  

There is a sample input file `inputs.txt` inside `inputdir/` folder. This input file follows the following format.  

```
1.0   	// mean inter-arrival time
0.5   	// mean service time
1000  	// number of customers
```

The input file you provide should be named `inputs.txt` and put inside `inputdir/` folder.  



## getting started  

In order to run the simulation, place `src/simulator.py` file inside a workspace folder. Create `inputdir/` folder inside the same workspace folder and place `inputs.txt` file inside `inputdir/`. You may need to install some Python modules (namely, `numpy`, `matplotlib`) beforehand. Run `simulator.py` inside the workspace folder for running the simulation.  



## output files description  

The following output files will be generated and placed inside `outputdir/` after running `simulator.py`.  

- `outputs.txt` contains statistics from single run of the simulation  
- `stats.csv` contains statistics for simulation with different values of mean service time  
- `stats.txt` contains statistics for generated uniform and exponential random variates  

