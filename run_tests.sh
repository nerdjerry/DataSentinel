#!/bin/bash
# Run all tests in the DataSentinel project

echo "=================================="
echo "DataSentinel Test Runner"
echo "=================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to run a test
run_test() {
    local test_file=$1
    local test_name=$(basename "$test_file" .py)
    
    echo "----------------------------------------"
    echo "Running: $test_name"
    echo "----------------------------------------"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if python3 "$test_file"; then
        echo -e "${GREEN}✓ $test_name PASSED${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}✗ $test_name FAILED${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    echo ""
}

echo "Running Agent Tests..."
echo "=================================="
run_test "tests/agent/DataAgent_test.py"
run_test "tests/agent/DataProfilingAgent_test.py"
run_test "tests/agent/DataQualityAgent_test.py"

echo ""
echo "Running Tool Tests..."
echo "=================================="
run_test "tests/tool/SnowflakeQueryEngine_test.py"
run_test "tests/tool/SnowflakeDataProfilingTool_test.py"

echo ""
echo "=================================="
echo "Test Summary"
echo "=================================="
echo "Total Tests:  $TOTAL_TESTS"
echo -e "${GREEN}Passed:       $PASSED_TESTS${NC}"
if [ $FAILED_TESTS -gt 0 ]; then
    echo -e "${RED}Failed:       $FAILED_TESTS${NC}"
else
    echo "Failed:       $FAILED_TESTS"
fi
echo "=================================="

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}All tests passed! ✓${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed! ✗${NC}"
    exit 1
fi
