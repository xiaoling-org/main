"""
实时数据系统
确保所有数据都是最新和实时的
"""

import asyncio
import aiohttp
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataFreshness(Enum):
    """数据新鲜度等级"""
    REALTIME = "realtime"      # <1分钟
    NEAR_REALTIME = "near_realtime"  # <5分钟
    RECENT = "recent"         # <15分钟
    STALE = "stale"           # >15分钟

@dataclass
class RealTimeDataConfig:
    """实时数据配置"""
    data_type: str
    refresh_interval_seconds: int
    max_age_seconds: int
    required_freshness: DataFreshness
    retry_count: int = 3
    retry_delay_seconds: int = 2

class RealTimeDataSystem:
    """实时数据系统"""
    
    def __init__(self):
        # 数据配置
        self.data_configs = {
            'financial_market': RealTimeDataConfig(
                data_type='financial_market',
                refresh_interval_seconds=30,  # 每30秒刷新
                max_age_seconds=300,  # 5分钟最大年龄
                required_freshness=DataFreshness.NEAR_REALTIME
            ),
            'stock_prices': RealTimeDataConfig(
                data_type='stock_prices',
                refresh_interval_seconds=10,  # 每10秒刷新
                max_age_seconds=60,  # 1分钟最大年龄
                required_freshness=DataFreshness.REALTIME
            ),
            'crypto_prices': RealTimeDataConfig(
                data_type='crypto_prices',
                refresh_interval_seconds=5,  # 每5秒刷新
                max_age_seconds=30,  # 30秒最大年龄
                required_freshness=DataFreshness.REALTIME
            ),
            'news': RealTimeDataConfig(
                data_type='news',
                refresh_interval_seconds=60,  # 每60秒刷新
                max_age_seconds=600,  # 10分钟最大年龄
                required_freshness=DataFreshness.RECENT
            ),
            'economic_indicators': RealTimeDataConfig(
                data_type='economic_indicators',
                refresh_interval_seconds=300,  # 每5分钟刷新
                max_age_seconds=1800,  # 30分钟最大年龄
                required_freshness=DataFreshness.NEAR_REALTIME
            )
        }
        
        # 数据缓存
        self.data_cache: Dict[str, Dict[str, Any]] = {}
        
        # 数据源状态
        self.source_status: Dict[str, Dict[str, Any]] = {}
        
        # 订阅者列表
        self.subscribers: Dict[str, List[callable]] = {}
        
        # 运行状态
        self.is_running = False
        
    async def fetch_realtime_data(self, data_type: str, url: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """获取实时数据"""
        config = self.data_configs.get(data_type)
        if not config:
            raise ValueError(f"未知的数据类型: {data_type}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        for attempt in range(config.retry_count):
            try:
                async with aiohttp.ClientSession() as session:
                    timeout = aiohttp.ClientTimeout(total=10)
                    
                    async with session.get(url, params=params, headers=headers, timeout=timeout) as response:
                        if response.status == 200:
                            data = await response.json()
                            
                            # 添加时间戳和元数据
                            enriched_data = {
                                'data': data,
                                'metadata': {
                                    'fetch_time': datetime.now().isoformat(),
                                    'data_type': data_type,
                                    'source_url': url,
                                    'freshness': DataFreshness.REALTIME.value,
                                    'age_seconds': 0,
                                    'attempt': attempt + 1
                                }
                            }
                            
                            # 更新数据源状态
                            self.source_status[url] = {
                                'last_success': datetime.now().isoformat(),
                                'response_time': response.elapsed.total_seconds(),
                                'status': 'healthy'
                            }
                            
                            return enriched_data
                        else:
                            logger.warning(f"数据获取失败: {response.status} - {url}")
                            
            except asyncio.TimeoutError:
                logger.warning(f"请求超时: {url} (尝试 {attempt + 1}/{config.retry_count})")
            except Exception as e:
                logger.error(f"数据获取错误: {e} - {url}")
            
            # 重试前等待
            if attempt < config.retry_count - 1:
                await asyncio.sleep(config.retry_delay_seconds)
        
        # 所有尝试都失败
        self.source_status[url] = {
            'last_failure': datetime.now().isoformat(),
            'status': 'unhealthy'
        }
        
        raise Exception(f"无法获取数据: {data_type} from {url}")
    
    def calculate_freshness(self, fetch_time: str) -> DataFreshness:
        """计算数据新鲜度"""
        try:
            fetch_datetime = datetime.fromisoformat(fetch_time.replace('Z', '+00:00'))
            age_seconds = (datetime.now() - fetch_datetime).total_seconds()
            
            if age_seconds < 60:
                return DataFreshness.REALTIME
            elif age_seconds < 300:
                return DataFreshness.NEAR_REALTIME
            elif age_seconds < 900:
                return DataFreshness.RECENT
            else:
                return DataFreshness.STALE
        except:
            return DataFreshness.STALE
    
    def is_data_fresh(self, data: Dict[str, Any], config: RealTimeDataConfig) -> bool:
        """检查数据是否新鲜"""
        if 'metadata' not in data:
            return False
        
        metadata = data['metadata']
        fetch_time = metadata.get('fetch_time')
        
        if not fetch_time:
            return False
        
        freshness = self.calculate_freshness(fetch_time)
        
        # 检查是否满足要求的新鲜度
        freshness_order = {
            DataFreshness.REALTIME: 4,
            DataFreshness.NEAR_REALTIME: 3,
            DataFreshness.RECENT: 2,
            DataFreshness.STALE: 1
        }
        
        return freshness_order.get(freshness, 0) >= freshness_order.get(config.required_freshness, 0)
    
    async def get_or_refresh_data(self, data_type: str, force_refresh: bool = False) -> Dict[str, Any]:
        """获取或刷新数据"""
        config = self.data_configs.get(data_type)
        if not config:
            raise ValueError(f"未知的数据类型: {data_type}")
        
        # 检查缓存中是否有数据
        cached_data = self.data_cache.get(data_type)
        
        if cached_data and not force_refresh:
            # 检查数据是否仍然新鲜
            if self.is_data_fresh(cached_data, config):
                logger.info(f"使用缓存数据: {data_type}")
                return cached_data
            
            # 数据不新鲜，需要刷新
            logger.info(f"数据已过期，刷新: {data_type}")
        
        # 需要获取新数据
        logger.info(f"获取实时数据: {data_type}")
        
        # 根据数据类型选择数据源
        data_sources = self.get_data_sources(data_type)
        
        # 尝试从多个数据源获取
        for source_name, source_info in data_sources.items():
            try:
                data = await self.fetch_realtime_data(
                    data_type, 
                    source_info['url'], 
                    source_info.get('params')
                )
                
                # 更新缓存
                self.data_cache[data_type] = data
                
                # 通知订阅者
                await self.notify_subscribers(data_type, data)
                
                return data
                
            except Exception as e:
                logger.error(f"数据源 {source_name} 失败: {e}")
                continue
        
        # 所有数据源都失败
        if cached_data:
            logger.warning(f"所有数据源失败，使用过期缓存: {data_type}")
            return cached_data
        else:
            raise Exception(f"无法获取数据: {data_type}")
    
    def get_data_sources(self, data_type: str) -> Dict[str, Dict[str, Any]]:
        """获取数据源配置"""
        sources = {
            'financial_market': {
                'yahoo_finance': {
                    'url': 'https://query1.finance.yahoo.com/v8/finance/chart/%5EHSI',
                    'params': {'interval': '1m', 'range': '1d'}
                },
                'investing_com': {
                    'url': 'https://api.investing.com/api/financialdata/historical/179',
                    'params': {'interval': '1m', 'period': '1d'}
                }
            },
            'stock_prices': {
                'yahoo_quotes': {
                    'url': 'https://query1.finance.yahoo.com/v7/finance/quote',
                    'params': {'symbols': 'AAPL,MSFT,GOOGL'}
                }
            },
            'crypto_prices': {
                'coinbase': {
                    'url': 'https://api.coinbase.com/v2/prices/BTC-USD/spot'
                },
                'binance': {
                    'url': 'https://api.binance.com/api/v3/ticker/price',
                    'params': {'symbol': 'BTCUSDT'}
                }
            }
        }
        
        return sources.get(data_type, {})
    
    async def notify_subscribers(self, data_type: str, data: Dict[str, Any]):
        """通知订阅者"""
        if data_type in self.subscribers:
            for callback in self.subscribers[data_type]:
                try:
                    await callback(data_type, data)
                except Exception as e:
                    logger.error(f"通知订阅者失败: {e}")
    
    def subscribe(self, data_type: str, callback: callable):
        """订阅数据更新"""
        if data_type not in self.subscribers:
            self.subscribers[data_type] = []
        
        self.subscribers[data_type].append(callback)
        logger.info(f"新的订阅者: {data_type}")
    
    async def start_monitoring(self):
        """启动数据监控"""
        self.is_running = True
        logger.info("实时数据监控启动")
        
        while self.is_running:
            try:
                # 监控所有数据类型
                for data_type, config in self.data_configs.items():
                    try:
                        # 检查是否需要刷新
                        cached_data = self.data_cache.get(data_type)
                        needs_refresh = False
                        
                        if not cached_data:
                            needs_refresh = True
                        else:
                            metadata = cached_data.get('metadata', {})
                            fetch_time = metadata.get('fetch_time')
                            
                            if fetch_time:
                                fetch_datetime = datetime.fromisoformat(fetch_time.replace('Z', '+00:00'))
                                age_seconds = (datetime.now() - fetch_datetime).total_seconds()
                                
                                if age_seconds > config.refresh_interval_seconds:
                                    needs_refresh = True
                        
                        if needs_refresh:
                            await self.get_or_refresh_data(data_type)
                            
                    except Exception as e:
                        logger.error(f"监控 {data_type} 失败: {e}")
                
                # 等待下一次检查
                await asyncio.sleep(10)  # 每10秒检查一次
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"监控循环错误: {e}")
                await asyncio.sleep(30)  # 错误后等待30秒
    
    async def stop_monitoring(self):
        """停止数据监控"""
        self.is_running = False
        logger.info("实时数据监控停止")
    
    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        status = {
            'is_running': self.is_running,
            'data_types_monitored': list(self.data_configs.keys()),
            'cache_size': len(self.data_cache),
            'subscriber_count': sum(len(subs) for subs in self.subscribers.values()),
            'source_health': self.source_status,
            'timestamp': datetime.now().isoformat()
        }
        
        # 添加缓存数据新鲜度信息
        freshness_info = {}
        for data_type, data in self.data_cache.items():
            if 'metadata' in data:
                metadata = data['metadata']
                fetch_time = metadata.get('fetch_time', '')
                freshness = self.calculate_freshness(fetch_time)
                
                freshness_info[data_type] = {
                    'freshness': freshness.value,
                    'fetch_time': fetch_time,
                    'age_seconds': (datetime.now() - datetime.fromisoformat(fetch_time.replace('Z', '+00:00'))).total_seconds() if fetch_time else 'unknown'
                }
        
        status['cache_freshness'] = freshness_info
        return status

# 全局实时数据系统实例
realtime_system = RealTimeDataSystem()

async def ensure_realtime_data(data_type: str, max_age_seconds: int = 300) -> Dict[str, Any]:
    """
    确保获取实时数据的装饰器函数
    
    参数:
        data_type: 数据类型
        max_age_seconds: 最大允许年龄（秒）
    
    返回:
        实时数据
    """
    logger.info(f"确保实时数据: {data_type}, 最大年龄: {max_age_seconds}秒")
    
    # 获取数据
    data = await realtime_system.get_or_refresh_data(data_type)
    
    # 检查数据新鲜度
    metadata = data.get('metadata', {})
    fetch_time = metadata.get('fetch_time')
    
    if fetch_time:
        fetch_datetime = datetime.fromisoformat(fetch_time.replace('Z', '+00:00'))
        age_seconds = (datetime.now() - fetch_datetime).total_seconds()
        
        if age_seconds > max_age_seconds:
            logger.warning(f"数据年龄 {age_seconds:.1f}秒 超过限制 {max_age_seconds}秒")
            
            # 强制刷新
            data = await realtime_system.get_or_refresh_data(data_type, force_refresh=True)
    
    return data

# 使用示例
async def example_usage():
    """使用示例"""
    print("🚀 实时数据系统示例")
    print("="*50)
    
    # 启动监控
    monitoring_task = asyncio.create_task(realtime_system.start_monitoring())
    
    try:
        # 等待系统启动
        await asyncio.sleep(2)
        
        # 获取系统状态
        status = realtime_system.get_system_status()
        print(f"📊 系统状态: {'运行中' if status['is_running'] else '已停止'}")
        print(f"📈 监控的数据类型: {', '.join(status['data_types_monitored'])}")
        
        # 获取实时金融数据
        print("\n📊 获取实时金融数据...")
        try:
            financial_data = await ensure_realtime_data('financial_market', max_age_seconds=60)
            metadata = financial_data.get('metadata', {})
            print(f"✅ 数据获取成功")
            print(f"🕒 数据时间: {metadata.get('fetch_time', '未知')}")
            print(f"⚡ 新鲜度: {metadata.get('freshness', '未知')}")
            print(f"📡 数据源: {metadata.get('source_url', '未知')}")
        except Exception as e:
            print(f"❌ 获取失败: {e}")
        
        # 等待一段时间查看自动刷新
        print("\n⏳ 等待自动刷新...")
        await asyncio.sleep(40)
        
        # 再次检查状态
        status = realtime_system.get_system_status()
        print(f"\n📊 刷新后系统状态:")
        for data_type, freshness_info in status.get('cache_freshness', {}).items():
            print(f"  • {data_type}: {freshness_info['freshness']} ({freshness_info['age_seconds']:.1f}秒前)")
        
    finally:
        # 停止监控
        await realtime_system.stop_monitoring()
        monitoring_task.cancel()
        
        try:
            await monitoring_task
        except asyncio.CancelledError:
            pass
        
        print("\n✅ 实时数据系统示例完成")

if __name__ == "__main__":
    # 运行示例
    asyncio.run(example_usage())