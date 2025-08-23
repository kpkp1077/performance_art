#!/usr/bin/env pypy3
"""
Startup script with PyPy optimizations for QuotaPath
"""

import os
import sys
import django


def detect_pypy():
    """Detect if running on PyPy and print version info"""
    if hasattr(sys, 'pypy_version_info'):
        print(f"🚀 Detected PyPy {sys.pypy_version_info.major}.{sys.pypy_version_info.minor}.{sys.pypy_version_info.micro}")
        return True
    else:
        print("📍 Running on CPython", sys.version_info)
        return False


def apply_pypy_optimizations():
    """Apply PyPy-specific optimizations"""
    if not hasattr(sys, 'pypy_version_info'):
        return
    
    print("🔧 Applying PyPy optimizations...")
    
    # Set PyPy-specific environment variables if not already set
    pypy_env_vars = {
        'PYPY_GC_MAX_DELTA': '200MB',
        'PYPY_GC_MAJOR_COLLECT': '1.82',
        'PYPY_GC_GROWTH': '1.82',
    }
    
    for var, value in pypy_env_vars.items():
        if not os.environ.get(var):
            os.environ[var] = value
            print(f"  ✓ Set {var}={value}")
    
    # Configure garbage collection
    import gc
    try:
        gc.set_threshold(700, 10, 10)
        print("  ✓ Configured garbage collection thresholds")
    except AttributeError:
        print("  ⚠ Could not configure GC thresholds (PyPy version may not support it)")
    
    # Import and configure pandas optimizations
    try:
        from commissions.pypy_optimizations import optimize_pandas_for_pypy
        optimize_pandas_for_pypy()
        print("  ✓ Applied pandas optimizations for PyPy")
    except ImportError:
        print("  ⚠ Could not import PyPy optimizations")


def setup_django():
    """Setup Django with PyPy-optimized settings if available"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotapath.settings')
    
    # Use PyPy-optimized settings if running on PyPy
    if hasattr(sys, 'pypy_version_info'):
        try:
            import quotapath.settings_pypy
            os.environ['DJANGO_SETTINGS_MODULE'] = 'quotapath.settings_pypy'
            print("  ✓ Using PyPy-optimized Django settings")
        except ImportError:
            print("  ⚠ PyPy-optimized settings not found, using default")
    
    django.setup()


def main():
    """Main startup function"""
    print("🎯 Starting QuotaPath with PyPy optimizations...")
    
    # Detect PyPy
    is_pypy = detect_pypy()
    
    # Apply optimizations
    if is_pypy:
        apply_pypy_optimizations()
    
    # Setup Django
    setup_django()
    
    print("✅ Startup complete!")


if __name__ == "__main__":
    main()