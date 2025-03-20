#!/usr/bin/env python3
"""
Main test runner for ComputerQuest tests
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_all_tests():
    """Run all unit tests"""
    # Find all test files
    loader = unittest.TestLoader()
    test_suite = loader.discover(os.path.dirname(__file__), pattern="test_*.py")
    
    # Create test runner
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run tests
    print("=" * 70)
    print("Running KodeKloud Computer Quest Unit Tests")
    print("=" * 70)
    
    result = runner.run(test_suite)
    
    print("\n" + "=" * 70)
    print(f"Test Results: {result.testsRun} tests run, {len(result.errors)} errors, {len(result.failures)} failures")
    print("=" * 70)
    
    # Return exit code based on test success
    return 0 if result.wasSuccessful() else 1

def run_specific_test(test_name):
    """Run a specific test module"""
    if not test_name.startswith('test_'):
        test_name = f'test_{test_name}'
    
    if not test_name.endswith('.py'):
        test_name = f'{test_name}.py'
    
    test_path = os.path.join(os.path.dirname(__file__), test_name)
    
    if not os.path.exists(test_path):
        print(f"Error: Test file {test_path} does not exist")
        return 1
    
    # Load and run specific test
    module_name = os.path.splitext(test_name)[0]
    loader = unittest.TestLoader()
    
    try:
        # Import the module dynamically
        test_module = __import__(f'tests.{module_name}', fromlist=[''])
        test_suite = loader.loadTestsFromModule(test_module)
        
        # Run tests
        print("=" * 70)
        print(f"Running tests from {module_name}")
        print("=" * 70)
        
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(test_suite)
        
        print("\n" + "=" * 70)
        print(f"Test Results: {result.testsRun} tests run, {len(result.errors)} errors, {len(result.failures)} failures")
        print("=" * 70)
        
        return 0 if result.wasSuccessful() else 1
        
    except ImportError as e:
        print(f"Error importing test module {module_name}: {e}")
        return 1

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test module
        test_name = sys.argv[1]
        exit_code = run_specific_test(test_name)
    else:
        # Run all tests
        exit_code = run_all_tests()
    
    sys.exit(exit_code)