# 🖥️ myGo Compiler – Compiler for a Subset of Go Language

This project was developed during my third year in my university **Compilers** course. It implements a compiler for **myGo**, a subset of the Go programming language, supporting variables, functions, expressions, control structures, and input/output operations. The compiler performs **lexical, syntactic, and semantic analysis**, and generates **LLVM IR code**.

---

## 🚀 Features

- 🔹 **Lexical Analysis:**  
  Recognizes identifiers, literals (int, float32, bool, string), operators, punctuation, and reserved keywords.

- 🔹 **Syntax Analysis:**  
  Constructs an abstract syntax tree (AST) using **Bison/Yacc**, detecting syntax errors with accurate line and column reporting.

- 🔹 **Semantic Analysis:**  
  Builds symbol tables, annotates the AST with types, checks for semantic errors (e.g., type mismatches, undefined symbols).

- 🔹 **Code Generation:**  
  Produces LLVM IR code executable with `lli` or compilable to native code with `llc` + `gcc`.

- 🔹 **Error Handling:**  
  Reports lexical, syntax, and semantic errors with precise messages and recovers gracefully when possible.

- 🔹 **Options:**  
  - `-l` → Lexical analysis only, prints tokens.  
  - `-t` → Syntax analysis only, prints AST.  
  - `-s` → Semantic analysis only, prints symbol tables and annotated AST.

---

## 🛠️ Compiler Workflow

1. **Lexer** → Scans source code, generates tokens.  
2. **Parser** → Builds AST from tokens, checks syntax.  
3. **Semantic Analyzer** → Constructs symbol tables, annotates AST, detects type and scope errors.  
4. **LLVM IR Generator** → Emits LLVM intermediate code when no errors are detected.  

---

## ⚡ Technologies Used

- **C Language** → Core compiler implementation  
- **Flex/Lex** → Lexical analysis  
- **Bison/Yacc** → Syntax parsing  
- **LLVM IR** → Intermediate representation and code generation  

---

## 🕹️ How to Build and Run

1. **Build the compiler:**  
    ```bash
    make all
    ```

2. **Run lexical analysis only:**  
    ```bash
    ./go_compiler -l < program.dgo
    ```

3. **Run syntax analysis and print AST:**  
    ```bash
    ./go_compiler -t < program.dgo
    ```

4. **Run semantic analysis and print tables/annotated AST:**  
    ```bash
    ./go_compiler -s < program.dgo
    ```

5. **Generate LLVM IR code:**  
    ```bash
    ./go_compiler < program.dgo > program.ll
    lli program.ll
    ```
