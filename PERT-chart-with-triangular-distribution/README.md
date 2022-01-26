# PERT-chart-with-triangular-distribution  

This repository contains the excel spreadsheet prepared for assignment on PERT (**Program Evaluation Review Technique**) chart analysis with triangular probability distribution **(Offline-3)**. The following probability distributions have been used in this assignment.  

- triangular `TRIANG(a, b, m)` distribution  
- right-triangular `RT(a, b)` distribution  
- left-triangular `LT(a, b)` distribution  

Here, `a` is location parameter, `b-a` is scaling parameter, and `m` is shape parameter. These distributions have been used to calculate duration for each activity in PERT chart.  



## navigation  

- `spec/` contains tasks specification for this assignment `offline3-spec.pdf`.  
- `src/` contains prepared excel spreadsheet `analyser.xlsx`.  



## `analyser.xlsx` description  

| **Activity**     | **Immediate Predecessor**         | `a`              | `m`               | `b`               |
| ---------------- | --------------------------------- | ---------------- | ----------------- | ----------------- |
| name of activity | predecessors of activity (if any) | optimistic value | most likely value | pessimistic value |

| **Start Time**         | `U(0, 1)`              | **Duration**         | **Finish Time**         |
| ---------------------- | ---------------------- | -------------------- | ----------------------- |
| start time of activity | uniform random variate | duration of activity | finish time of activity |

| **Trial**   | **Project Duration**             | **Success**                                        |
| ----------- | -------------------------------- | -------------------------------------------------- |
| `i`th trial | project duration for `i`th trial | whether project could meet deadline in `i`th trial |

| **Average Project Duration**                    | **Success Rate**                    |
| ----------------------------------------------- | ----------------------------------- |
| average project duration considering all trials | success rate considering all trials |

