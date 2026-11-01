import sys
import time
import subprocess
import tempfile
import os


def execute_python_code(code_string, test_cases, timeout_seconds=4):
    """
    Executes Python solution against given test cases.
    Each test case is a dict: {'input': str, 'expected': str, 'is_hidden': bool}
    Returns:
        {
            'status': 'Accepted' | 'Wrong Answer' | 'Runtime Error' | 'Time Limit Exceeded',
            'passed': int,
            'total': int,
            'execution_time_ms': float,
            'details': list of dicts,
            'error': str or None
        }
    """
    total = len(test_cases)
    if total == 0:
        return {
            'status': 'Accepted',
            'passed': 0,
            'total': 0,
            'execution_time_ms': 0.0,
            'details': [],
            'error': None
        }

    results = []
    passed = 0
    total_time = 0.0

    # Write candidate code to temporary file
    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False, encoding='utf-8') as f:
        temp_path = f.name
        f.write(code_string)

    try:
        for idx, tc in enumerate(test_cases):
            tc_input = tc.get('input', '')
            tc_expected = tc.get('expected', '').strip()
            is_hidden = tc.get('is_hidden', False)

            start = time.perf_counter()
            try:
                proc = subprocess.run(
                    [sys.executable, temp_path],
                    input=tc_input,
                    text=True,
                    capture_output=True,
                    timeout=timeout_seconds
                )
                elapsed_ms = (time.perf_counter() - start) * 1000.0
                total_time += elapsed_ms

                actual_out = proc.stdout.strip()
                err_out = proc.stderr.strip()

                if proc.returncode != 0:
                    results.append({
                        'test_case': idx + 1,
                        'passed': False,
                        'is_hidden': is_hidden,
                        'error': err_out or 'Runtime error occurred',
                        'expected': 'Hidden' if is_hidden else tc_expected,
                        'actual': 'Error'
                    })
                    return {
                        'status': 'Runtime Error',
                        'passed': passed,
                        'total': total,
                        'execution_time_ms': round(total_time, 2),
                        'details': results,
                        'error': err_out
                    }

                # Compare output
                # Normalize line breaks and trailing spaces
                norm_actual = '\n'.join([line.strip() for line in actual_out.splitlines()])
                norm_expected = '\n'.join([line.strip() for line in tc_expected.splitlines()])

                is_pass = (norm_actual == norm_expected)
                if is_pass:
                    passed += 1

                results.append({
                    'test_case': idx + 1,
                    'passed': is_pass,
                    'is_hidden': is_hidden,
                    'input': 'Hidden' if is_hidden else tc_input,
                    'expected': 'Hidden' if is_hidden else tc_expected,
                    'actual': 'Hidden' if is_hidden else actual_out,
                    'execution_time_ms': round(elapsed_ms, 2)
                })

            except subprocess.TimeoutExpired:
                results.append({
                    'test_case': idx + 1,
                    'passed': False,
                    'is_hidden': is_hidden,
                    'error': f'Execution timed out after {timeout_seconds}s'
                })
                return {
                    'status': 'Time Limit Exceeded',
                    'passed': passed,
                    'total': total,
                    'execution_time_ms': round(timeout_seconds * 1000.0, 2),
                    'details': results,
                    'error': f'Time limit of {timeout_seconds} seconds exceeded'
                }

    finally:
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception:
            pass

    status = 'Accepted' if passed == total else 'Wrong Answer'
    return {
        'status': status,
        'passed': passed,
        'total': total,
        'execution_time_ms': round(total_time / max(total, 1), 2),
        'details': results,
        'error': None if passed == total else 'Some test cases failed.'
    }
