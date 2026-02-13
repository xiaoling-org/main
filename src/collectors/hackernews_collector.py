"""
Hacker News数据采集器
采集Hacker News热门故事和最新文章
"""

import logging
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

from .base_collector import BaseCollector, CollectedItem, CollectorFactory


class HackerNewsCollector(BaseCollector):
    """Hacker News数据采集器"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name, config)
        
        # Hacker News配置
        self.top_stories_count = config.get("top_stories", 30)
        self.base_url = "https://hacker-news.firebaseio.com/v0"
        
        # 请求头
        self.headers = {
            "User-Agent": "GlobalOpportunityMonitor/1.0",
            "Accept": "application/json"
        }
    
    async def collect(self) -> List[CollectedItem]:
        """采集Hacker News数据"""
        items = []
        
        try:
            # 1. 采集Top Stories
            top_stories = await self._get_top_stories()
            
            # 2. 获取每个故事的详细信息
            for story_id in top_stories[:self.top_stories_count]:
                try:
                    story_item = await self._get_item_details(story_id)
                    if story_item and self._is_valid_story(story_item):
                        collected_item = self._convert_to_collected_item(story_item)
                        items.append(collected_item)
                    
                    time.sleep(0.1)  # 避免请求过快
                    
                except Exception as e:
                    self.logger.error(f"获取故事 {story_id} 详情失败: {str(e)}")
            
            self.logger.info(f"Hacker News采集完成，共采集 {len(items)} 个故事")
            
        except Exception as e:
            self.logger.error(f"Hacker News采集失败: {str(e)}", exc_info=True)
        
        return items
    
    async def _get_top_stories(self) -> List[int]:
        """获取Top Stories ID列表"""
        try:
            # 模拟API调用
            # 实际实现: response = requests.get(f"{self.base_url}/topstories.json", headers=self.headers)
            
            self.logger.debug("获取Top Stories列表")
            
            # 模拟数据
            return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 简化示例
            
        except Exception as e:
            self.logger.error(f"获取Top Stories失败: {str(e)}")
            return []
    
    async def _get_item_details(self, item_id: int) -> Optional[Dict[str, Any]]:
        """获取项目详细信息"""
        try:
            # 模拟API调用
            # 实际实现: response = requests.get(f"{self.base_url}/item/{item_id}.json", headers=self.headers)
            
            self.logger.debug(f"获取项目详情: {item_id}")
            
            # 根据ID生成模拟数据
            stories = {
                1: {
                    "id": 1,
                    "type": "story",
                    "title": "新的AI模型在代码生成任务上超越GPT-4",
                    "url": "https://example.com/ai-model-beats-gpt4",
                    "text": "研究人员开发了一种新的AI模型，在代码生成任务上表现优于GPT-4...",
                    "by": "ai_researcher",
                    "time": int(time.time()) - 3600,  # 1小时前
                    "score": 450,
                    "descendants": 120
                },
                2: {
                    "id": 2,
                    "type": "story",
                    "title": "量子计算突破：实现100量子比特系统",
                    "url": "https://example.com/quantum-computing-breakthrough",
                    "text": "科学家宣布在量子计算领域取得重大突破...",
                    "by": "quantum_scientist",
                    "time": int(time.time()) - 7200,  # 2小时前
                    "score": 380,
                    "descendants": 85
                },
                3: {
                    "id": 3,
                    "type": "story",
                    "title": "新的编程语言Zig 1.0发布",
                    "url": "https://example.com/zig-1.0-released",
                    "text": "Zig编程语言发布了1.0版本，带来了许多改进和新特性...",
                    "by": "zig_dev",
                    "time": int(time.time()) - 10800,  # 3小时前
                    "score": 320,
                    "descendants": 65
                },
                4: {
                    "id": 4,
                    "type": "story",
                    "title": "WebAssembly在边缘计算中的应用",
                    "url": "https://example.com/webassembly-edge-computing",
                    "text": "WebAssembly正在改变边缘计算的格局...",
                    "by": "webassembly_fan",
                    "time": int(time.time()) - 14400,  # 4小时前
                    "score": 280,
                    "descendants": 45
                },
                5: {
                    "id": 5,
                    "type": "story",
                    "title": "开源数据库性能基准测试2024",
                    "url": "https://example.com/database-benchmark-2024",
                    "text": "最新的开源数据库性能基准测试结果发布...",
                    "by": "db_enthusiast",
                    "time": int(time.time()) - 18000,  # 5小时前
                    "score": 240,
                    "descendants": 35
                }
            }
            
            return stories.get(item_id, None)
            
        except Exception as e:
            self.logger.error(f"获取项目 {item_id} 详情失败: {str(e)}")
            return None
    
    def _is_valid_story(self, story: Dict[str, Any]) -> bool:
        """检查故事是否有效"""
        if not story:
            return False
        
        # 检查必需字段
        required_fields = ["id", "type", "title"]
        for field in required_fields:
            if field not in story:
                return False
        
        # 只处理story类型
        if story.get("type") != "story":
            return False
        
        # 检查是否有内容
        if not story.get("title") and not story.get("text"):
            return False
        
        return True
    
    def _convert_to_collected_item(self, story: Dict[str, Any]) -> CollectedItem:
        """将Hacker News故事转换为CollectedItem"""
        
        # 发布时间
        published_at = datetime.fromtimestamp(story.get("time", time.time()))
        
        # 内容
        content = story.get("text", "")
        if not content:
            content = story.get("title", "")
        
        # URL
        url = story.get("url", "")
        if not url:
            url = f"https://news.ycombinator.com/item?id={story['id']}"
        
        # 元数据
        metadata = {
            "hn_id": story["id"],
            "score": story.get("score", 0),
            "comments": story.get("descendants", 0),
            "author": story.get("by", ""),
            "type": story.get("type", "story")
        }
        
        item = CollectedItem(
            source="hackernews",
            source_type="hackernews_story",
            title=story["title"],
            content=content,
            url=url,
            author=story.get("by"),
            published_at=published_at,
            metadata=metadata,
            raw_data=story
        )
        
        return item
    
    async def _search_stories(self, query: str) -> List[Dict[str, Any]]:
        """搜索Hacker News故事（简化实现）"""
        # 注意：Hacker News没有官方搜索API
        # 实际项目中可能需要使用Algolia的HN搜索API
        
        self.logger.debug(f"搜索故事: {query}")
        
        # 模拟搜索结果
        return [
            {
                "id": 100,
                "title": f"搜索结果: {query}",
                "url": f"https://example.com/search/{query}",
                "points": 50,
                "author": "search_user",
                "created_at": datetime.now().isoformat()
            }
        ]
    
    def validate_config(self) -> bool:
        """验证配置"""
        if self.top_stories_count <= 0:
            self.logger.warning(f"无效的故事数量: {self.top_stories_count}，使用默认值30")
            self.top_stories_count = 30
        
        if self.top_stories_count > 100:
            self.logger.warning(f"故事数量过多: {self.top_stories_count}，限制为100")
            self.top_stories_count = 100
        
        return True
    
    def get_status(self) -> Dict[str, Any]:
        """获取采集器状态"""
        status = super().get_status()
        status.update({
            "top_stories_count": self.top_stories_count,
            "base_url": self.base_url
        })
        return status


# 注册Hacker News采集器
CollectorFactory.register("hackernews", HackerNewsCollector)