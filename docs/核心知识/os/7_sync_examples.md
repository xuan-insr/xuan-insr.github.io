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

分析这里所需要的信号量，或者说「资源」。当一个 reader 进入 critical section 时，它会拿走 writer 的「资源」，但是当 writer 的「资源」不可用时，reader 并不需要等待；而当一个 writer 进入 critical section 时，它会等待并拿走公共的「资源」。

也就是说，大概的解决方案类似于：

```C linenums="1" hl_lines="16 20"
semaphore write_lock = 1;
semaphore public_lock = 1;

writer() {
    while (true) {
        wait(write_lock);       // guarantee no readers
        wait(public_lock);      // guarantee no readers or other writers
        read_and_write();
        signal(public_lock);
        signal(write_lock);
    }
}

reader() {
    while (true) {
        if (write_lock available)       // take write_lock but not wait
            wait(write_lock);
        wait(public_lock);              // guarantee no writers
        read();
        if (no other readers reading)   // release write_lock when ...
            signal(write_lock);         // ... no other readers reading
        signal(public_lock);
    }
}
```

可以看到，`reader()` 部分有两个用伪代码表示的片段，用高亮表示。这两个片段的难点分别在于：我们暂时没有手段不阻塞地检查某个信号量是否非 0；以及我们如何知道是否存在其他的 readers。

后面这个问题比较好解决，我们引入一个整型 `reader_count` 用来保存有多少个 readers，当其值变为 0 时，代表没有其他 readers 在读了。我们同时增加保证其同步的信号量。即：

```C linenums="1" hl_lines="3-4 22-24 28-32"
semaphore write_lock = 1;
semaphore public_lock = 1;
int reader_count = 0;
semaphore reader_count_lock = 1;

writer() {
    while (true) {
        wait(write_lock);       // guarantee no readers
        wait(public_lock);      // guarantee no readers or other writers
        read_and_write();
        signal(public_lock);
        signal(write_lock);
    }
}

reader() {
    while (true) {
        if (write_lock available)   // take write_lock but not wait
            wait(write_lock);
        wait(public_lock);          // guarantee no writers
        
        wait(reader_count_lock);
        reader_count++;
        signal(reader_count_lock);

        read();
        
        wait(reader_count_lock);
        reader_count--;
        if (reader_count == 0)      // release write_lock when ...
            signal(write_lock);     // ... no other readers reading
        signal(reader_count_lock);

        signal(public_lock);
    }
}
```

而对于第一个问题，也就是我们希望「当 `write_lock` 没有被占有时，获取之；但是如果已经被占有，不应当等待」，又该如何解决呢？显然，这个问题的解决方案仍然应该是 `if(cond) wait(write_lock);` 的形式，因为我们并没有其他获取一个锁的方法，因此关键就在于这个条件 `cond` 了。

既然我们没有办法不阻塞地判断这个信号量是否为 0，我们不妨回到什么情况下会让它变为 0 的这个问题上来。很显然，我们的目的是，让 **第一个** reader 在 entry section 中拿走 `write_lock`，而后续的 reader 不应在此阻塞。（注意，当 `write_lock` 被释放后，下一次来的 reader 也是「第一个」。）所以其实我们需要判断的核心可以是「第一个」reader，这其实也可以用之前的 `reader_count` 实现：

```C linenums="1" hl_lines="18-22"
semaphore write_lock = 1;
semaphore public_lock = 1;
int reader_count = 0;
semaphore reader_count_lock = 1;

writer() {
    while (true) {
        wait(write_lock);       // guarantee no readers
        wait(public_lock);      // guarantee no readers or other writers
        read_and_write();
        signal(public_lock);
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

        wait(public_lock);          // guarantee no writers

        read();
        
        wait(reader_count_lock);
        reader_count--;
        if (reader_count == 0)      // release write_lock when ...
            signal(write_lock);     // ... no other readers reading
        signal(reader_count_lock);

        signal(public_lock);
    }
}
```

我们讨论一下可能出现的情况，证明其能满足要求：

1. 当前有 writer 在 CS：
    1. 新的 writer 会在 L8 `wait(write_lock)` 被阻塞；
    1. 接下来的第一个 reader 会在 L21 `wait(write_lock)` 被阻塞，其余 reader 会在 L18 `wait(reader_count_lock)` 被阻塞（当 writer 退出 CS 之后，这些 reader 能够正常运行）；
1. 当前有 reader 在 CS：
    1. 新的 writer 会在 L8 `wait(write_lock)` 被阻塞；
    1. 接下来的 reader 只会在 L18 以及 L28 处被短暂阻塞，但是在 `reader_count` 大于 1 的前提下，这两处对应的 CS 都能在有限时间内完成；
1. 当前没有进程在 CS，如果有一个 writer 和一个 reader 同时进入，那么必有其中之一被 `wait(write_lock)` 阻塞。

可以看到，上述解法能够满足 Critical-Section Problem 的基本要求，同时能够满足题目要求。

不过，我们会发现一个问题：上述 1.b. 指出，reader 会被 `wait(write_lock)` 阻塞而不是被 `public_lock` 阻塞，这和我们最初的想法不同。事实确实如此：在我们当初的设想中，reader 应当直接取走 `write_lock` 而不应被其阻塞，因而需要一个 `public_lock` 用来阻塞有 writer 情形下的 reader。但是由于信号量取得必须使用原语 `wait`，因此这里的阻塞是不可避免的，反而帮助我们代替了 `public_lock` 的作用。所以，实际上我们可以去掉它，最终得到的代码是：

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