Fwiw, _all_ modern time pieces work by **counting **a regularly occurring event. This trend started in 1656 with the first pendulum clock that "counted" the swings of an oscillating pendulum.<br />Pendulum → quartz crystal → atomic vibrations<br />OR: ask and converage upon a consensus: NTP.

[Epoch (computing) - Wikipedia](https://en.wikipedia.org/wiki/Epoch_(computing))

[Time Stamp Counter - Wikipedia](https://en.wikipedia.org/wiki/Time_Stamp_Counter)
The **Time Stamp Counter** (**TSC**) is a 64-bit register present on all x86 processors since the Pentium. It counts the number of CPU cycles since its reset. The instruction RDTSC returns the TSC in EDX:EAX. (~MHz)
The Time Stamp Counter was once an excellent high-resolution, low-overhead way for a program to get CPU timing information. <br />With the advent of multi-core/hyper-threaded CPUs, systems with multiple CPUs, and hibernating operating systems, the TSC cannot be relied upon to provide accurate results. There is no promise that the timestamp counters of multiple CPUs on a single motherboard will be synchronized. With the SpeedStep technology, the processor clock may also be impacted.<br />Recent Intel processors include a constant rate TSC (identified by the kern.timecounter.invariant_tsc sysctl on FreeBSD or by the "constant_tsc" flag in Linux's /proc/cpuinfo). With these processors, the TSC ticks at the processor's nominal frequency (called "reference cycles"), regardless of the actual CPU clock frequency due to turbo or power saving states. Hence TSC ticks are counting the passage of time, not the number of CPU clock cycles elapsed. 

[c++ - Calculate system time using rdtsc - Stack Overflow](https://stackoverflow.com/questions/42189976/calculate-system-time-using-rdtsc)
The TSC frequency may not be the same as the frequency in the brand string

[How is a computer still able to know the correct time even after it has been completely turned off for a long time? - Quora](https://www.quora.com/How-is-a-computer-still-able-to-know-the-correct-time-even-after-it-has-been-completely-turned-off-for-a-long-time)
[cpu - How is time measured in computer systems? - Super User](https://superuser.com/questions/253471/how-is-time-measured-in-computer-systems)
CMOS **real-time-clock (RTC)**  (figure) , w/ quartz crystals & battery, not very accurate (~10kHz)
Internet time - Atomic Clocks, Network Time Protocol (NTP, ~μs), can change RTC; there is Precision Time Protocol (PTP) which can reach sub-μs accuracy <br />**Programmable Interval Timer (PIT)** , triggers interrupt when scheduled. Used in UP (uniprocessor) systems, but is not used in SMP (symmetric multiprocessing) systems. The latter uses **Advanced Programmable Interrupt Controller (APIC)** timer instead. (~MHz)
**High Precision Event Timer (HPET)** , >10MHz

[https://stackoverflow.com/a/46624236/14430730](https://stackoverflow.com/a/46624236/14430730)
[gcc/chrono.cc at master · gcc-mirror/gcc (github.com)](https://github.com/gcc-mirror/gcc/blob/master/libstdc++-v3/src/c++11/chrono.cc#L52)
[linux - Difference between CLOCK_REALTIME and CLOCK_MONOTONIC? - Stack Overflow](https://stackoverflow.com/questions/3523442/difference-between-clock-realtime-and-clock-monotonic)

- **TSC** ~~std::chrono::steady_clock , use clock_gettime(CLOCK_REALTIME), or gettimeoffay()~~ . Thanks to VDSO, this can run purely in user-space**<br />
   - might be adjusted according to NTP so may jump forwards or backwards
   - CLOCK_MONOTONIC_RAW will not affected by NTP (or will, but will not jump? so will CLOCK_MONOTONIC )
      - but it maybe not in VDSO, so it can be very slow relatively
- **RTC** ~~std::chrono::system_clock , use clock_gettime(CLOCK_MONOTONIC)~~ 
   - [https://stackoverflow.com/a/17663339/14430730](https://stackoverflow.com/a/17663339/14430730)
   - The important aspect of a monotonic time source is NOT the current value, but the guarantee that the time source is strictly linearly increasing, and thus useful for calculating the difference in time between two samplings



[(52 封私信 / 81 条消息) 时间测量方法？ - 知乎 (zhihu.com)](https://www.zhihu.com/question/28559933)

- grep tsc /proc/cpuinfo  constant_tsc , nonstop_tsc 



The x86 timestamp counter (TSC), despite its flaws, is still a good way to measure event duration for profiling and benchmarking.<br />To translate TSC tics to seconds, we need to know how fast the TSC is ticking.
