[http://www.concrete-semantics.org/theories.html](http://www.concrete-semantics.org/theories.html)
[http://www.concrete-semantics.org/concrete-semantics.pdf](http://www.concrete-semantics.org/concrete-semantics.pdf)
 

## 2.1 Basis

### 2.1.1 Types, Terms and Formulas

- 基本类型：bool, nat (![](https://cdn.nlark.com/yuque/__latex/af78e8e0d93943ec0d334f2f0465afce.svg#card=math&code=%5Cmathbb%7BN%7D&id=UhiBm)), int (![](https://cdn.nlark.com/yuque/__latex/d249f1b67fcffb4fb625518eb53a14d0.svg#card=math&code=%5Cmathbb%7BZ%7D&id=Ev88m))
- 类型构造器：list, set
   - 例如`nat list`就表示一个元素为`nat`的列表
- 函数类型：`⇒`
   - 例如![](https://cdn.nlark.com/yuque/__latex/4c59cce24d74de42ca380e40e5756fff.svg#card=math&code=%5Ctau_1%20%5CRightarrow%20%5Ctau_2&id=ufdpR)就表示一个类型![](https://cdn.nlark.com/yuque/__latex/cf6ab1758bae08e565d32108a2a2c007.svg#card=math&code=%5Ctau_1&id=KLNR2)到类型![](https://cdn.nlark.com/yuque/__latex/1688386ac720f09b4e2f2badab82f199.svg#card=math&code=%5Ctau_2&id=EbJHe)的函数（say `f`)。如果`t`是![](https://cdn.nlark.com/yuque/__latex/cf6ab1758bae08e565d32108a2a2c007.svg#card=math&code=%5Ctau_1&id=lwMAG)类型的一个 term（_Terms are formed as by applying functions to arguments_，记为 ![](https://cdn.nlark.com/yuque/__latex/2473f1f4dbda88d7acdf950e151783c4.svg#card=math&code=t%20%3A%3A%20%5Ctau_1&id=jIcko)），那么由于![](https://cdn.nlark.com/yuque/__latex/919e5b2c56e8f84c6c2ec87f1eca4ff5.svg#card=math&code=f%3A%5Ctau_1%5CRightarrow%5Ctau_2&id=ZX8Uw)，因此![](https://cdn.nlark.com/yuque/__latex/9570ede67a925a334e26ac5d94122743.svg#card=math&code=f%5C%20t%3A%3A%5Ctau_2&id=nlxOd)。
- 类型变量：形如`a'`, `b'`

![image.png](./assets/1658915126858-cf59b388-d887-4cd3-a668-7936111a491a.png)
![image.png](./assets/1658915137039-2cc34d2a-a939-406e-9a42-00e24f4b1c1b.png)
![image.png](./assets/1658915192237-813a17da-6d89-431e-966d-a5b1c974ae95.png)
![image.png](./assets/1658915799633-7962d50a-e638-4598-8fe3-72ad4f2af0e6.png)

对于变量，有时需要显式的 type constraint（或称 type annotation）以便消除可能的二义性，尤其是在`(+)`之类的 overloaded functions，形如`m + (n::nat)`
![image.png](./assets/1658915966829-a29aa220-ea7a-4d6a-ad94-d2a1fe2b63ca.png)


### 2.1.2 Theories
![image.png](./assets/1659357394563-7d7f1eea-5980-4603-98cd-ba0dcf38c6ea.png)
类似 Pascal 的 program，必须存在`T.thy`文件里
![image.png](./assets/1659357434911-2185dd33-949e-4060-a448-8ea80efb5d09.png)




## 2.2 bool, nat, list
![image.png](./assets/1659358172436-8709d9df-6e1f-430e-a105-51692da29c18.png)
![image.png](./assets/1659360672567-7017e1e9-6f5a-400d-8fff-8526f99f03a5.png)
![image.png](./assets/1659360690491-2e4b8ca3-e3a9-4799-af1d-d926ece4bc7a.png)
![image.png](./assets/1659369238509-b4898b96-a1bd-481c-ae60-0bd5942c0310.png)
![image.png](./assets/1659369271381-f76bd114-f719-4d34-bcc8-34c1aa4fd086.png)

---

```
theory Xyx
  imports Main
begin

(* § 2.2 *)
(* define function add *)
(* ⇒ can be typed with = plus > *)
fun add :: "nat ⇒ nat ⇒ nat" where
"add 0 n = n" |
"add (Suc m) n = Suc (add m n)"

(* example of prove by induction *)
lemma add_0n: "n = add n 0"
  apply(induction n)
   apply(auto)
  done

thm add_0n
full_prf add_0n

(* define datatype lst and functions *)
datatype 'a lst = Nil | Cons 'a "'a lst"

value "Cons True Nil"

fun app :: "'a lst ⇒ 'a lst ⇒ 'a lst" where
"app Nil x = x" |
"app (Cons x fs) y = Cons x (app fs y)"

fun lstrev :: "'a lst ⇒ 'a lst" where
"lstrev Nil = Nil" |
"lstrev (Cons x fs) = app (lstrev fs) (Cons x Nil)"

value "lstrev (Cons True (Cons False Nil))"
value "app (Cons True Nil) (Cons False Nil)"

(* prove lstrev (lstrev s) = s by structural induction *)
(* [simp] means that all "app xs Nil" can be simplified by "xs" from now on. See § 2.5 *)
lemma app_Nil [simp] : "app xs Nil = xs"
  apply(induction xs)
   apply(auto)
  done

lemma app_assoc [simp] : "app (app xs ys) zs = app xs (app ys zs)"
  apply(induction xs)
   apply(auto)
  done

lemma lstrev_app [simp] : "lstrev (app xs ys) = app (lstrev ys) (lstrev xs)"
  apply(induction xs)
   apply(auto)
  done

theorem lstrev_lstrev [simp] : "lstrev (lstrev xs) = xs"
  apply(induction xs)
   apply(auto)
  done

full_prf lstrev_lstrev

(* built-in list and its syntatic sugar & predefined functions *)
value "[]::nat list"

(* we can define a name with 'definition' *)
definition "list1 = 4#[1::nat, 2, 3]@[7, 8]"
value "4#[1::nat, 2, 3]@[7, 8]"
value "length list1"

fun double :: "nat ⇒ nat" where "double x = x * 2"
value "map double list1"
value "hd list1"
value "tl list1"

(* T 2.2 *)
theorem add_assoc: "add (add m n) p = add m (add n p)"
  apply(induction m)
   apply(auto)
  done
thm add_assoc

lemma add_mn1: "add (Suc n) m = add n (Suc m)"
  apply(induction n)
   apply(auto)
  done
thm add_mn1

theorem add_comm: "add m n = add n m"
  using add_0n
  using add_mn1
  apply(induction m)
   apply(auto)
  done

(* T 2.3 *)
fun length :: "'a lst ⇒ nat" where
"length Nil = 0" |
"length (Cons x fs) = Suc(length fs)"

value "length (app (Cons True (Cons False Nil)) (Cons False Nil))"

fun count :: "'a lst ⇒ 'a ⇒ nat" where
"count Nil x = 0" |
"count (Cons y fs) x = (if x = y then Suc(count fs x) else (count fs x))"

value "count (app (Cons True (Cons False Nil)) (Cons False Nil)) False"
value "count (app (Cons True (Cons False Nil)) (Cons False Nil)) True"

(* ≤ can be typed with < and = *)
theorem "count xs x ≤ length xs"
  apply(induction xs)
   apply(auto)
  done

(* T 2.4 *)
fun snoc :: "'a lst ⇒ 'a ⇒ 'a lst" where
"snoc Nil x = Cons x Nil" |
"snoc (Cons x fs) y = Cons x (snoc fs y)"

value "snoc (snoc (Cons True Nil) False) False"

fun lstreverse :: "'a lst ⇒ 'a lst" where
"lstreverse Nil = Nil" |
"lstreverse (Cons x fs) = snoc (lstreverse fs) x"

value "lstreverse (snoc (snoc (Cons True Nil) False) False)"

(* TODO: prove rev(rev xs) = xs by structural induction *)
lemma lstrev_sx: "lstreverse (snoc xs x) = Cons x (lstreverse xs)"
  apply(induction xs)
   apply(auto)
  done

(*
theorem "lstreverse (lstreverse xs) = xs"
  apply(induction xs)
   apply(auto)
  done
*)

(* T 2.5 *)
fun sum_upto :: "nat ⇒ nat" where
"sum_upto 0 = 0" |
"sum_upto n = n + sum_upto (n-1)"

value "sum_upto 10"

theorem "sum_upto n = n * (n + 1) div 2"
  apply(induction n)
   apply(auto)
  done

(* § 2.3 *)
type_synonym string = "char list"

(* define datatype (binary) tree and function mirror *)
datatype 'a tree = Tip | Node "'a tree" 'a "'a tree"

fun mirror :: "'a tree ⇒ 'a tree" where
"mirror Tip = Tip" |
"mirror (Node l a r) = Node (mirror r) a (mirror l)"

lemma "mirror (mirror t) = t"
  apply(induction t)
   apply(auto)
  done

(* define datatype option and function lookup using it *)
datatype 'a option = None | Some 'a

fun lookup :: "('a * 'b) list ⇒ 'a ⇒ 'b option" where
"lookup [] _ = None" |
"lookup ((a, b)#ps) x = (if a = x then Some b else lookup ps x)"

value "lookup ([(1::nat, abc), (3, def)]) 3"
value "lookup ([(1::nat, abc), (3, def)]) 0"

(* non-recursive function can be defined using 'definition' *)
definition square :: "nat ⇒ nat" where "square x = x * x"

(* abbreviation is like inline function *)
(* ≡ can be typed by \equiv or use == instead *)
abbreviation sq :: "nat ⇒ nat" where "sq x ≡ x * x"

(* T 2.6 *)
fun contents :: "'a tree ⇒ 'a list" where
"contents Tip = []" |
"contents (Node l a r) = a # contents l @ contents r"

fun sum_tree :: "nat tree ⇒ nat" where
"sum_tree Tip = 0" |
"sum_tree (Node l a r) = a + sum_tree l + sum_tree r"

definition "tree1 == (Node (Node Tip 6 (Node Tip 5 Tip)) 3 Tip)::nat tree"
value "contents tree1"
value "sum_tree tree1"
value "sum_list (contents tree1)"
value "mirror tree1"

lemma "sum_tree t = sum_list (contents t)"
  apply(induction t)
   apply(auto)
  done

(* T 2.7 *)
datatype 'a tree2 = Tip | Leaf 'a | Node "'a tree2" "'a tree2"

fun mirror2 :: "'a tree2 ⇒ 'a tree2" where
"mirror2 Tip = Tip" |
"mirror2 (Leaf x) = Leaf x" |
"mirror2 (Node l r) = Node (mirror2 r) (mirror2 l)"

fun pre_order :: "'a tree2 ⇒ 'a list" where
"pre_order Tip = []" |
"pre_order (Leaf x) = [x]" |
"pre_order (Node l r) = pre_order l @ pre_order r"

fun post_order :: "'a tree2 ⇒ 'a list" where
"post_order Tip = []" |
"post_order (Leaf x) = [x]" |
"post_order (Node l r) = post_order r @ post_order l"

definition "tree2 == (Node (Node (Leaf 4) (Leaf 3)) (Node (Leaf 5) (Node (Leaf 2) Tip)))::nat tree2"
value "mirror2 tree2"
value "pre_order tree2"
value "post_order tree2"

lemma "pre_order (mirror2 t) = post_order t"
  apply(induction t)
   apply(auto)
  done

(* T 2.8 TODO *)
fun intersperse :: "'a ⇒ 'a list ⇒ 'a list" where
"intersperse a [] = []" |
"intersperse a [x] = [x]" | 
"intersperse a (x#xs) = [x, a] @ intersperse a xs"

value "intersperse 0 [1::nat, 2, 3]"
value "intersperse 0 [1::nat]"
value "intersperse 0 []::nat list"

(*
lemma "map f (intersperse a xs) = intersperse (f a) (map f xs)"
  apply(induction xs)
   apply(auto)
  done
*)

(* § 2.4 *)

(* this function is better than rev because of linear complexity and tail-recursive *)
fun itrev :: "'a list ⇒ 'a list ⇒ 'a list" where
"itrev [] ys = ys" |
"itrev (x#xs) ys = itrev xs (x#ys)"

(* But it's hard to prove lemma "itrev xs [] = rev xs" *)

(* The key heuristic, and the main point of this section, is to generalize the
goal before induction. The reason is simple: if the goal is too specific, the
induction hypothesis is too weak to allow the induction step to go through. *)

(* So we will generalize the lemma: *)
lemma "itrev xs ys = rev xs @ ys"
  apply(induction xs arbitrary: ys)
   apply(auto)
  done
(* the problem is that the ys in the induction hypothesis is fixed,
but the induction hypothesis needs to be applied with a # ys instead of ys.
Hence we prove the theorem for all ys instead of a fixed one. We can instruct
induction to perform this generalization for us by adding arbitrary: ys. *)

(* T 2.9 *)
fun itadd :: "nat ⇒ nat ⇒ nat" where
"itadd 0 n = n" |
"itadd (Suc m) n = itadd m (Suc n)"

value "itadd 4 100"

lemma suc_add: "add m (Suc n) = Suc (add m n)"
  apply(induction m)
   apply(auto)
  done

lemma "itadd m n = add m n"
  using suc_add
  apply(induction m arbitrary: n)
   apply(auto)
  done

(* § 2.5 NOTE: something omitted *)
(* IMPORTANT: simp is in § 2.5 *)

(* T 2.10 *)
datatype tree0 = Tip | Node tree0 tree0

fun nodes :: "tree0 ⇒ nat" where
"nodes Tip = 0" |
"nodes (Node l r) = nodes l + nodes r + 1"

fun explode :: "nat ⇒ tree0 ⇒ tree0" where
"explode 0 t = t" |
"explode (Suc n) t = explode n (Node t t)"


lemma explode_once: "nodes (explode a (Node t t)) = 2 * nodes (explode a t) + 1"
  apply(induction a arbitrary: t)
   apply (auto simp: algebra_simps)
  done

(* IMPORTANT Hint: simplifying with the list of theorems algebra_simps takes care of
common algebraic properties of the arithmetic operators. *)
lemma "nodes (explode a t) = 2 ^ a * nodes t + 2 ^ a - 1 "
  apply(induction a arbitrary: t)
   apply (auto simp: algebra_simps)
  done

(* T 2.11 TODO *)
datatype exp = Var | Const int | Add exp exp | Mult exp exp

fun eval :: "exp ⇒ int ⇒ int" where
"eval Var x = x" |
"eval (Const a) _ = a" |
"eval (Add a b) x = eval a x + eval b x" |
"eval (Mult a b) x = eval a x * eval b x"

value "eval (Add (Mult (Const 2) Var) (Const 3)) 4"

fun evalp :: "int list ⇒ int ⇒ int" where
"evalp [] _ = 0" |
"evalp l x = hd l + x * (evalp (tl l) x)"

value "evalp [4, 2, -1, 3] (-1)"

value "(*) (4::nat) 2"

fun add_coeffs :: "int list ⇒ int list ⇒ int list" where
"add_coeffs a [] = a" |
"add_coeffs [] b = b" |
"add_coeffs a b = (hd a + hd b) # (add_coeffs (tl a) (tl b))"

fun mul_coeffs :: "int list ⇒ int list ⇒ int list" where
"mul_coeffs _ [] = []" |
"mul_coeffs a b = add_coeffs (map ((*) (hd b)) a) (0 # (mul_coeffs a (tl b)))"

fun coeffs :: "exp ⇒ int list" where
"coeffs Var = [0, 1]" |
"coeffs (Const c) = [c]" |
"coeffs (Add a b) = add_coeffs (coeffs a) (coeffs b)" |
"coeffs (Mult a b) = mul_coeffs (coeffs a) (coeffs b)"

value "coeffs (Mult (Add (Mult (Const 2) Var) (Const 3)) (Add Var (Mult (Const (-2)) Var)))"
value "coeffs (Mult (Add (Mult (Const 2) Var) (Const 3)) (Const 2))"

(*
lemma evalp_add_coeffs: "evalp (add_coeffs a b) x = evalp a x + evalp b x"
  apply(induction b)
   apply(auto simp:algebra_simps)
  done

lemma evalp_mul_coeffs: "evalp (mul_coeffs a b) x = evalp a x * evalp b x"
  apply(induction b)
   apply(auto simp:algebra_simps)
  done

theorem evalp_coeffs: "evalp (coeffs e) x = eval e x"
  apply(induction e)
   apply(auto simp:algebra_simps)
  done
*)

end
```



## 3 IMP Expressions
IMP 是一门语言

### 3.1 Arithmetic

#### 3.1.1 语法
![image.png](./assets/1659583752759-a11189da-f7dc-45a8-adcc-d6704580a940.png)

#### 3.1.2 语义
![image.png](./assets/1659583779253-35b1c7a0-091d-4a6e-94e8-d95b24baa2c5.png)
所有变量的值在 program state 中记录。<br />因此，计算`aexp`的值的函数就可以这样写：
![image.png](./assets/1659604551752-de0467ce-cec3-4b29-a2fa-6da0c2f042c6.png)
例如：
![image.png](./assets/1659604564394-297d3b06-ae09-49bb-a244-726d7bea28f5.png)
但是，state 一般不会只有这么简单。我们需要引入 generic function update notation：
![image.png](./assets/1659604619566-7e685653-3502-4dc8-b6a2-de18d8df9794.png)
例如，下式中：
![image.png](./assets/1659604643332-127e3be2-c0cc-472a-b3db-02f940cd1670.png)
`(λx. 0)`是`f`，`("x" := 7)`是`(a := b)`。这个式子表示了这样的映射关系：如果`vname`是`"x"`，则结果为`7`，否则适用`(λx. 0)`，即结果为`0`。<br />下式的意义也就明显了：
![image.png](./assets/1659604766898-db4881bd-f355-4ba7-bcb8-0f3c3edea418.png)
我们将这个式子简写为：
![image.png](./assets/1659604790643-39d29394-42b4-4687-987d-c61d38dac506.png)
`<>`是`(λx. 0)`的语法糖。


#### 3.1.3 常量折叠
![image.png](./assets/1659622944913-642999f3-df02-451a-909d-63bb5b502281.png)
![image.png](./assets/1659622967554-dfdccb28-e0ae-4a18-91e9-e8bf25ccd4e8.png)
