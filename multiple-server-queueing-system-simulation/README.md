# multiple-server-queueing-system-simulation  

This repository contains all the programs coded for assignment on multiple-server queueing system simulation **(Offline-2)**.  



## navigation  

- `inputdir/` contains sample input file `inputs.txt`  
- `spec/` contains **Offline-2** specification `offline2-spec.pdf`  
- `src/` contains python script `simulator.py`  



## input file format  

There is a sample input file `inputs.txt` inside `inputdir/` folder. This input file follows the following format.  

```
10000      // simulation termination condition (in seconds)
12 4 12 6  // number of floors, elevators, elevator capacity, maximum batch size
15 5 3 3   // door holding time, inter floor travelling time, door opening time, closing time (in seconds)
3 3        // passenger embarking time, disembarking time (in seconds)
1.5        // mean inter arrival time (in minutes)
```

The input file that you will provide should be named `inputs.txt` and put inside `inputdir/` folder.  



## getting started  

In order to run this elevator system simulation, place `src/simulator.py` file inside a workspace folder. Create `inputdir/` folder inside the same workspace folder and place `inputs.txt` file inside `inputdir/`. You may need to install some Python modules (namely, `numpy`) beforehand. Run `simulator.py` inside the workspace folder for running the simulation.  



## output files description  

The following output files will be generated and placed inside `outputdir/` after running `simulator.py`.  

- `customer_statistics.csv` contains various statistics on customers from specified number of runs of this elevator system simulation  
- `elevatorN_statistics.csv` contains various statistics on N-th elevator from specified number of runs of this elevator system simulation  



## sample outputs  

#### `customer_statistics.csv`  

| Simulation Run | Number of Customers Serviced | Avg Queue Length | Max Queue Length | Avg Delay Time | Max Delay Time | Avg Elevator Time | Max Elevator Time | Avg Delivery Time | Max Delivery Time |
| -------------- | ---------------------------- | ---------------- | ---------------- | -------------- | -------------- | ----------------- | ----------------- | ----------------- | ----------------- |
| 1              | 389                          | 0.09             | 5                | 111.99         | 184.78         | 50.23             | 127.0             | 75.11             | 251.78            |
| 2              | 338                          | 0.0              | 0                | 0              | 0              | 52.01             | 133.0             | 74.31             | 173.71            |
| 3              | 387                          | 0.09             | 3                | 150.19         | 336.79         | 51.62             | 133.0             | 76.52             | 458.79            |



#### `elevatorN_statistics.csv`  

| Simulation Run | Avg Load Size | Percentage Operation Time | Percentage Available Time | Number of Maximum Loads | Number of Total Stops |
| -------------- | ------------- | ------------------------- | ------------------------- | ----------------------- | --------------------- |
| 1              | 4.15          | 39.24                     | 60.76                     | 1                       | 112                   |
| 2              | 4.59          | 37.78                     | 62.22                     | 0                       | 106                   |
| 3              | 4.48          | 41.1                      | 58.9                      | 1                       | 121                   |

