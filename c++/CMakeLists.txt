cmake_minimum_required(VERSION 3.28)
project(proyecto_compiladores)

set(CMAKE_CXX_STANDARD 17)

add_executable(proyecto_compiladores 
    main.cpp 
    lexer.cpp 
    parser.cpp 
    generator.cpp 
    utils.cpp
)
