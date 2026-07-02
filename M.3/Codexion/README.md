*This project has been created as part of the 42 curriculum by oshtohri.*

# Codexion

## Description
Codexion is a concurrent multi-threaded simulation written in C, modeling a resource-constrained co-working hub where multiple coders (represented by POSIX threads) compete for a limited number of shared hardware USB dongles to compile their quantum code. 

The core challenge of this project lies in orchestrating these threads to guarantee liveness, avoid deadlocks, and schedule execution fairly using FIFO (First In, First Out) and EDF (Earliest Deadline First) algorithms. Coders must compile within a specific burnout window, requiring a highly synchronized monitoring and arbitration mechanism.

The simulation models three main actions for each coder:
1. **Compiling**: Requires taking the left and right USB dongles simultaneously.
2. **Debugging**: Conducted after a successful compilation. Both dongles are released prior to this.
3. **Refactoring**: Follows debugging. Once completed, the coder immediately tries to enqueue for compilation again.

To coordinate access to the dongles, we implement a scheduling queue with FIFO and EDF policies, complete with precise real-time burnout detection.

## Files and structure

```
.
├── Makefile
├── README.md
├── include
│   └── codexion.h
└── src
    ├── main.c
    ├── parser
    │   ├── parse_args.c
    │   ├── parse_utils.c
    │   └── print_parse_error.c
    ├── init
    │   ├── init_simulation.c
    │   ├── init_modules.c
    │   └── destroy_simulation.c
    ├── queue
    │   ├── heap_ops.c
    │   └── heapify.c
    ├── scheduler
    │   └── scheduler_routine.c
    ├── coder
    │   ├── coder_routine.c
    │   ├── coder_utils.c
    │   └── coder_actions.c
    ├── dongles
    │   ├── dongle_utils.c
    │   └── dongle_ops.c
    ├── monitor
    │   ├── monitor_routine.c
    │   └── monitor_checks.c
    ├── utils
    │   ├── get_timestamp.c
    │   └── log_action.c
    └── simulation
        └── simulation_utils.c
```


---

## System Architecture

The layout of the simulation mimics a modified circular ring topology. There are exactly as many physical dongles as there are coders, with one dongle positioned on the table between each pair of coders.

### Resource Allocation Topology (N = 5)

```text
       [D1] (idx 0)
       /  \
     [C1]  [C5]
     /       \
   [D2]     [D5]
   /           \
 [C2]          [C4]
   \           /
   [D3]     [D4]
     \       /
       [C3]
```

### The Thread Synchronization Cycle

The execution consists of three main cooperating layers:

```text
  +------------------+       Appends to       +--------------------+
  |   Coder Thread   | ---------------------> |  Scheduler Queue   |
  |  (C1, C2, ... )  |                        |   (Min-Heap Array) |
  +------------------+                        +--------------------+
           ^                                             |
           | Wakes up approved                           | Pops next
           | coder                                       v
  +------------------+                        +--------------------+
  |  Approval Signal | <--------------------- |  Scheduler Thread  |
  +------------------+                        +--------------------+
```

1. **Coder Threads**: Each coder runs a state machine:
   `Request Compilation -> Wait for Scheduler Approval -> Take Left & Right Dongles -> Compile (Hold) -> Release Dongles (Cooldown) -> Debug -> Refactor -> Repeat`.
2. **Scheduler Thread**: Acts as a centralized arbiter. It monitors the priority queue, pops the highest-priority coder thread according to the selected policy, and signals them to proceed.
3. **Monitor Thread**: Runs in the background as a watchdog, periodically checking if any coder has exceeded the burnout limit since their last compilation start.

---

## Why a Binary Min-Heap?

Standard C89 does not provide a built-in priority queue or heap data structure. While a doubly-linked list could be searched linearly in $O(N)$ time to find the next scheduled coder, a binary min-heap offers several engineering advantages:

1. **Time Complexity**:
   - **Insert (Push)**: $O(\log N)$ time, as the element bubbles up to its appropriate location.
   - **Extract Min (Pop)**: $O(\log N)$ time, as the root element is removed and the remaining elements are heapified down.
   - This provides scalable performance and deterministic latency guarantees.
2. **Unified Interface for FIFO and EDF**:
   - Under **FIFO**, priority is assigned based on a monotonically increasing global arrival counter.
   - Under **EDF**, priority is assigned based on the coder's absolute burnout deadline (`last_compile_start + burnout_time`).
   - Using a generic binary min-heap allows us to use the same sorting logic for both schedulers simply by modifying the comparison keys.
3. **Space Efficiency**:
   - The heap capacity is bounded by the total number of coders ($N$). By allocating a static array of size $N$ during initialization, we avoid any dynamic memory allocations or reallocations during runtime, preventing memory fragmentation and potential heap-allocation latency spikes.

---

## Instructions

### Compilation
Compile the project using the Makefile at the root of the repository:
```bash
make
```
This builds the `codexion` executable with `-Wall -Wextra -Werror -pthread` flags.

### Execution
Run the program by passing the mandatory arguments:
```bash
./codexion <number_of_coders> <time_to_burnout> <time_to_compile> <time_to_debug> <time_to_refactor> <number_of_compiles_required> <dongle_cooldown> <scheduler>
```

- **number_of_coders**: Total count of coders and dongles.
- **time_to_burnout**: Max milliseconds a coder can go without starting a compilation before burning out.
- **time_to_compile**: Milliseconds spent compiling (holding two dongles).
- **time_to_debug**: Milliseconds spent debugging.
- **time_to_refactor**: Milliseconds spent refactoring.
- **number_of_compiles_required**: Simulation stops when all coders compile at least this many times.
- **dongle_cooldown**: Milliseconds a dongle remains unavailable after being released.
- **scheduler**: Scheduling policy, must be exactly `fifo` or `edf`.

#### Example Run
```bash
./codexion 3 800 200 100 150 5 50 edf
./codexion 4 1500 200 200 200 5 100 fifo
```

#### Example Run with Valgrind
```bash
valgrind --leak-check=full ./codexion 50 800 200 100 150 3 50 edf
valgrind --tool=helgrind ./codexion 2 800 200 100 150 3 50 fifo > helgrind.txt 2>&1
```

---

## Blocking Cases Handled

- **Deadlock Prevention (Avoiding Coffman Conditions)**:
  - *Mutual Exclusion*: Protected using `pthread_mutex_t` per dongle.
  - *No Preemption*: Dongles are released voluntarily after compilation.
  - *Hold and Wait*: Solved via **lock backoff**. If a coder successfully locks their first dongle but finds the second dongle is busy or in its cooldown period, they immediately unlock the first dongle, sleep for a short duration (`usleep(1000)`), and retry. This breaks the hold-and-wait condition.
  - *Circular Wait*: Prevented by **lock ordering**. Coders always attempt to lock their lower-indexed dongle before locking their higher-indexed dongle.
- **Starvation**: Under the `edf` scheduler, coders with closer deadlines are prioritized to prevent them from hitting their burnout limit. FIFO guarantees that requests are processed in strict arrival order.
- **Cooldown Handling**: Dongle structures maintain a `cooldown_end` timestamp. Retrying mechanisms verify that the current timestamp is greater than or equal to `cooldown_end` before granting access.
- **Precise Burnout Detection**: The monitor thread polls coder deadlines with a resolution of 1ms (`usleep(1000)`). This ensures any burnout is reported within the required 10ms tolerance limit.
- **Log Serialization**: To prevent console outputs from interleaving or mixing lines, all actions and print statements are wrapped under a global `log_mutex`.

---

## Thread Synchronization Mechanisms

- `pthread_mutex_t`:
  - **Dongle Mutexes**: Protect the state of individual physical dongles.
  - **Coder Mutexes**: Protect the state transitions and compile counts of individual coders.
  - **Scheduler Mutex**: Synchronizes access to the binary heap during insertion and extraction.
  - **Log Mutex**: Ensures serialized, thread-safe stdout writing.
  - **Stop Mutex**: Safely handles the global boolean stop flag.
- `pthread_cond_t`:
  - **Scheduler CV (`scheduler.cond`)**: Used by the scheduler thread to sleep when there are no compilation requests, waking up as soon as a coder inserts themselves into the heap.
  - **Coder CV (`coder.cond`)**: Put to sleep when a coder is waiting for scheduler approval, and broadcasted when their request has been successfully popped and approved.
- `pthread_cond_broadcast`: 
  - To prevent thread hangs and clean up resources gracefully on shutdown, the monitor thread broadcasts to all condition variables, ensuring any blocked or waiting threads are woken up to terminate cleanly.

---

## Resources
- **Dining Philosophers Problem**: Classical synchronization pattern on resource sharing.
- **POSIX Thread Programming Reference**: Standard mutex and conditional variable behavior.
- **Binary Heap Algorithms**: Traditional parent/child index mapping on arrays:
  - $\text{Left Child} = 2 \times \text{Index} + 1$
  - $\text{Right Child} = 2 \times \text{Index} + 2$
  - $\text{Parent} = (\text{Index} - 1) / 2$
- **AI Tool Integration**: AI was utilized to draft structural logic for the lock backoff mechanism, analyze the safety of thread destruction paths, was leveraged to analyze race conditions in the binary min-heap implementation and format this documentation.
