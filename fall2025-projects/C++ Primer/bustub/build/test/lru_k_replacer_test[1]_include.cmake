if(EXISTS "/mnt/c/Users/zeyu6/Desktop/Database/Projects/C++ Primer/bustub/build/test/lru_k_replacer_test")
  if(NOT EXISTS "/mnt/c/Users/zeyu6/Desktop/Database/Projects/C++ Primer/bustub/build/test/lru_k_replacer_test[1]_tests.cmake" OR
     NOT "/mnt/c/Users/zeyu6/Desktop/Database/Projects/C++ Primer/bustub/build/test/lru_k_replacer_test[1]_tests.cmake" IS_NEWER_THAN "/mnt/c/Users/zeyu6/Desktop/Database/Projects/C++ Primer/bustub/build/test/lru_k_replacer_test" OR
     NOT "/mnt/c/Users/zeyu6/Desktop/Database/Projects/C++ Primer/bustub/build/test/lru_k_replacer_test[1]_tests.cmake" IS_NEWER_THAN "${CMAKE_CURRENT_LIST_FILE}")
    include("/usr/share/cmake-3.28/Modules/GoogleTestAddTests.cmake")
    gtest_discover_tests_impl(
      TEST_EXECUTABLE [==[/mnt/c/Users/zeyu6/Desktop/Database/Projects/C++ Primer/bustub/build/test/lru_k_replacer_test]==]
      TEST_EXECUTOR [==[]==]
      TEST_WORKING_DIR [==[/mnt/c/Users/zeyu6/Desktop/Database/Projects/C++ Primer/bustub/build/test]==]
      TEST_EXTRA_ARGS [==[--gtest_output=xml:/mnt/c/Users/zeyu6/Desktop/Database/Projects/C++ Primer/bustub/build/test/lru_k_replacer_test.xml;--gtest_catch_exceptions=0]==]
      TEST_PROPERTIES [==[TIMEOUT;120]==]
      TEST_PREFIX [==[]==]
      TEST_SUFFIX [==[]==]
      TEST_FILTER [==[]==]
      NO_PRETTY_TYPES [==[FALSE]==]
      NO_PRETTY_VALUES [==[FALSE]==]
      TEST_LIST [==[lru_k_replacer_test_TESTS]==]
      CTEST_FILE [==[/mnt/c/Users/zeyu6/Desktop/Database/Projects/C++ Primer/bustub/build/test/lru_k_replacer_test[1]_tests.cmake]==]
      TEST_DISCOVERY_TIMEOUT [==[120]==]
      TEST_XML_OUTPUT_DIR [==[]==]
    )
  endif()
  include("/mnt/c/Users/zeyu6/Desktop/Database/Projects/C++ Primer/bustub/build/test/lru_k_replacer_test[1]_tests.cmake")
else()
  add_test(lru_k_replacer_test_NOT_BUILT lru_k_replacer_test_NOT_BUILT)
endif()
