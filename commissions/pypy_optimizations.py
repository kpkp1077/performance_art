"""
PyPy-specific optimizations for commission calculations
"""

import sys
from decimal import Decimal
from typing import List, Dict, Any


def is_pypy():
    """Check if running on PyPy"""
    return hasattr(sys, 'pypy_version_info')


class PyPyCommissionOptimizer:
    """PyPy-optimized commission calculation helpers"""
    
    def __init__(self):
        self.calculation_cache = {}
        self._jit_warmup_done = False
    
    def warm_up_jit(self, sample_data: List[Dict[str, Any]]):
        """Warm up PyPy's JIT compiler with sample calculations"""
        if not is_pypy() or self._jit_warmup_done:
            return
        
        # Perform dummy calculations to trigger JIT compilation
        for _ in range(100):
            for data in sample_data[:10]:  # Use first 10 samples
                self._calculate_percentage_commission(
                    Decimal(str(data.get('amount', 1000))),
                    Decimal(str(data.get('rate', 5.0)))
                )
                self._calculate_tiered_commission(
                    Decimal(str(data.get('amount', 1000))),
                    [(Decimal('0'), Decimal('5000'), Decimal('5.0')),
                     (Decimal('5000'), Decimal('10000'), Decimal('7.0'))]
                )
        
        self._jit_warmup_done = True
    
    def _calculate_percentage_commission(self, amount: Decimal, rate: Decimal) -> Decimal:
        """JIT-optimized percentage commission calculation"""
        return amount * (rate / Decimal('100'))
    
    def _calculate_tiered_commission(self, amount: Decimal, tiers: List[tuple]) -> Decimal:
        """JIT-optimized tiered commission calculation"""
        commission = Decimal('0')
        remaining = amount
        
        for min_amount, max_amount, tier_rate in tiers:
            if remaining <= 0:
                break
            
            tier_amount = min(remaining, max_amount - min_amount)
            commission += tier_amount * (tier_rate / Decimal('100'))
            remaining -= tier_amount
        
        return commission
    
    def batch_calculate_commissions(self, deals_data: List[Dict[str, Any]]) -> List[Decimal]:
        """Optimized batch commission calculation for PyPy"""
        if is_pypy() and not self._jit_warmup_done:
            self.warm_up_jit(deals_data)
        
        results = []
        for deal in deals_data:
            amount = Decimal(str(deal['amount']))
            plan_type = deal['plan_type']
            
            if plan_type == 'percentage':
                rate = Decimal(str(deal['rate']))
                commission = self._calculate_percentage_commission(amount, rate)
            elif plan_type == 'tiered':
                tiers = deal.get('tiers', [])
                commission = self._calculate_tiered_commission(amount, tiers)
            elif plan_type == 'flat_rate':
                commission = Decimal(str(deal['flat_rate']))
            else:
                commission = Decimal('0')
            
            results.append(commission)
        
        return results


def optimize_pandas_for_pypy():
    """Configure pandas for better PyPy performance"""
    try:
        import pandas as pd
        
        # PyPy-specific pandas optimizations
        if is_pypy():
            # Reduce chunk size for better memory management in PyPy
            pd.options.mode.chained_assignment = None
            pd.options.compute.use_bottleneck = False  # Bottleneck can be slower on PyPy
            pd.options.compute.use_numexpr = False     # NumExpr not optimized for PyPy
            
            # Set smaller block size for memory efficiency
            pd.set_option('io.hdf.default_format', 'table')
            
    except ImportError:
        pass


def pypy_memory_optimization():
    """Apply PyPy-specific memory optimizations"""
    if not is_pypy():
        return
    
    import gc
    
    # Configure PyPy GC for better performance with large datasets
    try:
        # More frequent minor collections for better memory usage
        gc.set_threshold(700, 10, 10)
        
        # Force a collection to start clean
        gc.collect()
    except AttributeError:
        # Some PyPy versions may not support all GC settings
        pass


# Initialize optimizations when module is imported
if is_pypy():
    optimize_pandas_for_pypy()
    pypy_memory_optimization()