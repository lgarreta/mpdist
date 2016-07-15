A project to execute python multiprocessing over more than one node in a cluster.
The multiprocessing library of python can not be distributed over a cluster only executes in one node. My idea is to create a "daemon" that we call "worker" which is listening request from a "commander". The commander distributes one task over the active workers.
