"""
新闻数据采集器
采集科技新闻和商业新闻
"""

import logging
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
from urllib.parse import urlparse

from .base_collector import BaseCollector, CollectedItem, CollectorFactory


class NewsCollector(BaseCollector):
    """新闻数据采集器"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name, config)
        
        # 新闻源配置
        self.sources = config.get("sources", [
            "https://techcrunch.com/feed/",
            "https://news.ycombinator.com/rss"
        ])
        
        self.max_articles_per_source = config.get("max_articles", 20)
        self.api_key = config.get("api_key", "")
        
        # 请求头
        self.headers = {
            "User-Agent": "GlobalOpportunityMonitor/1.0 (News Collector)",
            "Accept": "application/xml, application/json, text/html"
        }
        
        # 新闻源映射
        self.source_names = {
            "techcrunch.com": "TechCrunch",
            "news.ycombinator.com": "Hacker News RSS",
            "scmp.com": "South China Morning Post",
            "hk01.com": "HK01",
            "bbc.com": "BBC News",
            "reuters.com": "Reuters"
        }
    
    async def collect(self) -> List[CollectedItem]:
        """采集新闻数据"""
        items = []
        
        try:
            # 遍历所有新闻源
            for source_url in self.sources:
                try:
                    source_items = await self._collect_from_source(source_url)
                    items.extend(source_items)
                    
                    self.logger.info(f"从 {source_url} 采集到 {len(source_items)} 篇文章")
                    time.sleep(1)  # 避免请求过快
                    
                except Exception as e:
                    self.logger.error(f"采集新闻源 {source_url} 失败: {str(e)}")
            
            self.logger.info(f"新闻采集完成，共采集 {len(items)} 篇文章")
            
        except Exception as e:
            self.logger.error(f"新闻采集失败: {str(e)}", exc_info=True)
        
        return items
    
    async def _collect_from_source(self, source_url: str) -> List[CollectedItem]:
        """从单个新闻源采集数据"""
        items = []
        
        try:
            # 解析域名
            domain = urlparse(source_url).netloc
            
            # 获取源名称
            source_name = self.source_names.get(domain, domain)
            
            # 检查是否是RSS源
            if source_url.endswith(".rss") or source_url.endswith("/feed") or "rss" in source_url:
                rss_items = await self._parse_rss_feed(source_url, source_name)
                items.extend(rss_items[:self.max_articles_per_source])
            
            # 检查是否是API端点
            elif "api" in source_url:
                api_items = await self._fetch_from_api(source_url, source_name)
                items.extend(api_items[:self.max_articles_per_source])
            
            # 否则尝试解析HTML
            else:
                html_items = await self._parse_website(source_url, source_name)
                items.extend(html_items[:self.max_articles_per_source])
            
        except Exception as e:
            self.logger.error(f"处理新闻源 {source_url} 失败: {str(e)}")
        
        return items
    
    async def _parse_rss_feed(self, feed_url: str, source_name: str) -> List[CollectedItem]:
        """解析RSS订阅源"""
        items = []
        
        try:
            # 模拟RSS解析
            # 实际实现应该使用feedparser库
            
            self.logger.debug(f"解析RSS订阅源: {feed_url}")
            
            # 模拟RSS数据
            rss_items = [
                {
                    "title": "AI芯片公司发布新一代处理器",
                    "description": "一家AI芯片初创公司发布了新一代处理器，性能提升3倍...",
                    "link": "https://techcrunch.com/ai-chip-new-processor",
                    "published": (datetime.now() - timedelta(hours=2)).isoformat(),
                    "author": "Tech Reporter"
                },
                {
                    "title": "电动汽车销量在2024年第一季度增长40%",
                    "description": "全球电动汽车销量持续增长，中国品牌表现突出...",
                    "link": "https://techcrunch.com/ev-sales-growth-2024",
                    "published": (datetime.now() - timedelta(hours=5)).isoformat(),
                    "author": "Auto Analyst"
                },
                {
                    "title": "量子加密技术取得突破",
                    "description": "研究人员在量子加密领域取得重要突破，提升网络安全...",
                    "link": "https://techcrunch.com/quantum-encryption-breakthrough",
                    "published": (datetime.now() - timedelta(hours=8)).isoformat(),
                    "author": "Security Expert"
                }
            ]
            
            for rss_item in rss_items:
                try:
                    # 发布时间
                    published_at = datetime.fromisoformat(rss_item["published"].replace("Z", "+00:00"))
                    
                    # 内容
                    content = rss_item.get("description", rss_item["title"])
                    
                    item = CollectedItem(
                        source=source_name,
                        source_type="news_rss",
                        title=rss_item["title"],
                        content=content,
                        url=rss_item["link"],
                        author=rss_item.get("author"),
                        published_at=published_at,
                        metadata={
                            "feed_url": feed_url,
                            "source_type": "rss",
                            "domain": urlparse(feed_url).netloc
                        }
                    )
                    items.append(item)
                    
                except Exception as e:
                    self.logger.error(f"解析RSS项目失败: {str(e)}")
            
            self.logger.debug(f"从RSS订阅源解析到 {len(items)} 篇文章")
            
        except Exception as e:
            self.logger.error(f"解析RSS订阅源失败: {str(e)}")
        
        return items
    
    async def _fetch_from_api(self, api_url: str, source_name: str) -> List[CollectedItem]:
        """从API获取新闻"""
        items = []
        
        try:
            # 模拟API调用
            # 实际实现应该使用requests库
            
            self.logger.debug(f"从API获取新闻: {api_url}")
            
            # 模拟API响应
            api_data = {
                "articles": [
                    {
                        "title": "科技巨头发布2024年第一季度财报",
                        "content": "多家科技公司发布了2024年第一季度财报，表现超出预期...",
                        "url": "https://newsapi.org/article/tech-earnings-2024-q1",
                        "author": "Financial Reporter",
                        "publishedAt": (datetime.now() - timedelta(hours=1)).isoformat(),
                        "source": {"name": source_name}
                    },
                    {
                        "title": "初创公司获得1亿美元融资",
                        "description": "一家AI初创公司成功获得1亿美元B轮融资...",
                        "url": "https://newsapi.org/article/startup-funding-100m",
                        "author": "VC Analyst",
                        "publishedAt": (datetime.now() - timedelta(hours=3)).isoformat(),
                        "source": {"name": source_name}
                    }
                ]
            }
            
            for article in api_data.get("articles", []):
                try:
                    # 发布时间
                    published_str = article.get("publishedAt", "")
                    if published_str:
                        published_at = datetime.fromisoformat(published_str.replace("Z", "+00:00"))
                    else:
                        published_at = datetime.now() - timedelta(days=1)
                    
                    # 内容
                    content = article.get("content", article.get("description", article["title"]))
                    
                    item = CollectedItem(
                        source=source_name,
                        source_type="news_api",
                        title=article["title"],
                        content=content,
                        url=article["url"],
                        author=article.get("author"),
                        published_at=published_at,
                        metadata={
                            "api_url": api_url,
                            "source_type": "api",
                            "api_provider": "newsapi" if "newsapi" in api_url else "custom"
                        }
                    )
                    items.append(item)
                    
                except Exception as e:
                    self.logger.error(f"解析API文章失败: {str(e)}")
            
            self.logger.debug(f"从API获取到 {len(items)} 篇文章")
            
        except Exception as e:
            self.logger.error(f"API调用失败: {str(e)}")
        
        return items
    
    async def _parse_website(self, website_url: str, source_name: str) -> List[CollectedItem]:
        """解析网站HTML"""
        items = []
        
        try:
            # 模拟网页解析
            # 实际实现应该使用BeautifulSoup
            
            self.logger.debug(f"解析网站: {website_url}")
            
            # 模拟网页内容
            website_articles = [
                {
                    "title": "全球科技趋势2024报告发布",
                    "summary": "最新发布的全球科技趋势报告揭示了2024年的关键发展方向...",
                    "url": f"{website_url}/global-tech-trends-2024",
                    "date": "2024-01-15",
                    "author": "Research Team"
                },
                {
                    "title": "数字化转型加速企业创新",
                    "summary": "越来越多的企业通过数字化转型提升竞争力...",
                    "url": f"{website_url}/digital-transformation-innovation",
                    "date": "2024-01-14",
                    "author": "Business Analyst"
                }
            ]
            
            for article in website_articles:
                try:
                    # 发布时间
                    published_at = datetime.strptime(article["date"], "%Y-%m-%d")
                    
                    item = CollectedItem(
                        source=source_name,
                        source_type="news_website",
                        title=article["title"],
                        content=article["summary"],
                        url=article["url"],
                        author=article.get("author"),
                        published_at=published_at,
                        metadata={
                            "website_url": website_url,
                            "source_type": "website",
                            "parsing_method": "html"
                        }
                    )
                    items.append(item)
                    
                except Exception as e:
                    self.logger.error(f"解析网页文章失败: {str(e)}")
            
            self.logger.debug(f"从网站解析到 {len(items)} 篇文章")
            
        except Exception as e:
            self.logger.error(f"解析网站失败: {str(e)}")
        
        return items
    
    def validate_config(self) -> bool:
        """验证配置"""
        if not self.sources:
            self.logger.warning("未配置新闻源，使用默认源")
            self.sources = [
                "https://techcrunch.com/feed/",
                "https://news.ycombinator.com/rss"
            ]
        
        # 验证URL格式
        valid_sources = []
        for source in self.sources:
            try:
                result = urlparse(source)
                if result.scheme and result.netloc:
                    valid_sources.append(source)
                else:
                    self.logger.warning(f"无效的新闻源URL: {source}")
            except:
                self.logger.warning(f"无法解析新闻源URL: {source}")
        
        self.sources = valid_sources
        
        if not self.sources:
            self.logger.error("没有有效的新闻源配置")
            return False
        
        if self.max_articles_per_source <= 0:
            self.logger.warning(f"无效的文章数量: {self.max_articles_per_source}，使用默认值20")
            self.max_articles_per_source = 20
        
        return True
    
    def get_status(self) -> Dict[str, Any]:
        """获取采集器状态"""
        status = super().get_status()
        status.update({
            "sources_count": len(self.sources),
            "sources": self.sources[:3],  # 只显示前3个
            "max_articles_per_source": self.max_articles_per_source,
            "api_key_configured": bool(self.api_key)
        })
        return status


# 注册新闻采集器
CollectorFactory.register("news", NewsCollector)