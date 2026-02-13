#!/usr/bin/env python3
"""
智能模型选择系统
优先使用本地Ollama模型，失败时回退到API
"""

import requests
import json
import time
import logging
from typing import Optional, Dict, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SmartModelSelector:
    """智能模型选择器"""
    
    def __init__(self):
        self.config = self.load_config()
        self.local_model_available = self.check_local_model()
        
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open('local_model_config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # 默认配置
            return {
                "model": "ollama/qwen2.5:1.5b-instruct",
                "apiBase": "http://localhost:11434/v1",
                "fallbackModel": "deepseek/deepseek-chat",
                "maxTokens": 2048,
                "temperature": 0.7,
                "timeout": 30000,
                "retryCount": 2
            }
    
    def check_local_model(self) -> bool:
        """检查本地模型是否可用"""
        try:
            response = requests.get(
                "http://localhost:11434/api/tags",
                timeout=5
            )
            if response.status_code == 200:
                models = response.json().get("models", [])
                target_model = self.config["model"].split("/")[-1]
                for model in models:
                    if target_model in model.get("name", ""):
                        logger.info(f"✅ 本地模型可用: {model.get('name')}")
                        return True
                logger.warning(f"⚠️ 本地模型 {target_model} 未找到")
            return False
        except Exception as e:
            logger.warning(f"❌ 本地模型检查失败: {e}")
            return False
    
    def generate_with_local(self, prompt: str) -> Optional[str]:
        """使用本地模型生成"""
        if not self.local_model_available:
            return None
        
        try:
            payload = {
                "model": self.config["model"].split("/")[-1],
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": self.config.get("maxTokens", 2048),
                    "temperature": self.config.get("temperature", 0.7)
                }
            }
            
            response = requests.post(
                f"{self.config['apiBase'].replace('/v1', '')}/api/generate",
                json=payload,
                timeout=self.config.get("timeout", 30)
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                logger.error(f"本地模型请求失败: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            logger.warning("本地模型请求超时")
            return None
        except Exception as e:
            logger.error(f"本地模型生成错误: {e}")
            return None
    
    def generate_with_fallback(self, prompt: str) -> str:
        """智能生成：先尝试本地，失败则使用回退"""
        logger.info(f"📝 处理请求: {prompt[:50]}...")
        
        # 先尝试本地模型
        if self.local_model_available:
            logger.info("🔄 尝试使用本地模型...")
            local_result = self.generate_with_local(prompt)
            if local_result:
                logger.info("✅ 本地模型生成成功")
                return local_result
            else:
                logger.warning("⚠️ 本地模型失败，切换到API")
        
        # 使用回退模型（这里需要实际的API调用）
        logger.info(f"🔄 使用回退模型: {self.config['fallbackModel']}")
        # 实际实现中，这里会调用相应的API
        # 暂时返回模拟响应
        return f"[使用API模型 {self.config['fallbackModel']}] 这是模拟响应。实际会调用相应API。"
    
    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        info = {
            "local_available": self.local_model_available,
            "local_model": self.config["model"],
            "fallback_model": self.config["fallbackModel"],
            "strategy": "local-first"
        }
        
        if self.local_model_available:
            try:
                response = requests.get(
                    "http://localhost:11434/api/tags",
                    timeout=5
                )
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    if models:
                        info["local_model_details"] = models[0]
            except:
                pass
        
        return info

def test_model_selector():
    """测试模型选择器"""
    print("🧪 测试智能模型选择系统...")
    
    selector = SmartModelSelector()
    
    # 显示模型信息
    info = selector.get_model_info()
    print(f"📊 模型信息:")
    print(f"   本地模型可用: {info['local_available']}")
    print(f"   本地模型: {info['local_model']}")
    print(f"   回退模型: {info['fallback_model']}")
    print(f"   策略: {info['strategy']}")
    
    # 测试生成
    test_prompt = "你好，请介绍一下你自己"
    print(f"\n📝 测试提示: {test_prompt}")
    
    result = selector.generate_with_fallback(test_prompt)
    print(f"📄 生成结果: {result}")
    
    return selector

if __name__ == "__main__":
    selector = test_model_selector()
    print("\n🎉 智能模型选择系统测试完成！")