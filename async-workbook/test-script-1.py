# Asyncio is single threaded and runs on a single process .. its uses co-operative multitasking , where task voluntarily gives-up control. 
# For CPU bound task that need heavy computation you would want to use processes instead

# main-fn is async ... we cant call it directly .. inorder to start the main-fn we've to start the event loop. .. asyncio.run( main-fn() )

# Event loop is basically the engine that runs and manages async fns  .... think of it as a scheduler ... it keep track of all the tasks and when a task is suspended 
# because its waiting for something else .. control returns to the event loop .. it then find another task to start or resume. 




# Awaitables are objects the implement a special __await__ method under the hood
# Sync libs dont have a mechanism to work with the event loop .. they don't know how to yeild control over and resume later

# when you await something you are telling the event loop to pause the execution of the current function
# and yeild control back to the event loop -- which can then run another task   
#
# In python asyncio -- there are 3 types of awaitables
# 1. Coroutines which are created when you call an async function
# 2. Tasks -- wrapper around coroutines
# 3. 


import asyncio
import time
import argparse


def sync_fn(param:str):
    print("SYNC FN STARTED")
    time.sleep(1)
    print("SYNC FN ENDED")


async def main(param:str):
    print("-- Main fn --")
    print("Calling sync fn")
    sync_fn(param=param)
    print("Main fn done")



if __name__ == "__main__":

    args = argparse.ArgumentParser(prog='asyncio 101', description="study asyncio by coding")
    args.add_argument( '-p','--param', default='hello', help="dummy parameter", type=str)

    params = args.parse_args()

    if params.param:
        asyncio.run(main=main(param=params.param))
    else:
        raise ValueError('Give the required input arguments')
    


# ---

# ## ✅ Is Your Code Correct?
# ``` asyncio.run(main=main(param=params.param)) ```
# You're mostly correct, but there's a small issue in this line:

# ```python
# asyncio.run(main=main(param=params.param))
# ```

# It should be:

# ```python
# asyncio.run(main(params.param))
# ```

# The `main` function is being passed as a keyword argument, which is not valid syntax for `asyncio.run`.

# ---

# ## 🧠 Best Practices for Using `argparse`

# Here are some solid guidelines to follow:

# ### 1. **Place Argument Parsing at the Top of `__main__` Block**
# Yes, it's good to keep `argparse` inside the `if __name__ == "__main__":` block. This ensures it's only executed when the script is run directly.

# ### 2. **Use Clear and Descriptive Argument Names**
# Avoid cryptic flags. For example, `--param` is okay, but if it's meant to be a message, consider `--message`.

# ### 3. **Always Provide Help Messages**
# This makes your CLI self-documenting.

# ```python
# parser.add_argument('--message', '-m', help='Message to be processed', type=str, default='hello')
# ```

# ### 4. **Set Sensible Defaults**
# Defaults make your script usable without requiring all arguments.

# ### 5. **Validate Inputs**
# Use `type=`, `choices=`, or custom validation logic to ensure inputs are correct.

# ### 6. **Group Related Arguments**
# Use `parser.add_argument_group()` to organize arguments logically.

# ### 7. **Use Subparsers for Multiple Commands**
# If your script supports multiple modes (e.g., `run`, `test`, `debug`), use `add_subparsers()`.

# ---

# ## 🔍 Important Parameters of `ArgumentParser`

# | Parameter         | Description                                                                 |
# |------------------|-----------------------------------------------------------------------------|
# | `prog`           | Name of the program (shown in help text)                                   |
# | `description`    | Description of the program                                                  |
# | `epilog`         | Text shown after help                                                       |
# | `add_help`       | Whether to add `-h/--help` automatically (default: True)                    |
# | `formatter_class`| Customize help formatting (e.g., `argparse.RawTextHelpFormatter`)           |

# For `add_argument()`:

# | Parameter     | Description                                                                 |
# |---------------|-----------------------------------------------------------------------------|
# | `name/flags`  | Argument name(s), e.g., `--verbose`, `-v`                                   |
# | `type`        | Type of the argument (e.g., `int`, `str`)                                   |
# | `default`     | Default value if not provided                                               |
# | `help`        | Help text shown in `--help`                                                 |
# | `required`    | Whether the argument is mandatory                                           |
# | `choices`     | Restrict input to a set of values                                           |
# | `action`      | Special behavior (e.g., `store_true`, `append`)                            |

# ---

# ## 🧪 Example: Clean and Effective Usage

# ```python
# import argparse
# import asyncio

# def sync_fn(param: str):
#     print(f"Sync received: {param}")

# async def main(param: str):
#     print(f"Async received: {param}")
#     await asyncio.sleep(1)
#     print("Done")

# def parse_args():
#     parser = argparse.ArgumentParser(
#         prog='asyncio 101',
#         description='Study asyncio by coding',
#         epilog='Enjoy learning Python async!'
#     )
#     parser.add_argument(
#         '-p', '--param',
#         type=str,
#         default='hello',
#         help='Dummy parameter to pass to async function'
#     )
#     return parser.parse_args()

# if __name__ == "__main__":
#     args = parse_args()
#     asyncio.run(main(args.param))
# ```

# ---

# ## 🧭 Bonus Tips

# - Use `argparse.RawTextHelpFormatter` if your help text needs formatting.
# - Use `nargs='*'` or `'+'` for variable-length arguments.
# - Use `metavar` to customize argument name in help output.

# ---
