set(src_files MCNPInput.cpp geometry.cpp)
add_executable(csg2csg csg2csg.cpp ${src_files})
target_link_libraries(csg2csg stdc++)

install(TARGETS csg2csg 
        RUNTIME DESTINATION bin)
