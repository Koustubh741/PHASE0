"""
BFSI Agent Performance Optimizer
Advanced performance optimization and monitoring for BFSI GRC agents
Enhanced with intelligent caching, real-time monitoring, and automated optimization
"""

import asyncio
import time
import logging
import gc
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import json
import pickle
from functools import wraps, lru_cache
import statistics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Optional dependency for system metrics
try:
    import psutil  # type: ignore[import-untyped, reportMissingImports]
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    psutil = None  # type: ignore[assignment]
    logger.warning("psutil not available, system metrics will be limited")

# Import with fallback
try:
    from bfsi_grc_agent import BFSIGRCAgent, BFSIMetrics, BFSIAlert
except ImportError:
    logger.warning("BFSI GRC Agent not found, using fallback")
    class BFSIGRCAgent:
        def __init__(self, agent_id, name): 
            self.agent_id = agent_id
            self.name = name
            self.metrics = None
            self.sub_agents = {}
    
    class BFSIMetrics:
        def __init__(self):
            self.total_operations = 0
            self.successful_operations = 0
            self.failed_operations = 0
            self.average_response_time = 0.0
            self.compliance_score = 0.0
            self.risk_score = 0.0
        
        def to_dict(self):
            return {
                "total_operations": self.total_operations,
                "successful_operations": self.successful_operations,
                "failed_operations": self.failed_operations,
                "average_response_time": self.average_response_time,
                "compliance_score": self.compliance_score,
                "risk_score": self.risk_score
            }
    
    class BFSIAlert:
        def __init__(self, alert_id, alert_type, severity, message, timestamp, agent_id, context):
            self.alert_id = alert_id
            self.alert_type = alert_type
            self.severity = severity
            self.message = message
            self.timestamp = timestamp
            self.agent_id = agent_id
            self.context = context

class PerformanceLevel(Enum):
    """Performance level classification"""
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    POOR = "poor"
    CRITICAL = "critical"

@dataclass
class PerformanceMetrics:
    """Enhanced performance metrics for BFSI agent optimization"""
    operation_name: str
    execution_time: float
    memory_usage: float
    cpu_usage: float
    success_rate: float
    error_count: int
    timestamp: datetime
    throughput: float = 0.0
    latency_p95: float = 0.0
    latency_p99: float = 0.0
    cache_hit_rate: float = 0.0
    concurrent_operations: int = 1
    optimization_score: float = 0.0
    bottleneck_type: Optional[str] = None
    
    def __post_init__(self):
        """Validate metrics after initialization"""
        if self.execution_time < 0:
            raise ValueError("Execution time cannot be negative")
        if self.success_rate < 0 or self.success_rate > 100:
            raise ValueError("Success rate must be between 0 and 100")
        if self.memory_usage < 0:
            raise ValueError("Memory usage cannot be negative")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with proper serialization"""
        return {
            "operation_name": self.operation_name,
            "execution_time": self.execution_time,
            "memory_usage": self.memory_usage,
            "cpu_usage": self.cpu_usage,
            "success_rate": self.success_rate,
            "error_count": self.error_count,
            "timestamp": self.timestamp.isoformat(),
            "throughput": self.throughput,
            "latency_p95": self.latency_p95,
            "latency_p99": self.latency_p99,
            "cache_hit_rate": self.cache_hit_rate,
            "concurrent_operations": self.concurrent_operations,
            "optimization_score": self.optimization_score,
            "bottleneck_type": self.bottleneck_type,
            "performance_level": self.get_performance_level().value
        }
    
    def get_performance_level(self) -> PerformanceLevel:
        """Determine performance level based on metrics"""
        if self.success_rate >= 99 and self.execution_time <= 0.5:
            return PerformanceLevel.EXCELLENT
        elif self.success_rate >= 95 and self.execution_time <= 1.0:
            return PerformanceLevel.GOOD
        elif self.success_rate >= 90 and self.execution_time <= 2.0:
            return PerformanceLevel.AVERAGE
        elif self.success_rate >= 80 and self.execution_time <= 5.0:
            return PerformanceLevel.POOR
        else:
            return PerformanceLevel.CRITICAL
    
    def calculate_optimization_score(self) -> float:
        """Calculate overall optimization score (0-100)"""
        time_score = max(0, 100 - (self.execution_time * 20))
        success_score = self.success_rate
        memory_score = max(0, 100 - (self.memory_usage / 100))  # Assuming MB
        cpu_score = max(0, 100 - (self.cpu_usage * 2))
        
        self.optimization_score = (time_score + success_score + memory_score + cpu_score) / 4
        return self.optimization_score

@dataclass
class BenchmarkConfig:
    """Configuration for performance benchmarks"""
    warmup_iterations: int = 3
    test_iterations: int = 10
    timeout_seconds: float = 30.0
    concurrent_operations: int = 5
    enable_caching: bool = True
    enable_monitoring: bool = True
    memory_threshold_mb: float = 500.0
    cpu_threshold_percent: float = 80.0

@dataclass
class OptimizationResult:
    """Result of optimization operation"""
    optimization_type: str
    success: bool
    improvement_percentage: float
    before_metrics: PerformanceMetrics
    after_metrics: PerformanceMetrics
    optimization_details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "optimization_type": self.optimization_type,
            "success": self.success,
            "improvement_percentage": self.improvement_percentage,
            "before_metrics": self.before_metrics.to_dict(),
            "after_metrics": self.after_metrics.to_dict(),
            "optimization_details": self.optimization_details,
            "timestamp": self.timestamp.isoformat()
        }

class BFSIPerformanceOptimizer:
    """Enhanced BFSI Agent Performance Optimizer with intelligent caching and monitoring"""
    
    def __init__(self, agent: BFSIGRCAgent, config: BenchmarkConfig = None):
        self.agent = agent
        self.config = config or BenchmarkConfig()
        self.performance_history: List[PerformanceMetrics] = []
        self.optimization_results: List[OptimizationResult] = []
        self.benchmark_results: Dict[str, Any] = {}
        self.cache: Dict[str, Any] = {}
        self.cache_stats: Dict[str, int] = {"hits": 0, "misses": 0}
        self.monitoring_active = False
        self.monitoring_task: Optional[asyncio.Task] = None
        self.system_metrics_history: List[Dict[str, Any]] = []
        
        # Performance tracking
        self.operation_timings: Dict[str, List[float]] = {}
        self.memory_usage_history: List[float] = []
        self.cpu_usage_history: List[float] = []
        
        # Optimization settings
        self.optimization_threshold = 0.1  # 10% improvement threshold
        self.max_cache_size = 1000
        self.cache_ttl = 3600  # 1 hour
        
        logger.info(f"BFSI Performance Optimizer initialized for agent: {agent.name}")
    
    def _get_system_metrics(self) -> Dict[str, float]:
        """Get current system metrics with fallback"""
        if not PSUTIL_AVAILABLE:
            return {"memory_mb": 0, "cpu_percent": 0, "memory_percent": 0, "system_memory_percent": 0, "system_cpu_percent": 0}
        
        try:
            process = psutil.Process()
            return {
                "memory_mb": process.memory_info().rss / 1024 / 1024,
                "cpu_percent": process.cpu_percent(),
                "memory_percent": process.memory_percent(),
                "system_memory_percent": psutil.virtual_memory().percent,
                "system_cpu_percent": psutil.cpu_percent()
            }
        except Exception as e:
            logger.warning(f"Failed to get system metrics: {e}")
            return {"memory_mb": 0, "cpu_percent": 0, "memory_percent": 0, "system_memory_percent": 0, "system_cpu_percent": 0}
    
    def _measure_operation(self, operation_name: str, func: Callable, *args, **kwargs) -> PerformanceMetrics:
        """Measure performance of an operation"""
        start_time = time.time()
        start_memory = self._get_system_metrics()["memory_mb"]
        start_cpu = self._get_system_metrics()["cpu_percent"]
        
        try:
            result = func(*args, **kwargs)
            success = True
            error_count = 0
        except Exception as e:
            result = None
            success = False
            error_count = 1
            logger.error(f"Operation {operation_name} failed: {e}")
        
        end_time = time.time()
        end_metrics = self._get_system_metrics()
        
        execution_time = end_time - start_time
        memory_usage = end_metrics["memory_mb"] - start_memory
        cpu_usage = end_metrics["cpu_percent"] - start_cpu
        success_rate = 100.0 if success else 0.0
        
        # Update operation timings
        if operation_name not in self.operation_timings:
            self.operation_timings[operation_name] = []
        self.operation_timings[operation_name].append(execution_time)
        
        # Keep only last 100 timings
        if len(self.operation_timings[operation_name]) > 100:
            self.operation_timings[operation_name] = self.operation_timings[operation_name][-100:]
        
        # Calculate percentiles
        timings = self.operation_timings[operation_name]
        latency_p95 = statistics.quantiles(timings, n=20)[18] if len(timings) > 1 else execution_time
        latency_p99 = statistics.quantiles(timings, n=100)[98] if len(timings) > 1 else execution_time
        
        # Calculate throughput (operations per second)
        throughput = 1.0 / execution_time if execution_time > 0 else 0
        
        # Determine bottleneck type
        bottleneck_type = None
        if memory_usage > self.config.memory_threshold_mb:
            bottleneck_type = "memory"
        elif cpu_usage > self.config.cpu_threshold_percent:
            bottleneck_type = "cpu"
        elif execution_time > 2.0:
            bottleneck_type = "latency"
        
        metrics = PerformanceMetrics(
            operation_name=operation_name,
            execution_time=execution_time,
            memory_usage=max(0, memory_usage),
            cpu_usage=max(0, cpu_usage),
            success_rate=success_rate,
            error_count=error_count,
            timestamp=datetime.now(),
            throughput=throughput,
            latency_p95=latency_p95,
            latency_p99=latency_p99,
            cache_hit_rate=0.0,  # Will be updated by cache decorator
            concurrent_operations=1,
            optimization_score=0.0,
            bottleneck_type=bottleneck_type
        )
        
        metrics.calculate_optimization_score()
        return metrics
    
    def _cache_key(self, operation: str, *args, **kwargs) -> str:
        """Generate cache key for operation"""
        import hashlib
        key_data = f"{operation}_{str(args)}_{str(sorted(kwargs.items()))}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _is_cache_valid(self, cache_entry: Dict[str, Any]) -> bool:
        """Check if cache entry is still valid"""
        if not cache_entry:
            return False
        
        created_time = cache_entry.get("created_at", 0)
        return time.time() - created_time < self.cache_ttl
    
    def cached_operation(self, operation_name: str):
        """Decorator for caching operations"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                if not self.config.enable_caching:
                    return await func(*args, **kwargs)
                
                cache_key = self._cache_key(operation_name, *args, **kwargs)
                
                # Check cache
                if cache_key in self.cache:
                    cache_entry = self.cache[cache_key]
                    if self._is_cache_valid(cache_entry):
                        self.cache_stats["hits"] += 1
                        logger.debug(f"Cache hit for {operation_name}")
                        return cache_entry["result"]
                
                # Cache miss - execute operation
                self.cache_stats["misses"] += 1
                result = await func(*args, **kwargs)
                
                # Store in cache
                self.cache[cache_key] = {
                    "result": result,
                    "created_at": time.time(),
                    "operation": operation_name
                }
                
                # Cleanup old cache entries
                if len(self.cache) > self.max_cache_size:
                    oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]["created_at"])
                    del self.cache[oldest_key]
                
                return result
            return wrapper
        return decorator
    
    async def start_monitoring(self):
        """Start real-time performance monitoring"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitoring_task = asyncio.create_task(self._monitoring_loop())
        logger.info("Performance monitoring started")
    
    async def stop_monitoring(self):
        """Stop real-time performance monitoring"""
        self.monitoring_active = False
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
        logger.info("Performance monitoring stopped")
    
    async def _monitoring_loop(self):
        """Real-time monitoring loop"""
        while self.monitoring_active:
            try:
                metrics = self._get_system_metrics()
                self.system_metrics_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "metrics": metrics
                })
                
                # Keep only last 1000 entries
                if len(self.system_metrics_history) > 1000:
                    self.system_metrics_history = self.system_metrics_history[-1000:]
                
                # Check for performance issues
                await self._check_performance_thresholds(metrics)
                
                await asyncio.sleep(5)  # Monitor every 5 seconds
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(10)
    
    async def _check_performance_thresholds(self, metrics: Dict[str, float]):
        """Check performance thresholds and create alerts if needed"""
        if metrics["memory_mb"] > self.config.memory_threshold_mb:
            logger.warning(f"High memory usage detected: {metrics['memory_mb']:.2f}MB")
        
        if metrics["cpu_percent"] > self.config.cpu_threshold_percent:
            logger.warning(f"High CPU usage detected: {metrics['cpu_percent']:.2f}%")
        
        if metrics["system_memory_percent"] > 90:
            logger.warning(f"System memory usage critical: {metrics['system_memory_percent']:.2f}%")
        
    async def run_performance_benchmark(self) -> Dict[str, Any]:
        """Run comprehensive performance benchmark with enhanced metrics"""
        logger.info("Starting Enhanced BFSI Agent Performance Benchmark")
        
        start_time = datetime.now()
        benchmark_results = {
            "start_time": start_time.isoformat(),
            "tests": {},
            "overall_score": 0.0,
            "recommendations": [],
            "system_info": self._get_system_metrics(),
            "config": {
                "warmup_iterations": self.config.warmup_iterations,
                "test_iterations": self.config.test_iterations,
                "timeout_seconds": self.config.timeout_seconds,
                "concurrent_operations": self.config.concurrent_operations
            }
        }
        
        try:
            # Warmup phase
            await self._warmup_phase()
            
            # Test 1: Basic Operations Performance
            basic_ops_result = await self._test_basic_operations_enhanced()
            benchmark_results["tests"]["basic_operations"] = basic_ops_result
            
            # Test 2: Sub-Agent Performance
            sub_agent_result = await self._test_sub_agent_performance_enhanced()
            benchmark_results["tests"]["sub_agents"] = sub_agent_result
            
            # Test 3: Advanced Operations Performance
            advanced_ops_result = await self._test_advanced_operations_enhanced()
            benchmark_results["tests"]["advanced_operations"] = advanced_ops_result
            
            # Test 4: Concurrent Operations Performance
            concurrent_result = await self._test_concurrent_operations_enhanced()
            benchmark_results["tests"]["concurrent_operations"] = concurrent_result
            
            # Test 5: Memory and Resource Usage
            resource_result = await self._test_resource_usage_enhanced()
            benchmark_results["tests"]["resource_usage"] = resource_result
        
            # Test 6: Cache Performance
            cache_result = await self._test_cache_performance()
            benchmark_results["tests"]["cache_performance"] = cache_result
            
            # Test 7: Stress Testing
            stress_result = await self._test_stress_performance()
            benchmark_results["tests"]["stress_testing"] = stress_result
            
            # Calculate overall score with weighted metrics
            overall_score = self._calculate_weighted_score(benchmark_results["tests"])
            benchmark_results["overall_score"] = overall_score
            
            # Generate intelligent recommendations
            benchmark_results["recommendations"] = await self._generate_intelligent_recommendations(benchmark_results)
            
            # Performance analysis
            benchmark_results["analysis"] = await self._analyze_performance_patterns(benchmark_results)
            
            benchmark_results["end_time"] = datetime.now().isoformat()
            benchmark_results["duration"] = (datetime.now() - start_time).total_seconds()
            
            self.benchmark_results = benchmark_results
            logger.info(f"Enhanced performance benchmark completed. Overall score: {benchmark_results['overall_score']:.2f}")
            
            return benchmark_results
            
        except Exception as e:
            logger.error(f"Benchmark failed: {e}")
            benchmark_results["error"] = str(e)
            benchmark_results["end_time"] = datetime.now().isoformat()
            return benchmark_results
    
    async def _warmup_phase(self):
        """Warmup phase to stabilize performance"""
        logger.info("Running warmup phase...")
        
        warmup_operations = [
            ("warmup_basic", {"operation": "risk_assessment", "context": {"test": True}}),
            ("warmup_sub_agent", {"operation": "compliance_check", "context": {"test": True}}),
            ("warmup_advanced", {"operation": "advanced_assessment", "context": {"test": True}})
        ]
        
        for i in range(self.config.warmup_iterations):
            for op_name, op_data in warmup_operations:
                try:
                    if hasattr(self.agent, 'perform_grc_operation'):
                        await self.agent.perform_grc_operation(op_data["operation"], op_data["context"])
                    elif hasattr(self.agent, 'execute_enhanced_operation'):
                        await self.agent.execute_enhanced_operation(op_data["operation"], op_data["context"])
                except Exception as e:
                    logger.debug(f"Warmup operation failed: {e}")
            
            # Small delay between warmup iterations
            await asyncio.sleep(0.1)
        
        logger.info("Warmup phase completed")
    
    def _calculate_weighted_score(self, tests: Dict[str, Any]) -> float:
        """Calculate weighted overall score"""
        weights = {
            "basic_operations": 0.20,
            "sub_agents": 0.15,
            "advanced_operations": 0.25,
            "concurrent_operations": 0.15,
            "resource_usage": 0.15,
            "cache_performance": 0.05,
            "stress_testing": 0.05
        }
        
        weighted_sum = 0
        total_weight = 0
        
        for test_name, test_result in tests.items():
            if test_name in weights and "score" in test_result:
                weighted_sum += test_result["score"] * weights[test_name]
                total_weight += weights[test_name]
        
        return weighted_sum / total_weight if total_weight > 0 else 0
    
    async def _test_basic_operations_enhanced(self) -> Dict[str, Any]:
        """Enhanced test for basic operations performance with detailed metrics"""
        logger.info("Testing basic operations performance with enhanced metrics")
        
        operations = [
            ("risk_assessment", {"business_unit": "retail_banking", "risk_scope": "comprehensive"}),
            ("compliance_check", {"framework": "Basel III", "business_unit": "capital_management"}),
            ("policy_review", {"policy_id": "POL-001", "review_type": "annual"})
        ]
        
        results = []
        execution_times = []
        success_count = 0
        memory_usage = []
        cpu_usage = []
        
        for iteration in range(self.config.test_iterations):
            for op_name, context in operations:
                metrics = self._measure_operation(
                    f"{op_name}_{iteration}",
                    lambda: asyncio.run(self._execute_operation_safely(op_name, context))
                )
                
                execution_times.append(metrics.execution_time)
                memory_usage.append(metrics.memory_usage)
                cpu_usage.append(metrics.cpu_usage)
                
                if metrics.success_rate == 100:
                    success_count += 1
                
                results.append({
                    "operation": op_name,
                    "iteration": iteration,
                    "execution_time": metrics.execution_time,
                    "memory_usage": metrics.memory_usage,
                    "cpu_usage": metrics.cpu_usage,
                    "success": metrics.success_rate == 100,
                    "optimization_score": metrics.optimization_score,
                    "performance_level": metrics.get_performance_level().value
                })
        
        total_operations = len(operations) * self.config.test_iterations
        success_rate = (success_count / total_operations) * 100
        average_time = statistics.mean(execution_times) if execution_times else 0
        median_time = statistics.median(execution_times) if execution_times else 0
        p95_time = statistics.quantiles(execution_times, n=20)[18] if len(execution_times) > 1 else average_time
        
        # Calculate enhanced score
        time_score = max(0, 100 - (average_time * 15))
        consistency_score = max(0, 100 - (statistics.stdev(execution_times) * 10)) if len(execution_times) > 1 else 100
        reliability_score = success_rate
        resource_score = max(0, 100 - (statistics.mean(memory_usage) / 10))
        
        score = (time_score + consistency_score + reliability_score + resource_score) / 4
        
        return {
            "operations_tested": len(operations),
            "iterations": self.config.test_iterations,
            "total_operations": total_operations,
            "success_rate": success_rate,
            "average_time": average_time,
            "median_time": median_time,
            "p95_time": p95_time,
            "time_std": statistics.stdev(execution_times) if len(execution_times) > 1 else 0,
            "average_memory": statistics.mean(memory_usage) if memory_usage else 0,
            "average_cpu": statistics.mean(cpu_usage) if cpu_usage else 0,
            "score": score,
            "detailed_scores": {
                "time_score": time_score,
                "consistency_score": consistency_score,
                "reliability_score": reliability_score,
                "resource_score": resource_score
            },
            "results": results
        }
    
    async def _execute_operation_safely(self, op_name: str, context: Dict[str, Any]):
        """Execute operation with timeout and error handling"""
        try:
            if hasattr(self.agent, 'perform_grc_operation'):
                return await asyncio.wait_for(
                    self.agent.perform_grc_operation(op_name, context),
                    timeout=self.config.timeout_seconds
                )
            elif hasattr(self.agent, 'execute_enhanced_operation'):
                return await asyncio.wait_for(
                    self.agent.execute_enhanced_operation(op_name, context),
                    timeout=self.config.timeout_seconds
                )
            else:
                return {"success": False, "error": "No suitable operation method found"}
        except asyncio.TimeoutError:
            return {"success": False, "error": "Operation timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _test_sub_agent_performance(self) -> Dict[str, Any]:
        """Test sub-agent performance"""
        logger.info("Testing sub-agent performance")
        
        sub_agent_tests = []
        total_time = 0
        success_count = 0
        
        for agent_type, agent in self.agent.sub_agents.items():
            start_time = time.time()
            try:
                result = await agent.execute_task({
                    "task_type": "performance_test",
                    "agent_type": agent_type.value
                })
                execution_time = time.time() - start_time
                total_time += execution_time
                
                if result.get("status") != "error":
                    success_count += 1
                
                sub_agent_tests.append({
                    "agent_type": agent_type.value,
                    "agent_name": agent.name,
                    "execution_time": execution_time,
                    "success": result.get("status") != "error",
                    "response": result
                })
                
            except Exception as e:
                execution_time = time.time() - start_time
                total_time += execution_time
                sub_agent_tests.append({
                    "agent_type": agent_type.value,
                    "agent_name": agent.name,
                    "execution_time": execution_time,
                    "success": False,
                    "error": str(e)
                })
        
        success_rate = (success_count / len(self.agent.sub_agents)) * 100
        average_time = total_time / len(self.agent.sub_agents)
        
        # Calculate score
        score = min(100, max(0, 100 - (average_time * 5) + (success_rate * 0.3)))
        
        return {
            "sub_agents_tested": len(self.agent.sub_agents),
            "total_time": total_time,
            "average_time": average_time,
            "success_rate": success_rate,
            "score": score,
            "results": sub_agent_tests
        }
    
    async def _test_advanced_operations(self) -> Dict[str, Any]:
        """Test advanced operations performance"""
        logger.info("Testing advanced operations performance")
        
        advanced_operations = [
            ("comprehensive_assessment", {"business_unit": "retail_banking", "risk_scope": "comprehensive"}),
            ("regulatory_compliance", {"jurisdiction": "US", "framework": "Basel III"}),
            ("risk_management", {"portfolio_type": "retail_banking", "risk_categories": ["credit", "market", "operational"]}),
            ("fraud_prevention", {"monitoring_period": "real_time", "fraud_types": ["payment", "identity", "account_takeover"]})
        ]
        
        results = []
        total_time = 0
        success_count = 0
        
        for op_name, context in advanced_operations:
            start_time = time.time()
            try:
                result = await self.agent.execute_enhanced_operation(op_name, context)
                execution_time = time.time() - start_time
                total_time += execution_time
                
                if result.get("overall_status") == "completed":
                    success_count += 1
                
                results.append({
                    "operation": op_name,
                    "execution_time": execution_time,
                    "success": result.get("overall_status") == "completed",
                    "status": result.get("overall_status", "unknown")
                })
                
            except Exception as e:
                execution_time = time.time() - start_time
                total_time += execution_time
                results.append({
                    "operation": op_name,
                    "execution_time": execution_time,
                    "success": False,
                    "error": str(e)
                })
        
        success_rate = (success_count / len(advanced_operations)) * 100
        average_time = total_time / len(advanced_operations)
        
        # Calculate score
        score = min(100, max(0, 100 - (average_time * 2) + (success_rate * 0.4)))
        
        return {
            "operations_tested": len(advanced_operations),
            "total_time": total_time,
            "average_time": average_time,
            "success_rate": success_rate,
            "score": score,
            "results": results
        }
    
    async def _test_concurrent_operations(self) -> Dict[str, Any]:
        """Test concurrent operations performance"""
        logger.info("Testing concurrent operations performance")
        
        # Create multiple concurrent operations
        concurrent_operations = [
            self.agent.perform_advanced_risk_assessment({
                "business_unit": "retail_banking",
                "risk_scope": "comprehensive"
            }),
            self.agent.get_comprehensive_analytics(),
            self.agent.execute_enhanced_operation("comprehensive_assessment", {
                "business_unit": "investment_banking",
                "risk_scope": "market_risk"
            }),
            self.agent.generate_compliance_report("comprehensive")
        ]
        
        start_time = time.time()
        try:
            results = await asyncio.gather(*concurrent_operations, return_exceptions=True)
            total_time = time.time() - start_time
            
            success_count = sum(1 for result in results if not isinstance(result, Exception))
            success_rate = (success_count / len(concurrent_operations)) * 100
            
            # Calculate score
            score = min(100, max(0, 100 - (total_time * 0.5) + (success_rate * 0.6)))
            
            return {
                "concurrent_operations": len(concurrent_operations),
                "total_time": total_time,
                "success_rate": success_rate,
                "score": score,
                "results": [str(result)[:100] + "..." if len(str(result)) > 100 else str(result) for result in results]
            }
            
        except Exception as e:
            total_time = time.time() - start_time
            return {
                "concurrent_operations": len(concurrent_operations),
                "total_time": total_time,
                "success_rate": 0,
                "score": 0,
                "error": str(e)
            }
    
    async def _test_resource_usage(self) -> Dict[str, Any]:
        """Test resource usage"""
        logger.info("Testing resource usage")
        
        # Get current metrics
        metrics = self.agent.metrics
        
        # Resource-intensive operations require actual resource monitoring
        start_time = time.time()
        await self.agent.perform_advanced_risk_assessment({
            "business_unit": "retail_banking",
            "risk_scope": "comprehensive"
        })
        execution_time = time.time() - start_time
        
        # Calculate resource efficiency score
        memory_efficiency = 100 - (len(self.agent.performance_history) * 0.1)
        cpu_efficiency = 100 - (execution_time * 10)
        alert_efficiency = 100 - (len(self.agent.alerts) * 0.5)
        
        overall_efficiency = (memory_efficiency + cpu_efficiency + alert_efficiency) / 3
        
        return {
            "execution_time": execution_time,
            "memory_efficiency": memory_efficiency,
            "cpu_efficiency": cpu_efficiency,
            "alert_efficiency": alert_efficiency,
            "overall_efficiency": overall_efficiency,
            "score": min(100, max(0, overall_efficiency)),
            "metrics": {
                "total_operations": metrics.total_operations,
                "successful_operations": metrics.successful_operations,
                "failed_operations": metrics.failed_operations,
                "average_response_time": metrics.average_response_time
            }
        }
    
    async def _generate_optimization_recommendations(self, benchmark_results: Dict[str, Any]) -> List[str]:
        """Generate optimization recommendations based on benchmark results"""
        recommendations = []
        
        # Analyze basic operations
        basic_ops = benchmark_results["tests"]["basic_operations"]
        if basic_ops["average_time"] > 2.0:
            recommendations.append("Optimize basic operations - average time too high")
        if basic_ops["success_rate"] < 90:
            recommendations.append("Improve basic operations reliability")
        
        # Analyze sub-agent performance
        sub_agents = benchmark_results["tests"]["sub_agents"]
        if sub_agents["average_time"] > 1.0:
            recommendations.append("Optimize sub-agent response times")
        if sub_agents["success_rate"] < 95:
            recommendations.append("Improve sub-agent reliability")
        
        # Analyze advanced operations
        advanced_ops = benchmark_results["tests"]["advanced_operations"]
        if advanced_ops["average_time"] > 5.0:
            recommendations.append("Optimize advanced operations - consider parallel processing")
        if advanced_ops["success_rate"] < 85:
            recommendations.append("Improve advanced operations error handling")
        
        # Analyze concurrent operations
        concurrent_ops = benchmark_results["tests"]["concurrent_operations"]
        if concurrent_ops["success_rate"] < 80:
            recommendations.append("Improve concurrent operation handling")
        if concurrent_ops["total_time"] > 10:
            recommendations.append("Optimize concurrent operation execution time")
        
        # Analyze resource usage
        resource_usage = benchmark_results["tests"]["resource_usage"]
        if resource_usage["overall_efficiency"] < 70:
            recommendations.append("Optimize resource usage and memory management")
        
        # General recommendations
        if benchmark_results["overall_score"] < 80:
            recommendations.append("Overall performance needs improvement")
        if benchmark_results["overall_score"] < 60:
            recommendations.append("Critical performance issues detected")
        
        return recommendations
    
    async def optimize_agent_performance(self) -> Dict[str, Any]:
        """Optimize agent performance based on benchmark results"""
        logger.info("Starting agent performance optimization")
        
        optimization_results = {
            "start_time": datetime.now().isoformat(),
            "optimizations_applied": [],
            "performance_improvements": {},
            "recommendations": []
        }
        
        # Run benchmark first
        benchmark_results = await self.run_performance_benchmark()
        
        # Apply optimizations based on results
        if benchmark_results["overall_score"] < 80:
            # Optimize basic operations
            if benchmark_results["tests"]["basic_operations"]["average_time"] > 2.0:
                await self._optimize_basic_operations()
                optimization_results["optimizations_applied"].append("Basic operations optimization")
            
            # Optimize sub-agent performance
            if benchmark_results["tests"]["sub_agents"]["average_time"] > 1.0:
                await self._optimize_sub_agents()
                optimization_results["optimizations_applied"].append("Sub-agent optimization")
            
            # Optimize advanced operations
            if benchmark_results["tests"]["advanced_operations"]["average_time"] > 5.0:
                await self._optimize_advanced_operations()
                optimization_results["optimizations_applied"].append("Advanced operations optimization")
        
        # Run benchmark again to measure improvements
        post_optimization_benchmark = await self.run_performance_benchmark()
        
        # Calculate improvements
        optimization_results["performance_improvements"] = {
            "overall_score_improvement": post_optimization_benchmark["overall_score"] - benchmark_results["overall_score"],
            "basic_operations_improvement": post_optimization_benchmark["tests"]["basic_operations"]["score"] - benchmark_results["tests"]["basic_operations"]["score"],
            "sub_agents_improvement": post_optimization_benchmark["tests"]["sub_agents"]["score"] - benchmark_results["tests"]["sub_agents"]["score"],
            "advanced_operations_improvement": post_optimization_benchmark["tests"]["advanced_operations"]["score"] - benchmark_results["tests"]["advanced_operations"]["score"]
        }
        
        optimization_results["recommendations"] = post_optimization_benchmark["recommendations"]
        optimization_results["end_time"] = datetime.now().isoformat()
        
        logger.info(f"Performance optimization completed. Overall score improvement: {optimization_results['performance_improvements']['overall_score_improvement']:.2f}")
        
        return optimization_results
    
    async def _test_cache_performance(self) -> Dict[str, Any]:
        """Test cache performance"""
        logger.info("Testing cache performance")
        
        # Clear cache for clean test
        self.cache.clear()
        self.cache_stats = {"hits": 0, "misses": 0}
        
        # Test cache operations
        test_operations = [
            ("cache_test_1", {"operation": "cache_test_1"}),
            ("cache_test_2", {"operation": "cache_test_2"}),
            ("cache_test_3", {"operation": "cache_test_3"})
        ]
        
        # First run (cache misses)
        for op_name, context in test_operations:
            await self._execute_operation_safely(op_name, context)
        
        # Second run (cache hits)
        for op_name, context in test_operations:
            await self._execute_operation_safely(op_name, context)
        
        total_requests = len(test_operations) * 2
        hit_rate = (self.cache_stats["hits"] / total_requests) * 100 if total_requests > 0 else 0
        
        score = min(100, hit_rate * 1.5)  # Cache hit rate is important
        
        return {
            "cache_size": len(self.cache),
            "cache_hits": self.cache_stats["hits"],
            "cache_misses": self.cache_stats["misses"],
            "hit_rate": hit_rate,
            "total_requests": total_requests,
            "score": score
        }
    
    async def _test_stress_performance(self) -> Dict[str, Any]:
        """Test stress performance with high load"""
        logger.info("Testing stress performance")
        
        # Create high concurrent load
        stress_operations = []
        for i in range(self.config.concurrent_operations * 2):
            stress_operations.append(self._execute_operation_safely("stress_test", {"load": i}))
        
        start_time = time.time()
        results = await asyncio.gather(*stress_operations, return_exceptions=True)
        total_time = time.time() - start_time
        
        success_count = sum(1 for result in results if not isinstance(result, Exception) and result.get("success", False))
        success_rate = (success_count / len(stress_operations)) * 100
        
        # Calculate throughput
        throughput = len(stress_operations) / total_time if total_time > 0 else 0
        
        score = min(100, success_rate + (throughput * 2))
        
        return {
            "concurrent_operations": len(stress_operations),
            "total_time": total_time,
            "success_rate": success_rate,
            "throughput": throughput,
            "score": score
        }
    
    async def _generate_intelligent_recommendations(self, benchmark_results: Dict[str, Any]) -> List[str]:
        """Generate intelligent optimization recommendations"""
        recommendations = []
        tests = benchmark_results.get("tests", {})
        
        # Analyze each test category
        for test_name, test_result in tests.items():
            score = test_result.get("score", 0)
            
            if score < 60:
                if test_name == "basic_operations":
                    recommendations.append("ð¨ CRITICAL: Basic operations severely underperforming - implement connection pooling and request batching")
                elif test_name == "sub_agents":
                    recommendations.append("ð¨ CRITICAL: Sub-agent performance critical - implement load balancing and health checks")
                elif test_name == "concurrent_operations":
                    recommendations.append("ð¨ CRITICAL: Concurrent operations failing - implement proper async/await patterns and semaphores")
                elif test_name == "resource_usage":
                    recommendations.append("ð¨ CRITICAL: Resource usage excessive - implement memory management and garbage collection optimization")
            
            elif score < 80:
                if test_name == "basic_operations":
                    recommendations.append("â ï¸ Basic operations need optimization - consider caching and query optimization")
                elif test_name == "sub_agents":
                    recommendations.append("â ï¸ Sub-agent performance suboptimal - implement circuit breakers and retry logic")
                elif test_name == "advanced_operations":
                    recommendations.append("â ï¸ Advanced operations need improvement - implement parallel processing")
                elif test_name == "cache_performance":
                    recommendations.append("â ï¸ Cache performance poor - optimize cache keys and TTL settings")
        
        # Overall recommendations
        overall_score = benchmark_results.get("overall_score", 0)
        if overall_score < 70:
            recommendations.append("ð¯ OVERALL: System requires comprehensive performance optimization")
        elif overall_score < 85:
            recommendations.append("â OVERALL: System performing well with minor optimizations needed")
        else:
            recommendations.append("ð OVERALL: Excellent performance - maintain current optimization levels")
        
        # Add specific technical recommendations
        recommendations.extend([
            "ð¡ Consider implementing request deduplication for repeated operations",
            "ð¡ Implement circuit breaker pattern for fault tolerance",
            "ð¡ Add performance monitoring dashboards for real-time insights",
            "ð¡ Optimize database queries and implement query caching",
            "ð¡ Consider horizontal scaling for high-load scenarios"
        ])
        
        return recommendations
    
    async def _analyze_performance_patterns(self, benchmark_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance patterns and trends"""
        analysis = {
            "bottlenecks": [],
            "strengths": [],
            "trends": {},
            "recommendations": []
        }
        
        tests = benchmark_results.get("tests", {})
        
        # Identify bottlenecks
        for test_name, test_result in tests.items():
            score = test_result.get("score", 0)
            if score < 70:
                analysis["bottlenecks"].append({
                    "component": test_name,
                    "score": score,
                    "severity": "critical" if score < 50 else "high" if score < 60 else "medium"
                })
        
        # Identify strengths
        for test_name, test_result in tests.items():
            score = test_result.get("score", 0)
            if score >= 90:
                analysis["strengths"].append({
                    "component": test_name,
                    "score": score,
                    "performance_level": "excellent"
                })
        
        # Performance trends (if historical data available)
        if len(self.performance_history) > 1:
            recent_scores = [p.optimization_score for p in self.performance_history[-10:]]
            if len(recent_scores) > 1:
                trend = "improving" if recent_scores[-1] > recent_scores[0] else "declining"
                analysis["trends"]["overall"] = {
                    "direction": trend,
                    "change": recent_scores[-1] - recent_scores[0]
                }
        
        return analysis
    
    async def _optimize_basic_operations(self):
        """Optimize basic operations with actual implementations"""
        logger.info("Optimizing basic operations")
        
        # Enable caching for basic operations
        self.config.enable_caching = True
        
        # Optimize timeout settings
        if hasattr(self.agent, 'operation_timeout'):
            self.agent.operation_timeout = min(self.agent.operation_timeout, 30)
        
        # Force garbage collection
        gc.collect()
        
        logger.info("Basic operations optimization completed")
    
    async def _optimize_sub_agents(self):
        """Optimize sub-agent performance with actual implementations"""
        logger.info("Optimizing sub-agent performance")
        
        # Reset circuit breakers if they exist
        for agent_type, agent in self.agent.sub_agents.items():
            if hasattr(agent, '_reset_circuit_breaker'):
                agent._reset_circuit_breaker()
        
        # Optimize concurrent operation limits
        if hasattr(self.agent, 'max_concurrent_operations'):
            self.agent.max_concurrent_operations = min(self.agent.max_concurrent_operations, 20)
        
        logger.info("Sub-agent optimization completed")
    
    async def _optimize_advanced_operations(self):
        """Optimize advanced operations with actual implementations"""
        logger.info("Optimizing advanced operations")
        
        # Enable parallel processing
        if hasattr(self.agent, 'enable_parallel_processing'):
            self.agent.enable_parallel_processing = True
        
        # Optimize memory usage
        gc.collect()
        
        logger.info("Advanced operations optimization completed")
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report"""
        return {
            "agent_id": self.agent.agent_id,
            "agent_name": self.agent.name,
            "current_metrics": self.agent.metrics.to_dict(),
            "performance_history": [metric.to_dict() for metric in self.performance_history],
            "benchmark_results": self.benchmark_results,
            "optimization_recommendations": self.optimization_recommendations,
            "timestamp": datetime.now().isoformat()
        }

async def main():
    """Main function for performance optimization"""
    # Initialize BFSI agent
    agent = BFSIGRCAgent(agent_id="performance-test-agent", name="Performance Test Agent")
    
    # Initialize performance optimizer
    optimizer = BFSIPerformanceOptimizer(agent)
    
    print("ð Starting BFSI Agent Performance Optimization")
    print("=" * 60)
    
    # Run performance benchmark
    print("\nð Running Performance Benchmark...")
    benchmark_results = await optimizer.run_performance_benchmark()
    
    print(f"Overall Score: {benchmark_results['overall_score']:.2f}/100")
    print(f"Duration: {benchmark_results['duration']:.2f} seconds")
    
    # Show test results
    for test_name, test_result in benchmark_results["tests"].items():
        print(f"\n{test_name.replace('_', ' ').title()}:")
        print(f"  Score: {test_result['score']:.2f}/100")
        if 'success_rate' in test_result:
            print(f"  Success Rate: {test_result['success_rate']:.1f}%")
        if 'average_time' in test_result:
            print(f"  Average Time: {test_result['average_time']:.2f}s")
    
    # Show recommendations
    if benchmark_results["recommendations"]:
        print(f"\nð¡ Optimization Recommendations:")
        for i, recommendation in enumerate(benchmark_results["recommendations"], 1):
            print(f"  {i}. {recommendation}")
    
    # Run optimization if needed
    if benchmark_results["overall_score"] < 80:
        print(f"\nð§ Running Performance Optimization...")
        optimization_results = await optimizer.optimize_agent_performance()
        
        print(f"Optimizations Applied: {len(optimization_results['optimizations_applied'])}")
        for optimization in optimization_results["optimizations_applied"]:
            print(f"  â¢ {optimization}")
        
        improvements = optimization_results["performance_improvements"]
        print(f"\nPerformance Improvements:")
        print(f"  Overall Score: +{improvements['overall_score_improvement']:.2f}")
        print(f"  Basic Operations: +{improvements['basic_operations_improvement']:.2f}")
        print(f"  Sub-Agents: +{improvements['sub_agents_improvement']:.2f}")
        print(f"  Advanced Operations: +{improvements['advanced_operations_improvement']:.2f}")
    
    # Generate performance report
    performance_report = optimizer.get_performance_report()
    
    print(f"\nð Performance Report Generated")
    print(f"Report includes:")
    print(f"  â¢ Current metrics")
    print(f"  â¢ Performance history")
    print(f"  â¢ Benchmark results")
    print(f"  â¢ Optimization recommendations")
    
    print(f"\nâ BFSI Agent Performance Optimization Completed!")

if __name__ == "__main__":
    asyncio.run(main())

