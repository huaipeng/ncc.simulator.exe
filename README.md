# **ncc.simulator**
Neuromorphic chip simulator is developed by C++, the simulator instance named as 'ncc.simulator' can run on the Ubuntu 18.04.4 LTS, with OpenMP version, CUDA 

## 1. **Install Dependency Libraries Before to Run the Simulator**

The simulator only needs one dependency libraries: Protobuf. The simulator use Protobuf version is 3.4.0. You can
download source code from:

      https://github.com/google/protobuf/releases/download/v3.4.0/protobuf-cpp-3.4.0.zip

After downloading the source code, user can install Protobuf library from source code following below steps:

  1.1   ***Install dependency libraries for the protobuf***. On Ubuntu, you can install them with:

     $ sudo apt-get install autoconf automake libtool curl make g++ unzip

1.2  ***Install the protobuf***. Unzip the package and navigate into the unzipped folder of protobuf-3.4.0 to generate the configuration script first :

     $ ./autogen.sh

Then to build and install the Protocol Buffer runtime and the Protocol Buffer compiler (protoc) as the following commands:

     $ ./configure
     $ make
     $ make check
     $ sudo make install
     $ sudo ldconfig # refresh shared library cache.


If "make check" fails, you can still install, but it is likely that some features of this library will not work correctly on your system.

## 2. **Install Boost Library**

The simulator use boost library version is 1.65.1, the following command can help to install this library directly

    $ sudo apt-get install libboost-all-dev

After installation, you can check your boost library in your machine using following command :

    $ dpkg -s libboost-dev | grep 'Version'

  
  ## 2. **the Software Architecture of the Simulator**

The following picture show the simulator's architecture, which can get us general understanding about simulator's behaviours. the upper side include one list of cores which would perform core processing and the below side include two types of different communication networks: ideal network and 2D-mesh network, the ideal network will directly move spikes from injection buffer to ejection buffer, the 2D-mesh network will transfer spikes by the router matrix. The middle part is the network interface which include two important memory buffer : injection buffer and ejection buffer, the injection buffer store all the spikes outputed from all the neurons and the ejection buffer store all the spikes as the inputs for all the axons on the chip.

<img width="561" alt="image" src="https://user-images.githubusercontent.com/42291598/102766951-da92da00-43b9-11eb-8028-052296a4a461.png">

## 3. **Simulator’s features:**

  3.1   ***Two types of different crossbar: digital crossbar and RRAM crossbar.*** The digital crossbar uses one single value to store trained weight but RRAM crossbar uses one pair of resistances to hold trained weight.

  3.2   ***Two types of different communication network : ideal network and router-based 2D-mesh network.***  User can choose ideal network for fast accelerated speed or choose 2d-mesh network to analyse the traffic flow in the communication.

  3.3   ***Read- noise and write-noise simulation on RRAM crossbar***. The simulator can perform two types of noise behaviour : read-noise will occur at each tick however write-noise only occur when fusing values onto the RRAM crossbar. 

  3.4   ***Defect simulation on RRAM crossbar***. The simulator can perform defect simulation on the RRAM crossbar. User can specify the percentage of defect on the RRAM crossbar to explore the relationship between the chip performance and the percentage of defects

  3.5   ***Power estimation in the core processing and router processing***. The simulator can simulate each operation inside real chip and also can record final accumulated energy for all these operations.

3.6   ***Parallel computation can achieve fast accelerated speed***. The simulator can speed up on high performance machine with multi-core processor in order to decrease the simulation time. It also can run on GPUs with CUDA programming.

  3.7   ***Two types of computing mode: ANN and SNN***. SNN is spike neural network and ANN is artificial neural network using original values as the chip input.

## 4. **What is Needed for the Simulator:**
   4.1  ***The simulation configuration file.*** This file include all global settings for the simulator.
   
   4.2  ***The chip configuration file.*** This file define the chip layout including core number and core size.
   
   4.3  ***The bitstream configuration file.*** This file include weight matrics for each core and connections between cores and neuron settings.
   
   4.4  ***The input folder including spike source files.*** This folder specify the input folder for the simulation including all spike sources in CSV format
   
   4.5  ***The execution file : ncc.simulator.*** This is binary execution file which is compiled on Ubuntu 18.04.4 LTS.

## 5. **The input file format for the simulator in the SNN mode:**

The input file is in the CSV format holding spike trains for each axon. three columns are included: time step, core id, axon id. In the below picture, the left side display one example segment from one spike source file; the right side display the sorted records by last column 'axon id' from the same spike source file, which demonstrate all the spikes at different steps for one particular axon.

<img width="659" src="https://user-images.githubusercontent.com/42291598/102757109-c34cf000-43ab-11eb-972f-753b4dba99dd.png">

## 6. **The Output file format from the simulator in the SNN mode:**

When user specify the output cores in the simulation configuration file, the simulator will produce spike output for each spike source and store into one corresponding file with the extension name '.sink'. The '.sink' file is also in CSV format and include five columns : time step, source code id, source neuron id, destination code id, destination axon id.  The following picture display one example segment from one '.sink' file

<img width="539" alt="Screenshot 2022-12-21 at 5 05 42 PM" src="https://user-images.githubusercontent.com/42291598/102759234-cd242280-43ae-11eb-968a-7cbad683263f.png">

The user can compute following information from the 'sink' file:

- Compute the statistics about spike output from one particular core using column ’src core id’.

- Compute average spike ratio per tick between different cores using the column ‘src core id’ and ‘dest core id’

- Compute predication for final class  using the column ‘src neuron id’ or ‘dest axon id’


## 7. **The input file format for the simulator in the ANN mode:**

The ANN mode can help user to locate the issues in the mapping because the real values are the inputs of the chip simulation. The user can compare the values between the simulator output and Tensorflow outputs. The following picture display one example segment from one input file for ANN mode simulation. The four columns are included: time step, source core id, source axon id, spiked value (floating-point value which is equal to one pixel value in the input image).

<img width="364" alt="Screenshot 2022-12-21 at 5 23 18 PM" src="https://user-images.githubusercontent.com/42291598/102760975-4290f280-43b1-11eb-83d5-da1e55fb6b2b.png">

The input file only include one time-step because in the ANN mode, the inputs are fed into the chip at one time. the last column in the input file include original floating-point values.

## 8. **The output file format from the simulator in the ANN mode:**

The output files include six columns when user specify the ANN mode : time step, source code id, source axon id, destination core id, destination axon id, spiked value. The following picture display one example segment from one 'sink' file:

<img width="539" alt="Screenshot 2022-12-21 at 5 05 42 PM" src="https://user-images.githubusercontent.com/42291598/102762249-fe9eed00-43b2-11eb-826c-3aa5a691e33f.png">

From the above 'sink' file in the ANN mode, user can perform the following computing:

- Compare simulator’s output and Tensorflow output using the column ‘spiked value’ and ‘src core id’ and ‘src neuron id’
- Compute predication for final class using the column ‘src neuron id’ or ‘dest axon id’ and ’spiked value’

## 9. **One case study for 21-core simulation for MNIST classification:**

The following picture demonstrate the entire pipeline when user want to simulate neuromorphic chip how to work. The three steps are needed: 

- Build the neural network model,
- Map the model onto the chip, 
- Perform the simulation on the simulator.

<img width="792" alt="Screenshot 2022-12-21 at 5 40 59 PM" src="https://user-images.githubusercontent.com/42291598/102763241-5d189b00-43b4-11eb-9049-af4944ea54d0.png">

## 10. Run the Simulator and Explore its Features

Clone the example folder from repository:

       $ git clone https://github.com/huaipeng/ncc.simulator.exe.git
       
All the necessary configuration files and input files are ready in the folder '25-cores', after user clone the example folder and navigate into the folder '25-cores', he can type the following command to run the simualtor:
~~~~
./ncc.simulator simulation_config_digital.json
~~~~

The executable file is *'ncc.simulator'* and the configuration file *'simulation_config_digital.json'* including different settings for the simulator. After you run the simulator, you can find the output file with the extension named like '*.sink' in the same folder as the spike sources.

The following picture display the progress to run the simulator: type the simulator name with one simulation configuration file as input argument. The simulator will load spike source one by one from input folder and produce corresponding 'sink' file and print out the 'sink' filename on the console.

<img width="935" alt="Screenshot 2023-06-02 at 1 56 43 PM" src="https://user-images.githubusercontent.com/42291598/120434561-3624b300-c3af-11eb-8470-8285b1024a9f.png">

The following picture display the processing of output files in order to predict final class for each output and also compute final accuracy for entire dataset.

<img width="732" alt="Screenshot 2023-06-02 at 2 30 35 PM" src="https://user-images.githubusercontent.com/42291598/120434570-391fa380-c3af-11eb-833c-fa98c5656b26.png">

