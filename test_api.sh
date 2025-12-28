#!/bin/bash

# API Test Script for Reharmonizer Backend
# Tests all API endpoints with example requests

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# API Base URL
API_BASE=${API_BASE:-"http://localhost:8000/api/v1"}

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Helper function to print section headers
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

# Helper function to test an endpoint
test_endpoint() {
    local method=$1
    local endpoint=$2
    local description=$3
    local expected_status=${4:-200}
    local data=$5

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    echo -e "${YELLOW}TEST ${TOTAL_TESTS}:${NC} ${description}"
    echo -e "  Method: ${method}"
    echo -e "  Endpoint: ${endpoint}"

    if [ "$method" = "GET" ]; then
        response=$(curl -s -L -w "\n%{http_code}" "${API_BASE}${endpoint}")
    elif [ "$method" = "POST" ]; then
        response=$(curl -s -L -w "\n%{http_code}" -X POST \
            -H "Content-Type: application/json" \
            -d "${data}" \
            "${API_BASE}${endpoint}")
    fi

    # Extract status code (last line)
    status_code=$(echo "$response" | tail -n 1)
    # Extract body (all but last line) - macOS compatible
    body=$(echo "$response" | sed '$d')

    if [ "$status_code" -eq "$expected_status" ]; then
        echo -e "  ${GREEN}✓ PASSED${NC} (Status: ${status_code})"
        PASSED_TESTS=$((PASSED_TESTS + 1))

        # Pretty print JSON response (first 500 chars)
        if [ ! -z "$body" ]; then
            echo "$body" | python3 -m json.tool 2>/dev/null | head -n 15 || echo "$body" | head -c 500
        fi
    else
        echo -e "  ${RED}✗ FAILED${NC} (Expected: ${expected_status}, Got: ${status_code})"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        echo "  Response: $body"
    fi
    echo ""
}

# Start testing
print_header "REHARMONIZER API TESTS"

echo "Testing API at: ${API_BASE}"
echo "Date: $(date)"
echo ""

# Check if backend is running
echo -e "${YELLOW}Checking if backend is accessible...${NC}"
if curl -s --connect-timeout 5 "${API_BASE%/api/v1}/docs" > /dev/null; then
    echo -e "${GREEN}✓ Backend is running${NC}\n"
else
    echo -e "${RED}✗ Backend is not accessible at ${API_BASE%/api/v1}${NC}"
    echo -e "${RED}Please start the backend with: docker-compose up backend${NC}\n"
    exit 1
fi

# ========================================
# CHORD ENDPOINTS
# ========================================
print_header "1. CHORD ENDPOINTS"

test_endpoint "GET" "/chords/" \
    "Get all chords" \
    200

test_endpoint "GET" "/chords/?skip=0&limit=5" \
    "Get first 5 chords with pagination" \
    200

test_endpoint "GET" "/chords/?skip=5&limit=3" \
    "Get chords with offset" \
    200

# ========================================
# KEY SIGNATURE ENDPOINTS
# ========================================
print_header "2. KEY SIGNATURE ENDPOINTS"

test_endpoint "GET" "/keys/" \
    "Get all key signatures" \
    200

test_endpoint "GET" "/keys/?mode=major" \
    "Get major key signatures" \
    200

test_endpoint "GET" "/keys/?mode=minor" \
    "Get minor key signatures" \
    200

# Note: This endpoint might not exist - testing it
test_endpoint "GET" "/keys/C%20major/chords/" \
    "Get chords for C major key" \
    200

test_endpoint "GET" "/keys/A%20minor/chords/" \
    "Get chords for A minor key" \
    200

# ========================================
# REHARMONIZATION ENDPOINTS
# ========================================
print_header "3. REHARMONIZATION ENDPOINTS"

test_endpoint "GET" "/reharmonize/substitutions/C?technique=random" \
    "Get random substitutions for C chord" \
    200

test_endpoint "GET" "/reharmonize/substitutions/Dm?technique=tritone" \
    "Get tritone substitutions for Dm chord" \
    200

test_endpoint "GET" "/reharmonize/substitutions/G7?technique=diatonic" \
    "Get diatonic substitutions for G7 chord" \
    200

test_endpoint "GET" "/reharmonize/substitutions/Am?technique=chromatic" \
    "Get chromatic substitutions for Am chord" \
    200

test_endpoint "GET" "/reharmonize/substitutions/F?technique=circle-of-fifths" \
    "Get circle-of-fifths substitutions for F chord" \
    200

# Test with context (if implemented)
test_endpoint "POST" "/reharmonize/substitutions/analyze/" \
    "Get context-aware substitutions" \
    200 \
    '{"chord": "C", "context": {"key": "C major", "position": "tonic"}}'

# ========================================
# IMPROVISATION ENDPOINTS
# ========================================
print_header "4. IMPROVISATION ENDPOINTS"

test_endpoint "GET" "/improvisation/notes/C?count=5" \
    "Get 5 improvisation notes for C chord" \
    200

test_endpoint "GET" "/improvisation/notes/Dm7?count=7" \
    "Get 7 improvisation notes for Dm7 chord" \
    200

test_endpoint "GET" "/improvisation/notes/G7?count=3" \
    "Get 3 improvisation notes for G7 chord" \
    200

test_endpoint "GET" "/improvisation/notes/Cmaj7" \
    "Get default improvisation notes for Cmaj7 chord" \
    200

# ========================================
# ERROR HANDLING TESTS
# ========================================
print_header "5. ERROR HANDLING TESTS"

test_endpoint "GET" "/chords/nonexistent/" \
    "Get non-existent chord" \
    404

test_endpoint "GET" "/reharmonize/substitutions/InvalidChord123" \
    "Get substitutions for invalid chord (should still work)" \
    200

test_endpoint "GET" "/keys/InvalidKey/chords/" \
    "Get chords for invalid key" \
    404

# ========================================
# EDGE CASES
# ========================================
print_header "6. EDGE CASES"

test_endpoint "GET" "/chords/?skip=1000&limit=10" \
    "Pagination beyond available data" \
    200

test_endpoint "GET" "/improvisation/notes/C?count=100" \
    "Request many improvisation notes" \
    200

test_endpoint "GET" "/reharmonize/substitutions/C?technique=invalid_technique" \
    "Invalid substitution technique (should default to random)" \
    200

# ========================================
# SUMMARY
# ========================================
print_header "TEST SUMMARY"

echo "Total Tests:  ${TOTAL_TESTS}"
echo -e "Passed:       ${GREEN}${PASSED_TESTS}${NC}"
echo -e "Failed:       ${RED}${FAILED_TESTS}${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "\n${GREEN}All tests passed! ✓${NC}\n"
    exit 0
else
    echo -e "\n${RED}Some tests failed! ✗${NC}\n"
    exit 1
fi
