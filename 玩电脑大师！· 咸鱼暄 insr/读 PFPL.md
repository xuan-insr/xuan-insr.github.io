
## I Judgments and Rules

### 1 Abstract Syntax
**抽象语法树** 

- AST
- 是一棵树，叶子结点是变量或者无参运算符，内部结点是运算符
- 具有不同的 **类型 sort**
   - 例如，表达式和命令就是两种不同的类型
- 多个 ast 可以通过运算符组合成一个新的 ast
- 运算符自身的类别，以及其各个参数的类别称为** 元数 arity**



**变量**

- 属于某个 **域 domain** 的未知对象，可以通过 **代换 substitution** 变为已知

**结构归纳法**

**抽象绑定树**


### 2 Inductive Definitions 归纳定义
**判断 judgment**
