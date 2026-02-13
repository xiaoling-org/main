"""
GitHub数据采集器
采集GitHub Trending Repositories和热门项目
"""

import logging
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

from .base_collector import BaseCollector, CollectedItem, CollectorFactory


class GitHubCollector(BaseCollector):
    """GitHub数据采集器"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name, config)
        
        # GitHub配置
        self.api_token = config.get("api_token", "")
        self.languages = config.get("languages", ["python", "javascript", "java", "go", "rust"])
        self.max_repositories = config.get("repositories", 50)
        
        # API端点
        self.base_url = "https://api.github.com"
        self.trending_url = "https://github.com/trending"
        
        # 请求头
        self.headers = {
            "User-Agent": "GlobalOpportunityMonitor/1.0",
            "Accept": "application/vnd.github.v3+json"
        }
        
        if self.api_token:
            self.headers["Authorization"] = f"token {self.api_token}"
    
    async def collect(self) -> List[CollectedItem]:
        """采集GitHub数据"""
        items = []
        
        try:
            # 1. 采集Trending Repositories
            trending_items = await self._collect_trending_repositories()
            items.extend(trending_items)
            
            # 2. 按语言采集热门项目
            for language in self.languages[:3]:  # 限制前3种语言
                try:
                    language_items = await self._collect_by_language(language)
                    items.extend(language_items)
                    time.sleep(1)  # 避免请求过快
                except Exception as e:
                    self.logger.error(f"采集语言 {language} 失败: {str(e)}")
            
            self.logger.info(f"GitHub采集完成，共采集 {len(items)} 个项目")
            
        except Exception as e:
            self.logger.error(f"GitHub采集失败: {str(e)}", exc_info=True)
        
        return items
    
    async def _collect_trending_repositories(self) -> List[CollectedItem]:
        """采集Trending Repositories"""
        items = []
        
        try:
            # 注意：GitHub Trending没有官方API，这里使用简化实现
            # 实际项目中可能需要使用web scraping或第三方API
            
            # 模拟数据
            trending_repos = [
                {
                    "name": "example-repo-1",
                    "description": "一个创新的AI项目，使用最新的Transformer架构",
                    "url": "https://github.com/user/example-repo-1",
                    "language": "Python",
                    "stars": 1500,
                    "forks": 300,
                    "stars_today": 150
                },
                {
                    "name": "example-repo-2",
                    "description": "下一代Web框架，性能提升50%",
                    "url": "https://github.com/user/example-repo-2",
                    "language": "JavaScript",
                    "stars": 2500,
                    "forks": 500,
                    "stars_today": 200
                },
                {
                    "name": "example-repo-3",
                    "description": "区块链智能合约安全审计工具",
                    "url": "https://github.com/user/example-repo-3",
                    "language": "Solidity",
                    "stars": 800,
                    "forks": 150,
                    "stars_today": 80
                }
            ]
            
            for repo in trending_repos:
                item = CollectedItem(
                    source="github",
                    source_type="github_trending",
                    title=repo["name"],
                    content=repo["description"],
                    url=repo["url"],
                    author=repo["url"].split("/")[-2],  # 提取用户名
                    published_at=datetime.now() - timedelta(days=1),  # 假设是昨天发布的
                    metadata={
                        "language": repo["language"],
                        "stars": repo["stars"],
                        "forks": repo["forks"],
                        "stars_today": repo["stars_today"],
                        "trending": True
                    }
                )
                items.append(item)
            
            self.logger.info(f"采集到 {len(items)} 个Trending仓库")
            
        except Exception as e:
            self.logger.error(f"采集Trending仓库失败: {str(e)}")
        
        return items
    
    async def _collect_by_language(self, language: str) -> List[CollectedItem]:
        """按语言采集热门项目"""
        items = []
        
        try:
            # 模拟按语言搜索热门项目
            # 实际项目中使用GitHub Search API: /search/repositories?q=language:{language}&sort=stars&order=desc
            
            language_repos = [
                {
                    "name": f"{language}-project-1",
                    "description": f"使用{language}开发的高性能计算框架",
                    "url": f"https://github.com/user/{language}-project-1",
                    "stars": 1000,
                    "forks": 200,
                    "updated_at": (datetime.now() - timedelta(days=2)).isoformat()
                },
                {
                    "name": f"{language}-project-2",
                    "description": f"基于{language}的机器学习库",
                    "url": f"https://github.com/user/{language}-project-2",
                    "stars": 800,
                    "forks": 150,
                    "updated_at": (datetime.now() - timedelta(days=5)).isoformat()
                }
            ]
            
            for repo in language_repos:
                item = CollectedItem(
                    source="github",
                    source_type="github_language",
                    title=repo["name"],
                    content=repo["description"],
                    url=repo["url"],
                    author=repo["url"].split("/")[-2],
                    published_at=datetime.fromisoformat(repo["updated_at"].replace("Z", "+00:00")),
                    metadata={
                        "language": language,
                        "stars": repo["stars"],
                        "forks": repo["forks"],
                        "language_specific": True
                    }
                )
                items.append(item)
            
            self.logger.info(f"采集到 {len(items)} 个{language}语言项目")
            
        except Exception as e:
            self.logger.error(f"采集{language}语言项目失败: {str(e)}")
        
        return items
    
    async def _search_repositories(self, query: str, sort: str = "stars", order: str = "desc") -> List[Dict[str, Any]]:
        """搜索GitHub仓库（简化实现）"""
        # 实际实现应该调用GitHub Search API
        # 这里返回模拟数据
        
        self.logger.debug(f"搜索仓库: query={query}, sort={sort}, order={order}")
        
        # 模拟API响应
        return [
            {
                "name": "search-result-1",
                "description": f"搜索结果1: {query}",
                "html_url": "https://github.com/user/search-result-1",
                "language": "Python",
                "stargazers_count": 500,
                "forks_count": 100,
                "updated_at": "2024-01-15T10:30:00Z"
            }
        ]
    
    def validate_config(self) -> bool:
        """验证配置"""
        # GitHub采集器不需要强制配置API token
        # 有token可以享受更高的API限制，没有token也能工作
        
        if not self.languages:
            self.logger.warning("未配置编程语言列表，使用默认值")
            self.languages = ["python", "javascript", "java"]
        
        if self.max_repositories <= 0:
            self.logger.warning(f"无效的仓库数量: {self.max_repositories}，使用默认值50")
            self.max_repositories = 50
        
        return True
    
    def get_status(self) -> Dict[str, Any]:
        """获取采集器状态"""
        status = super().get_status()
        status.update({
            "api_token_configured": bool(self.api_token),
            "languages": self.languages,
            "max_repositories": self.max_repositories
        })
        return status


# 注册GitHub采集器
CollectorFactory.register("github", GitHubCollector)