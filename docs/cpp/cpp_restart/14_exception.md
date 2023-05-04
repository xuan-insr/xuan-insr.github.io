`std::expect` C++23 https://youtu.be/eD-ceG-oByA?t=2236

关于 STL 的 move / copy: https://godbolt.org/z/YceThebxa ；如果操作失败，STL 希望能保持操作前的完整样子；因此除非 move ctor 是 `noexcept` 的，否则会使用 copy ctor 来保证安全。