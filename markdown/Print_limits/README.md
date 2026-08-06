                              __         ___                       __             
                   __        /\ \__     /\_ \   __              __/\ \__          
     _____   _ __ /\_\    ___\ \ ,_\    \//\ \ /\_\    ___ ___ /\_\ \ ,_\   ____  
    /\ '__`\/\`'__\/\ \ /' _ `\ \ \/      \ \ \\/\ \ /' __` __`\/\ \ \ \/  /',__\ 
    \ \ \L\ \ \ \/ \ \ \/\ \/\ \ \ \_      \_\ \\ \ \/\ \/\ \/\ \ \ \ \ \_/\__, `\
     \ \ ,__/\ \_\  \ \_\ \_\ \_\ \__\     /\____\ \_\ \_\ \_\ \_\ \_\ \__\/\____/
      \ \ \/  \/_/   \/_/\/_/\/_/\/__/     \/____/\/_/\/_/\/_/\/_/\/_/\/__/\/___/ 
       \ \_\                                                          by yavi337     
        \/_/                                                                   
# print_limits

## About

`print_limits` is a C program designed to display the maximum and minimum values of various data types. It provides a user-friendly interface for selecting data types and viewing their corresponding limits.

## Features

- **Interactive Mode:** Allows users to choose data types from a list.
- **Command-Line Arguments:** Supports directly specifying data type names for quick access.
- **Colored Output:** Enhances readability with visually distinct text.
- **Help Message:** Provides guidance on usage and available options.
- **Error Handling:** Gracefully handles invalid inputs.

## Installation

### Clone the Repository
```bash
git clone https://github.com/haddoumounir/Print_limits.git
```

### Compile
```bash
cd print_limits
gcc -o print_limits print_limits.c libraries/libraries.h
```

## Usage:

### Interactive Mode:
Run the executable:
```bash
./print_limits
```
Follow the on-screen prompts to select a data type.

### Command-Line Arguments:
Run the executable with the desired data type name as an argument:
```bash
./print_limits <data_type>
```
Available data types: `CHAR_BIT`, `SCHAR_MIN`, `SCHAR_MAX`, `UCHAR_MAX`, `SHRT_MIN`, `SHRT_MAX`, `MB_LEN_MAX`, `USHRT_MAX`, `INT_MAX`, `INT_MIN`, `UINT_MAX`, `LONG_MIN`, `LONG_MAX`, `ULONG_MAX`, `LLONG_MIN`, `LLONG_MAX`, `ULLONG_MAX`

### Example:
To view the maximum value of `INT_MAX`, run:
```bash
./print_limits INT_MAX
```

## Project Structure:

```
.
├── libraries
│   └── libraries.h
├── print_limits.c
├── prli_files
│   ├── help.prli
│   ├── intro.prli
│   └── list_of_text.prli
└── src
    └── ft_strcmp.c
```

- **libraries:** Contains header files for functions or constants used in the project.
- **print_limits.c:** The main program file.
- **prli_files:** Stores text files for displaying information.
- **src:** Contains source code for specific functions or modules.
