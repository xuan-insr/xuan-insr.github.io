# 7 Synchronization Examples

## 7.1 经典同步问题

一般我们用信号量解决问题，因为信号量相对来说功能更多，而且很多操作系统对信号量做了更多设计，用来避免 busy waiting 等问题。

信号量的逻辑其实非常简单：一个信号量用来表示 **一类「资源」的余量**；`wait()` 等待到其有余量时从中取走一个，而 `signal()` 释放一个资源。因此，在用信号量解决同步问题时，我们通常考虑哪些东西属于资源，对它们的访问有哪些。同时，通过考虑在哪些地方需要等待，我们也能够得到一些提示。

### 7.1.1 Bounded-Buffer Problem

!!! info "Bounded-Buffer Problem"
    给定两个进程：producer 和 consumer，它们共用大小为 $n$ 的 buffer。Producer 生产数据放入 buffer，consumer 从 buffer 取出数据从而使用之。

    该问题需要保证：producer 不应当在 buffer 满时放入数据，consumer 也不应当在 buffer 空时取出数据。

首先，根据我们在前一节中的讨论，produce 和 consume 的过程会访问到 `buffer` 的资源，因此是 critical section，我们需要使用一个锁（或者信号量，后同）来控制对 `buffer` 的访问：

```C linenums="1"
semaphore lock = 1;

producer() {
    while (true) {
        // <1> If buffer is full, wait 
        wait(lock);
        add_to_buffer(next_produced);
        signal(lock);
    }
}

consumer() {
    while (true) {
        // <2> If buffer is empty, wait
        wait(lock);
        next_consumed = take_from_buffer();
        signal(lock);
    }
}
```

不过，上面两处注释中要求根据 `buffer` 的容量决定是否需要等待的需求还没有实现。

我们可以考虑使用一个变量 `count` 来记录 `buffer` 中有多少个元素；如果这样实现的话，对 `count` 的修改也是 critical section，因此也需要锁的控制：

```C linenums="1"
semaphore lock = 1;
int count = 0;

producer() {
    while (true) { 
        wait(lock);
        while (count == BUFFER_SIZE) ;  // If buffer is full, wait 
        add_to_buffer(next_produced);
        count++;
        signal(lock);
    }
}

consumer() {
    while (true) {
        wait(lock);
        while (count == 0) ;    // If buffer is empty, wait
        next_consumed = take_from_buffer();
        count--;
        signal(lock);
    }
}
```

这种方式的实现问题是显然的：比如当前 `buffer` 为空，即 `count` 为 0，`consumer` 会在 16 行处等待；但因为此时它持有着 `lock`，任何 producer 都不能 produce，因此这个等待会永久持续下去。这违反了 **Progress** 和 **Bounded waiting** 的要求。

我们可以稍作修改，当 `count` 的要求不满足时，立即释放 `lock` 并进入下一次循环，即：

```C linenums="1"
semaphore lock = 1;
int count = 0;

producer() {
    while (true) { 
        wait(lock);
        if (count == BUFFER_SIZE) {
            // If buffer is full, give up
            signal(lock);
            continue;
        } else {
            add_to_buffer(next_produced);
            count++;
            signal(lock);
        }
    }
}

consumer() {
    while (true) {
        wait(lock);
        if (count == 0) {
            // If buffer is empty, give up
            signal(lock);
            continue;
        } else {
            next_consumed = take_from_buffer();
            count--;
            signal(lock);
        }
    }
}
```

也就是：

```C linenums="1"
semaphore lock = 1;
int count = 0;

producer() {
    while (true) { 
        wait(lock);
        if (count != BUFFER_SIZE) {
            add_to_buffer(next_produced);
            count++;
        }
        signal(lock);
    }
}

consumer() {
    while (true) {
        wait(lock);
        if (count != 0) {
            next_consumed = take_from_buffer();
            count--;
        }
        signal(lock);
    }
}
```

但是，这种实现方法强制了 busy waiting。我们在前一节讨论过了 busy waiting 及其利弊；在这里 critical section 的运行时间明显比 context switch 的时间要长，因此这里使用 busy waiting 是浪费时间的。

而我们之前提到，许多操作系统对信号量做了一些处理，使得其等待不再是 busy waiting，而是类似于第 6 节中讲到的解决方案。因此，我们更倾向于使用信号量来解决问题。

首先我们尝试使用一个 `lock`  和一个 `eslot` (empty slot，空闲 buffer 的个数) 来解决：

```C linenums="1"
semaphore lock = 1;
semaphore eslot = BUFFER_SIZE;

producer() {
    while (true) {
        wait(eslot);    // if buffer is full, i.e. eslot == 0, wait
                        // else, eslot--
        wait(lock);
        add_to_buffer(next_produced);
        signal(lock);
    }
}

consumer() {
    while (true) {
        // <2> If buffer is empty, i.e. eslot == BUFFER_SIZE, wait
        wait(lock);
        next_consumed = take_from_buffer();
        signal(lock);
        signal(eslot);  // eslot++
    }
}
```

由于 `eslot` 作为一个信号量，我们对它 `++` 和 `--` (实际上是 `wait` 和 `signal`) 是 atomic 的，不需要考虑同步问题。

但是，16 行处我们希望让 `eslot == BUFFER_SIZE` 的时候循环等待，不过信号量本身并没有提供这个功能。怎么办呢？我们需要一个额外的 semaphore `fslot`  (full slot) 来解决这个问题：

```C linenums="1"
semaphore lock = 1;
semaphore eslot = BUFFER_SIZE;
semaphore fslot = 0;

producer() {
    while (true) {
        wait(eslot);    // if buffer is full, i.e. eslot == 0, wait
                        // else, eslot--
        wait(lock);
        add_to_buffer(next_produced);
        signal(lock);
        signal(fslot);  // fslot++
    }
}

consumer() {
    while (true) {
        wait(fslot);    // if buffer is empty, i.e. fslot == 0, wait
                        // else, fslot--
        wait(lock);
        next_consumed = take_from_buffer();
        signal(lock);
        signal(eslot);  // eslot++
    }
}
```

事实上，如我们之前所说，分析两处需要 wait 的情况（即 producer 在 buffer 满时、consumer 在 buffer 空时）就可以得到使用信号量的提示。也就是说，对于 producer 来说，「空格子」是它需要的资源；而对于 consumer 来说，「有东西的格子」是它需要的资源。我们可以根据这样的提示来设计信号量。

需要特别注意的是 `wait` 之间的顺序。例如如果将 `wait(lock)` 和 `wait(fslot)` 的顺序调转过来，就会发生和前面提到的情况一样的死锁。

### 7.1.2 Readers-Writers Problem

!!! info "Readers-Writers Problem"
    对一个数据，readers 读，writers 读和写。
    
    设计方案保证：多个 readers 可以同时读取，但是 writer 进行读写时不能有其他 writers 和 readers。

也就是说，我们希望的方案大概如下：

```C linenums="1"
writer() {
    while (true) {
        // if there is any reader or any other writer, wait
        read_and_write();
    }
}

reader() {
    while (true) {
        // if there is any writer, wait
        read();
    }
}
```

我们分类讨论不同的情形下，reader 和 writer 在 entry section 中期望的做法：

对于 reader：

- 有 writer：等待
- 有其他 reader：什么都不做，直接进入 CS
- 都没有：禁止 writer，然后进入 CS

这样的做法可以保证不会同时有 writer 和 reader 在 critical section。

对于 writer；

- 有其他 reader / writer：等待
- 都没有：禁止 reader 和其他 writer，然后进入 CS

在 exit section 的操作与之对称。

这两处「禁止」可能对应着两处信号量，我们分别给它们起名为 `R` 和 `W`，初值均为 1；那么 reader 的 entry section 就形如：

```C linenums="1"
wait for W but not take;    // if there is a writer, wait
if (no other readers)       // if no other readers, take R
    wait(R);                // else, do nothing
```

writer 的 entry section 形如：

```C linenums="1"
wait for R but not take;    // if there are some readers, wait
wait(W);                    // if there is another writer, wait; else take W
```

这里有两个问题没有解决，第一个是「wait but not take」这样的操作是不存在的，第二个是如何判定「no other readers」。我们分别讨论这两个问题。

首先，wait but not take 肯定还是要使用 `wait()` 来解决的，因为我们没有除此之外的用来等待的信号量操作。我们分别考虑两处 wait but not take 如果直接用 `wait()` 实现会带来什么问题。

对于 reader，如果我们直接改为 `wait(W)`，会出现的问题是：这样只有第一个 reader 能够进入 CS 了，后续的都会被阻塞。不过我们可以发现，要解决这个问题，只要把 `wait(W)` 也放到 `if` 里面去就好了，也就是说如果有其他 reader 在的情况下，一定不存在 writer，`W` 也一定被某个（第一个）reader 持有，就不需要再 wait 了。即：

```C linenums="1"
if (no other readers) {
    wait(W);
    wait(R);      
}         
```

容易检查，这样的设计符合我们之前分类讨论的要求。

对于 writer，我们可以直接改为 `wait(R)`，因为释放 `W` 之前一定不会有 reader 能够进入 CS，而释放 `W` 时可以一并释放 `R`。即：

```C linenums="1"
wait(R);      
wait(W);
```

这里本来应该检查一下死锁，因为从第 8 节可以看到，这种设计有循环等待的情况，因此有死锁的风险；但是我们可以发现，其实 `R` 和 `W` 总是会同时被获取（对称地，也同时被释放），因此其实我们可以合并为一个信号量，不妨叫做 `write_lock`。其设计为：

```C linenums="1"
semaphore write_lock = 1;

writer() {
    while (true) {
        wait(write_lock);
        read_and_write();
        signal(write_lock);
    }
}

reader() {
    while (true) {
        if (no other readers)
            wait(write_lock);
        read();
        if (no other readers)
            signal(write_lock);
    }
}
```

「no other readers」这个问题比较好解决，我们引入一个整型 `reader_count` 用来保存有多少个 readers，当其值变为 0 时，代表没有其他 readers 在读了。我们同时增加保证其同步的信号量。即：

```C linenums="1"
semaphore write_lock = 1;
int reader_count = 0;
semaphore reader_count_lock = 1;

writer() {
    while (true) {
        wait(write_lock);
        read_and_write();
        signal(write_lock);
    }
}

reader() {
    while (true) {
        wait(reader_count_lock);
        reader_count++;
        if (reader_count == 1)     // first reader take write_lock
            wait(write_lock);
        signal(reader_count_lock);

        read();
        
        wait(reader_count_lock);
        reader_count--;
        if (reader_count == 0)      // release write_lock when ...
            signal(write_lock);     // ... no other readers reading
        signal(reader_count_lock);
    }
}
```

另外需要注意的是，这种实现的结果是：当存在读进程时，写进程将被延迟。这可能导致写进程发生 **starvation**。

如果希望写进程优先，我们可以规定，如果写进程 ready，那么其他读进程应当等待，直到写进程结束；即使得写进程尽可能早地开始。我们可以通过新增一个信号量实现：

```C linenums="1" hl_lines="3 8 12 18 24"
semaphore write_lock = 1;
int reader_count = 0;
semaphore reader_count_lock = 1;
semaphore writer_first = 1;

writer() {
    while (true) {
        wait(writer_first);
        wait(write_lock);
        read_and_write();
        signal(write_lock);
        signal(writer_first);
    }
}

reader() {
    while (true) {
        wait(writer_first);
        wait(reader_count_lock);
        reader_count++;
        if (reader_count == 1)
            wait(write_lock);
        signal(reader_count_lock);
        signal(writer_first);

        read();
        
        wait(reader_count_lock);
        reader_count--;
        if (reader_count == 0)
            signal(write_lock);
        signal(reader_count_lock);
    }
}
```

### 7.1.3 Dining-Philosophers Problem

!!! info "Dining-Philosophers Problem"
    5 个哲学家一起吃饭！每两个哲学家之间有一根筷子，每个人一次可以拿起来一根筷子，拿到两根筷子的就可以吃一段时间。吃完思考一段时间。

    <center>![](2022-11-19-00-17-19.png)</center>

一个朴素的解法是这样的：

```C linenums="1"
vector<semaphore> chopstick(5, 1);  // initialize semaphores to all 1

philosopher(int index) {
    while (true) {
        wait(chopstick[i]);
        wait(chopstick[(i + 1) % 5]);
        eat();
        signal(chopstick[i]);
        signal(chopstick[(i + 1) % 5]);
        think();
    }
}
```

问题是，可能某时刻每个人同时拿起左边的筷子，这样会导致死锁。

解决方案之一是，只允许同时拿起两根筷子；这种方案的实现是，轮流询问每个人是否能够拿起两根筷子，如果能则拿起，如果不能则需要等待那些筷子放下：

```C linenums="1"  hl_lines="2 6 9"
vector<semaphore> chopstick(5, 1);  // initialize semaphores to all 1
semaphore lock = 1;

philosopher(int index) {
    while (true) {
        wait(lock);
        wait(chopstick[i]);
        wait(chopstick[(i + 1) % 5]);
        signal(lock);

        eat();
        
        signal(chopstick[i]);
        signal(chopstick[(i + 1) % 5]);
        think();
    }
}
```

另一种解决方案是，奇数号人先拿左边筷子，偶数号人先拿右边筷子，这样也能避免死锁。

## 7.2 Linux Sync

2.6 以前的版本的 kernel 中通过禁用中断来实现一些短的 critical section；2.6 及之后的版本的 kernel 是抢占式的。

Linux 提供：

- Atomic integers
- Spinlocks
- Semaphores
- Reader-writer locks

## 7.3 POSIX Sync