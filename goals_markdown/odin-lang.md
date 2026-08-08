# Odin Programming Language Exploration

A personal exploration into the Odin programming language, manual memory management architectures, and building modern systems software without object-oriented overhead.

---

## 1. Why Odin?

Odin is a modern, general-purpose systems programming language designed with data-oriented programming, explicit memory allocation, and zero hidden control flow at its core.

### Core Philosophy:
* **Simplicity over Complexity:** Clear syntax avoiding the hidden traps of C++ OOP hierarchies.
* **Context System:** Custom allocators (Arena, Pool, Stack) passed seamlessly via implicit context.
* **Type Safety with Low-Level Control:** Strict typing with direct access to memory layouts, pointer arithmetic, and bit-level representations.

---

## 2. Key Language Concepts Under Exploration

1. **Custom Memory Allocators:**
   * Eliminating heap fragmentation through custom Arena and Temp memory allocators.
   * Region-based memory lifecycles for high-performance utilities.
2. **Data-Oriented Design (DOD):**
   * Struct of Arrays (SoA) vs Array of Structs (AoS) optimizations for L1/L2 CPU cache utilization.
   * Explicit SIMD vector intrinsics.
3. **Cross-Platform Low-Level Tools:**
   * Writing lightweight Unix CLI utilities and binary file inspectors.

---

## 3. Project Milestones

* [x] Basic syntax, packages, and procedure typing.
* [ ] Implementing a custom arena allocator from scratch.
* [ ] Building a binary ELF/Mach-O inspector CLI tool in pure Odin.
* [ ] Benchmarking Odin performance vs pure C in cache-heavy operations.
