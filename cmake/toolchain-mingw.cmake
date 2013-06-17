# the name of the target operating system
SET(CMAKE_SYSTEM_NAME Windows)

set(COMPILER_PREFIX "x86_64-w64-mingw32")

# here is the target environment located
SET(USER_ROOT_PATH /home/cap/win)
SET(CMAKE_FIND_ROOT_PATH ${USER_ROOT_PATH}/${COMPILER_PREFIX} ${USER_ROOT_PATH})

# which compilers to use for C and C++
find_program(CMAKE_RC_COMPILER NAMES ${COMPILER_PREFIX}-windres)
find_program(CMAKE_C_COMPILER NAMES ${COMPILER_PREFIX}-gcc)
find_program(CMAKE_CXX_COMPILER NAMES ${COMPILER_PREFIX}-g++)

# adjust the default behaviour of the FIND_XXX() commands:
# search headers and libraries in the target environment, search
# programs in the host environment
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
