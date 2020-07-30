Installation 

1. Create 3 VMs , and connect them to the same network , in this case NAT network.
2. Label each of them as "Intermediate" , "Edge"  and "Backend" 
3. Install Docker and Docker compose in all of them .
4. Clone this repository branch ("intermediate-pack")into the "Intermediate" VM .
5. `cd SCCAM`
6. `./intermediate.sh`