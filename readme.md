# PID Tuner
Author：Felix  
Date：2022.11.24  
QQ：0x3338233D  
If you like it, please give me a star, thank you~  

## Terrible Adjusting
Everytime adjusting PID, I am nearly crazy!!!  
I have to observe the Intelligent Car running in, running out.  
I have to observe so many figures.  
I have to change Kp, Ki, Kd manually.  
I have to chagne Kp, Ki, Kd slightly(0.001) and repeatly.  
Damn, I do not have that patience.  

Okay, now, all of that can be done by computer.  
You just need to tell it, how much fast, how much steady.  
It is easier, faster and better.  

## Project File Structure
1. aircraft.py：a non-linear test model
2. pid.py：the pid implemented by Python
3. pidtuner.py：pid tuner code, main source
4. test_bench.py：step function, track test
5. test_bench_nonlinear.py：continuous function, track test

## Core Concept
First, we should know:  
1. Kp,Ki,Kd have different and irrelevant effects. We adjust PID parameters, in fact, we are to find a best ratio among P Effect, I Effect and D Effect.
2. PID has not a globally best parameter. Fast, Accurate, Steady, these three optimization objectives are not both-had. So we always find a balance among Fast, Accurate and Steady.
3. The optimization always getting better, Kp,Ki,Kd increase from 0 to a limited up-boundary.

So, if we could find a variable which rules PID effect, we can make PID itself adjust Kp,Ki,Kd until it gets the effect we expect.

Through PID figure of Target-Y，I chose to use Globally Average Error to meansure PID effect.

When adjust PID parameter, we always first adjust Kp, then Ki, last Kd.

## Parameter Explaination
Parameters we need to change depend on model are:
1. RangP: P Optimizer's Expected Effect Range. The smaller value, the stronger P effect.
2. IncP：P Increament Coefficient. You should determine this parameter before `RangP` depend on your model's input and output. IncP affects RangP.
3. DesP：P Decreasement Coefficient. Commonly, 0.1*IncP
4. ConP：P Constant Increament and Decreasement.
5. RangI：I Optimizer's Expected Effect Target.
6. ConI：I Constant Increament and Decreasement.
7. ConD：D Constant Increament and Decreasement. D optimizer has no a obvious target. So, we should observe Target-Y figure to find the best Kd.

## Evaluation Method
When use PID Tuner, we need to observe these values:
1. Target-Y Figure：which reflects the general PID effect. You can use this to determine RangP, RangI.
2. AveErr：which shows the Generally Average Error. 

## Optimization Method
To make PID Tuner faster and delicate, one thing I recommand:  
Normalize your PID Input and Output to [-1,+1].