"""
数据采集器基类
定义所有数据采集器的通用接口和功能
"""

import abc
import logging
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
import json


@dataclass
class CollectedItem:
    """采集的数据项"""
    source: str  # 数据源名称
    source_type: str  # 数据源类型 (github, hackernews, news, social, hongkong)
    title: str  # 标题
    content: str  # 内容
    url: str  # 原始URL
    author: Optional[str] = None  # 作者
    published_at: Optional[datetime] = None  # 发布时间
    metadata: Optional[Dict[str, Any]] = None  # 元数据
    raw_data: Optional[Dict[str, Any]] = None  # 原始数据
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        if self.published_at:
            data['published_at'] = self.published_at.isoformat()
        if self.metadata is None:
            data['metadata'] = {}
        if self.raw_data is None:
            data['raw_data'] = {}
        return data
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False)


class BaseCollector(abc.ABC):
    """数据采集器基类"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        初始化采集器
        
        Args:
            name: 采集器名称
            config: 配置字典
        """
        self.name = name
        self.config = config
        self.logger = logging.getLogger(f"collector.{name}")
        self.items_collected = 0
        self.last_collection_time = None
        
    @abc.abstractmethod
    async def collect(self) -> List[CollectedItem]:
        """
        执行数据采集
        
        Returns:
            采集到的数据项列表
        """
        pass
    
    @abc.abstractmethod
    def validate_config(self) -> bool:
        """
        验证配置是否有效
        
        Returns:
            配置是否有效
        """
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取采集器状态
        
        Returns:
            状态信息字典
        """
        return {
            "name": self.name,
            "enabled": self.config.get("enabled", True),
            "items_collected": self.items_collected,
            "last_collection_time": self.last_collection_time.isoformat() if self.last_collection_time else None,
            "config_valid": self.validate_config()
        }
    
    async def run(self) -> List[CollectedItem]:
        """
        运行采集器并返回结果
        
        Returns:
            采集到的数据项列表
        """
        self.logger.info(f"开始采集数据: {self.name}")
        start_time = time.time()
        
        try:
            # 验证配置
            if not self.validate_config():
                self.logger.error(f"配置无效: {self.name}")
                return []
            
            # 执行采集
            items = await self.collect()
            
            # 更新状态
            self.items_collected += len(items)
            self.last_collection_time = datetime.now()
            
            # 记录日志
            elapsed_time = time.time() - start_time
            self.logger.info(f"采集完成: {self.name}, 采集到 {len(items)} 个项目, 耗时 {elapsed_time:.2f} 秒")
            
            return items
            
        except Exception as e:
            self.logger.error(f"采集失败: {self.name}, 错误: {str(e)}", exc_info=True)
            return []
    
    def _make_request(self, url: str, headers: Optional[Dict[str, str]] = None, 
                     params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        发送HTTP请求（简化版，实际实现需要requests库）
        
        Args:
            url: 请求URL
            headers: 请求头
            params: 查询参数
            
        Returns:
            响应数据
        """
        # 这里是一个简化实现，实际项目中应该使用requests库
        self.logger.debug(f"发送请求: {url}")
        return {"url": url, "headers": headers, "params": params}
    
    def _parse_html(self, html: str) -> Any:
        """
        解析HTML（简化版，实际实现需要BeautifulSoup）
        
        Args:
            html: HTML字符串
            
        Returns:
            解析后的对象
        """
        # 这里是一个简化实现，实际项目中应该使用BeautifulSoup
        self.logger.debug(f"解析HTML，长度: {len(html)}")
        return {"html_length": len(html)}
    
    def _parse_json(self, json_str: str) -> Dict[str, Any]:
        """
        解析JSON字符串
        
        Args:
            json_str: JSON字符串
            
        Returns:
            解析后的字典
        """
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON解析失败: {str(e)}")
            return {}


class CollectorFactory:
    """采集器工厂"""
    
    _collectors = {}
    
    @classmethod
    def register(cls, name: str, collector_class):
        """注册采集器类"""
        cls._collectors[name] = collector_class
    
    @classmethod
    def create(cls, name: str, config: Dict[str, Any]) -> Optional[BaseCollector]:
        """创建采集器实例"""
        if name not in cls._collectors:
            logging.error(f"未知的采集器类型: {name}")
            return None
        
        collector_class = cls._collectors[name]
        return collector_class(name, config)
    
    @classmethod
    def get_available_collectors(cls) -> List[str]:
        """获取可用的采集器列表"""
        return list(cls._collectors.keys())


# 示例采集器实现
class ExampleCollector(BaseCollector):
    """示例采集器"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name, config)
        self.api_url = config.get("api_url", "")
        self.api_key = config.get("api_key", "")
    
    async def collect(self) -> List[CollectedItem]:
        """示例采集实现"""
        items = []
        
        # 模拟采集数据
        for i in range(3):
            item = CollectedItem(
                source=self.name,
                source_type="example",
                title=f"示例项目 {i+1}",
                content=f"这是来自 {self.name} 的示例内容 {i+1}",
                url=f"https://example.com/item/{i+1}",
                author="示例作者",
                published_at=datetime.now(),
                metadata={"index": i, "source": self.name}
            )
            items.append(item)
        
        return items
    
    def validate_config(self) -> bool:
        """验证配置"""
        if not self.api_url:
            self.logger.warning(f"{self.name}: api_url 未配置")
            return False
        return True


# 注册示例采集器
CollectorFactory.register("example", ExampleCollector)