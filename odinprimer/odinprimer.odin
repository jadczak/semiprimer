package main

import "core:fmt"
import "core:math/big"
import "core:os"
import "core:strings"
import "core:container/queue"

Node :: struct {
    level: int,
    a: big.Int,
    b: big.Int,
}

// TODO: Most of this code is error handling code.
// Figure out a way to make the code more compact.
// Wrap all the procedures in a helper to do the
// error handling?

main :: proc() {
    // Get the semiprime to be factored from the user
    buf: [2048]byte
    fmt.print("Enter Semiprime: ")
    n, read_err := os.read(os.stdin, buf[:])
    if read_err != nil {
        fmt.eprintfln("%v:%v %v", #file, #line, read_err)
        return
    }
    raw_semi := string(buf[:n])

    // test data
    // raw_semi := "17549235333121"
    // raw_semi := "41758540882408627201"  // ~8.5 minutes to factor
    semistring := strings.trim_space(raw_semi)
    semiprime := big.Int{}
    defer big.destroy(&semiprime)
    int_err := big.set(&semiprime, semistring)
    if int_err != nil {
        fmt.eprintfln("%v:%v %v", #file, #line, int_err)
        return
    }

    // Setup the lookups for use when sub_factorings
    semiprime_length := len(semistring)
    lookup : [dynamic]big.Int
    defer delete(lookup)
    scale : [dynamic]big.Int
    defer delete(scale)
    for i in 0..=semiprime_length {
        append(&lookup, big.Int{})
        int_err := big.set(&lookup[i], semistring[semiprime_length-i:semiprime_length])
        if int_err != nil {
            fmt.eprintfln("%v:%v %v", #file, #line, int_err)
            return
        }
        append(&scale, big.Int{})
        int_err = big.pow(&scale[i], 10, i)
        if int_err != nil {
            fmt.eprintfln("%v:%v %v", #file, #line, int_err)
            return
        }
    }

    // 0-9 are used repeatedly, keep these around.
    digits : [10]big.DIGIT
    for i in 0..=9 {
        digits[i] = big.DIGIT(i)
        if int_err != nil {
            fmt.eprintfln("%v:%v %v", #file, #line, int_err)
            return
        }
    }

    // prime the node list
    nodes      :  [dynamic]Node         // stack of nodes to process
    temp       :  [dynamic]big.Int      // scratch storage for sub_factor
    first      := Node{}
    big_err    := big.zero(&first.a)
    if int_err != nil {
        fmt.eprintfln("%v:%v %v", #file, #line, int_err)
        return
    }
    big_err     = big.zero(&first.b)
    if int_err != nil {
        fmt.eprintfln("%v:%v %v", #file, #line, int_err)
        return
    }
    first.level = 1
    append(&nodes, first)
    done : bool = false
    counter := 0
    for !done {
        done = sub_factor(&nodes, &lookup, &scale, &temp, digits, &semiprime)
        idx := len(temp)
        // counter += 1
        // if (counter % 10000) == 0 {
        //     fmt.println(counter)
        // }
        // TODO: try to find a telemetry program.
        // how much time is wasted on the destroy calls?
        // how much time is wasted on the error handling?
        for i in 0..<idx {
            trash := pop(&temp)
            big.destroy(&trash)
        }
    }
    return
    
}


sub_factor :: proc(nodes: ^[dynamic]Node, lookup, scale, temp : ^[dynamic]big.Int, digits: [10]big.DIGIT, semiprime : ^big.Int) -> bool {
    node := pop(nodes)
    defer free(&node)
    defer big.destroy(&node.a)
    defer big.destroy(&node.b)
    defer free(&node.level)
    if node.level >= len(scale) {
        return false
    }
    current_a, current_b, current_product, current_mod: big.Int
    defer big.destroy(&current_a)
    defer big.destroy(&current_b)
    defer big.destroy(&current_product)
    defer big.destroy(&current_mod)
    cond, a_is_1, b_is_1, is_semiprime : bool
    
    for a in digits {
        err :=  big.mul(&current_a, &scale[node.level-1], a)
        if err != nil {
            fmt.eprintfln("%v:%v %v", #file, #line, err)
        }
        err  = big.add(&current_a, &current_a, &node.a)
        if err != nil {
            fmt.eprintfln("%v:%v %v", #file, #line, err)
        }
        for b in digits {
            err := big.mul(&current_b, &scale[node.level-1], b)
            if err != nil {
                fmt.eprintfln("%v:%v %v", #file, #line, err)
            }
            err  = big.add(&current_b, &current_b, &node.b)
            if err != nil {
                fmt.eprintfln("%v:%v %v", #file, #line, err)
            }
            err = big.mul(&current_product, &current_a, &current_b)
            if err != nil {
                fmt.eprintfln("%v:%v %v", #file, #line, err)
            }
            cond, err = big.gt(&current_product, semiprime)
            if err != nil {
                fmt.eprintfln("%v:%v %v", #file, #line, err)
            }
            if cond {
                continue  // bail early if the product is too big.
            }
            err = big.mod(&current_mod, &current_product, &scale[node.level])
            if err != nil {
                fmt.eprintfln("%v:%v %v", #file, #line, err)
            }
            cond, err = big.eq(&current_mod, &lookup[node.level]) 
            if cond {
                cond, err = big.gt(&current_a, &current_b)
                if err != nil {
                    fmt.eprintfln("%v:%v %v", #file, #line, err)
                }
                if cond {
                    big.swap(&current_a, &current_b)
                }
                valid := true
                for &value in temp {
                    cond, err = big.eq(&value, &current_a)
                    if err != nil {
                        fmt.eprintfln("%v:%v %v", #file, #line, err)
                    }
                    if cond {
                        valid = false
                        break 
                    }
                }
                if valid {
                    idx := len(temp)
                    append(temp, big.Int{})
                    err = big.copy(&temp[idx], &current_a)
                    if err != nil {
                        fmt.eprintfln("%v:%v %v", #file, #line, err)
                    }
                    idx = len(nodes)
                    append(nodes, Node{})
                    nodes[idx].level = node.level + 1
                    nodes[idx].a = big.Int{}
                    nodes[idx].b = big.Int{}
                    err = big.copy(&nodes[idx].a, &current_a)
                    if err != nil {
                        fmt.eprintfln("%v:%v %v", #file, #line, err)
                    }
                    err = big.copy(&nodes[idx].b, &current_b)
                    if err != nil {
                        fmt.eprintfln("%v:%v %v", #file, #line, err)
                    }
                    is_semiprime, err = big.eq(&current_product, semiprime)
                    if err != nil {
                        fmt.eprintfln("%v:%v %v", #file, #line, err)
                    }
                    a_is_1, err = big.eq(&current_a, 1)
                    if err != nil {
                        fmt.eprintfln("%v:%v %v", #file, #line, err)
                    }
                    b_is_1, err = big.eq(&current_a, 1)
                    if err != nil {
                        fmt.eprintfln("%v:%v %v", #file, #line, err)
                    }
                    if is_semiprime {
                        if a_is_1 || b_is_1 {
                            trash := pop(nodes)
                            big.destroy(&trash.a)
                            big.destroy(&trash.b)
                            free(&trash.level)
                            free(&trash)
                        }
                        else
                        {
                            str_a, str_b, str_s : string
                            str_a, err = big.itoa(&current_a)
                            if err != nil {
                                fmt.eprintfln("%v:%v %v", #file, #line, err)
                            }
                            str_b, err = big.itoa(&current_b)
                            if err != nil {
                                fmt.eprintfln("%v:%v %v", #file, #line, err)
                            }
                            str_s, err = big.itoa(semiprime)
                            if err != nil {
                                fmt.eprintfln("%v:%v %v", #file, #line, err)
                            }
                            fmt.printfln("Solution found %v x %v = %v", str_a, str_b, str_s)
                            return true
                        }
                    }
                }
            }
        }
    }
    return false
}
