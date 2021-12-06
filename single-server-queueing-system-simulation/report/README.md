## Offline-1: Single-server Queueing System Simulation  

This report is prepared and submitted by Ajmain Yasar Ahmed Sahil **(Student ID: 1605023)**.  



### Inputs  

```
1.0   // mean inter-arrival time
0.5   // mean service time
1000  // number of customer
```



### Task-1: Simulation with `mean_inter_arrival_time` and `mean_service_time`  

| Performance Measure     | Value           |
| ----------------------- | --------------- |
| Average delay in queue  | 0.620 minutes   |
| Average number in queue | 0.669           |
| Server utilization      | 0.515           |
| Time simulation ended   | 927.090 minutes |



### Task-2: Simulation with Different Values of `mean_service_time`  

| k    | Average delay in queue (minutes) | Average number in queue | Server utilization | Time simulation ended (minutes) |
| ---- | -------------------------------- | ----------------------- | ------------------ | ------------------------------- |
| 0.5  | 0.4689002209579499               | 0.4497999525745997      | 0.4887327864002765 | 1042.4639181796765              |
| 0.6  | 0.5458670747769993               | 0.5372616164768749      | 0.5672781242594485 | 1016.0172586989468              |
| 0.7  | 1.3855905443957375               | 1.3864009349136892      | 0.7153034662607128 | 999.4154717459134               |
| 0.8  | 2.521811434689961                | 2.4393909974227217      | 0.7809861918991363 | 1033.7873007460955              |
| 0.9  | 5.226005937976064                | 4.930493439495078       | 0.8321959213101716 | 1059.9356843503365              |



### Task-3: Statistics on Generated Uniform and Exponential Random Variates  

#### Uniform random variates (2000 generated)  

| Performance Measure | Value                 |
| ------------------- | --------------------- |
| Min                 | 0.0003854765335904453 |
| Max                 | 0.999477074978319     |
| Median              | 0.5143297178826047    |

![fig1](https://github.com/FromSaffronCity/simulation-and-modeling-sessional/blob/master/single-server-queueing-system-simulation/report/res/Figure_1.PNG?raw=true)

![fig2](https://github.com/FromSaffronCity/simulation-and-modeling-sessional/blob/master/single-server-queueing-system-simulation/report/res/Figure_2.PNG?raw=true)



#### Exponential random variates with mean_inter_arrival_time (1000 generated)  

| Performance Measure | Value                 |
| ------------------- | --------------------- |
| Min                 | 0.0005230617946536215 |
| Max                 | 6.271790637423871     |
| Median              | 0.6409373452822282    |

![fig3](https://github.com/FromSaffronCity/simulation-and-modeling-sessional/blob/master/single-server-queueing-system-simulation/report/res/Figure_3.PNG?raw=true)

![fig4](https://github.com/FromSaffronCity/simulation-and-modeling-sessional/blob/master/single-server-queueing-system-simulation/report/res/Figure_4.PNG?raw=true)



#### Exponential random variates with mean_service_time (1000 generated)  

| Performance Measure | Value                 |
| ------------------- | --------------------- |
| Min                 | 0.0015899557240103709 |
| Max                 | 3.9305151197357175    |
| Median              | 0.3452815575074324    |

![fig5](https://github.com/FromSaffronCity/simulation-and-modeling-sessional/blob/master/single-server-queueing-system-simulation/report/res/Figure_5.PNG?raw=true)

![fig6](https://github.com/FromSaffronCity/simulation-and-modeling-sessional/blob/master/single-server-queueing-system-simulation/report/res/Figure_6.PNG?raw=true)

