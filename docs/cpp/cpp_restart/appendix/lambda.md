关于递归的 lambda：https://youtu.be/eD-ceG-oByA?t=1925

lambda 和其他 function object 作为参数传递时相较函数指针会有更好的优化，因为函数指针不易内联：https://stackoverflow.com/questions/13722426/why-can-lambdas-be-better-optimized-by-the-compiler-than-plain-functions ；但同时注意每个 function object 都会使得模板产生一个新的特化

lambda 在没有 capture 时扮演「better function」的身份，例如能够转为函数指针；当有 capture 时实现了 function 做不到的功能：functions with "states": capture behavior parameter to deal with call parameters

视频看到 https://youtu.be/IgNUBw3vcO4?t=1622 这里了