"""
数据准确性框架
确保所有数据都经过验证和交叉检查
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataAccuracyFramework:
    """数据准确性框架"""
    
    def __init__(self):
        # 数据验证配置
        self.validation_config = {
            'financial_data': {
                'min_sources': 2,
                'consistency_threshold': 0.95,  # 95%一致性
                'max_age_minutes': 5,
                'required_checks': ['source', 'time', 'consistency', 'logic']
            },
            'general_data': {
                'min_sources': 2,
                'consistency_threshold': 0.90,
                'max_age_minutes': 60,
                'required_checks': ['source', 'consistency']
            },
            'technical_data': {
                'min_sources': 1,
                'consistency_threshold': 0.98,
                'max_age_minutes': 1440,  # 24小时
                'required_checks': ['source', 'logic']
            }
        }
        
        # 数据验证记录
        self.validation_logs = []
        
        # 可信数据源列表
        self.trusted_sources = {
            'financial': [
                'yahoo_finance',
                'investing_com',
                'bloomberg',
                'reuters',
                'wsj'
            ],
            'general': [
                'wikipedia',
                'official_government',
                'academic_journals',
                'reputable_news'
            ],
            'technical': [
                'official_docs',
                'github',
                'stackoverflow',
                'technical_blogs'
            ]
        }
    
    def validate_financial_data(self, data_points: List[Dict[str, Any]]) -> Dict[str, Any]:
        """验证金融数据"""
        logger.info(f"验证金融数据，共{len(data_points)}个数据点")
        
        validation_result = {
            'data_type': 'financial',
            'timestamp': datetime.now().isoformat(),
            'sources_count': len(data_points),
            'validation_passed': False,
            'confidence_score': 0.0,
            'issues': [],
            'validated_data': None
        }
        
        # 检查数据源数量
        if len(data_points) < self.validation_config['financial_data']['min_sources']:
            validation_result['issues'].append(f"数据源不足: {len(data_points)}个，需要至少{self.validation_config['financial_data']['min_sources']}个")
            return validation_result
        
        # 提取价格数据
        prices = []
        for point in data_points:
            if 'price' in point:
                prices.append(point['price'])
            elif 'value' in point:
                prices.append(point['value'])
        
        if not prices:
            validation_result['issues'].append("没有找到价格数据")
            return validation_result
        
        # 计算一致性
        if len(prices) >= 2:
            avg_price = sum(prices) / len(prices)
            deviations = [abs(price - avg_price) / avg_price for price in prices]
            consistency = 1 - (sum(deviations) / len(deviations))
            
            validation_result['consistency_score'] = consistency
            
            if consistency >= self.validation_config['financial_data']['consistency_threshold']:
                validation_result['confidence_score'] = consistency * 100
            else:
                validation_result['issues'].append(f"数据一致性不足: {consistency:.2%}，要求{self.validation_config['financial_data']['consistency_threshold']:.2%}")
        else:
            validation_result['issues'].append("数据点不足，无法计算一致性")
        
        # 检查数据时效性
        current_time = datetime.now()
        for i, point in enumerate(data_points):
            if 'timestamp' in point:
                try:
                    data_time = datetime.fromisoformat(point['timestamp'].replace('Z', '+00:00'))
                    age_minutes = (current_time - data_time).total_seconds() / 60
                    
                    if age_minutes > self.validation_config['financial_data']['max_age_minutes']:
                        validation_result['issues'].append(f"数据源{i+1}过时: {age_minutes:.1f}分钟前")
                except:
                    validation_result['issues'].append(f"数据源{i+1}时间格式无效")
        
        # 逻辑检查（金融数据特定）
        if prices:
            avg_price = sum(prices) / len(prices)
            
            # 检查价格合理性
            if avg_price <= 0:
                validation_result['issues'].append("价格数据不合理（非正数）")
            
            # 检查波动性（如果有多时间点数据）
            if len(prices) > 1:
                price_range = max(prices) - min(prices)
                if price_range / avg_price > 0.5:  # 波动超过50%
                    validation_result['issues'].append(f"价格波动过大: {price_range/avg_price:.1%}")
        
        # 确定验证结果
        if not validation_result['issues']:
            validation_result['validation_passed'] = True
            validation_result['confidence_score'] = min(100, validation_result.get('consistency_score', 0) * 100)
            
            # 计算验证后的数据
            if prices:
                validation_result['validated_data'] = {
                    'value': sum(prices) / len(prices),
                    'range': f"{min(prices):.2f}-{max(prices):.2f}",
                    'sources': len(data_points),
                    'confidence': validation_result['confidence_score']
                }
        
        # 记录验证日志
        self.validation_logs.append(validation_result)
        
        return validation_result
    
    def validate_general_data(self, data_points: List[Dict[str, Any]]) -> Dict[str, Any]:
        """验证一般数据"""
        logger.info(f"验证一般数据，共{len(data_points)}个数据点")
        
        validation_result = {
            'data_type': 'general',
            'timestamp': datetime.now().isoformat(),
            'sources_count': len(data_points),
            'validation_passed': False,
            'confidence_score': 0.0,
            'issues': [],
            'validated_data': None
        }
        
        # 简化的一般数据验证逻辑
        if len(data_points) >= self.validation_config['general_data']['min_sources']:
            # 检查数据一致性
            values = []
            for point in data_points:
                if 'value' in point:
                    values.append(str(point['value']).lower())
                elif 'text' in point:
                    values.append(str(point['text']).lower())
            
            if values:
                # 简单的一致性检查：多数一致
                from collections import Counter
                value_counts = Counter(values)
                most_common = value_counts.most_common(1)
                
                if most_common:
                    most_common_value, count = most_common[0]
                    consistency = count / len(values)
                    
                    if consistency >= self.validation_config['general_data']['consistency_threshold']:
                        validation_result['validation_passed'] = True
                        validation_result['confidence_score'] = consistency * 100
                        validation_result['validated_data'] = {
                            'value': most_common_value,
                            'consistency': consistency,
                            'sources': len(data_points)
                        }
                    else:
                        validation_result['issues'].append(f"数据一致性不足: {consistency:.2%}")
        
        self.validation_logs.append(validation_result)
        return validation_result
    
    def get_data_with_validation(self, data_type: str, data_points: List[Dict[str, Any]]) -> Dict[str, Any]:
        """获取经过验证的数据"""
        logger.info(f"获取{data_type}类型数据，进行验证")
        
        if data_type == 'financial':
            validation_result = self.validate_financial_data(data_points)
        elif data_type == 'general':
            validation_result = self.validate_general_data(data_points)
        else:
            validation_result = {
                'data_type': data_type,
                'validation_passed': False,
                'error': f"不支持的数据类型: {data_type}"
            }
        
        # 生成数据报告
        report = {
            'data_type': data_type,
            'validation_result': validation_result['validation_passed'],
            'confidence_score': validation_result.get('confidence_score', 0),
            'timestamp': datetime.now().isoformat(),
            'data_hash': hashlib.md5(str(data_points).encode()).hexdigest()[:8]
        }
        
        if validation_result['validation_passed']:
            report['status'] = 'VALIDATED'
            report['data'] = validation_result['validated_data']
            report['message'] = f"数据验证通过，置信度{validation_result['confidence_score']:.1f}%"
        else:
            report['status'] = 'FAILED'
            report['issues'] = validation_result.get('issues', [])
            report['message'] = f"数据验证失败: {', '.join(validation_result.get('issues', ['未知错误']))}"
        
        return report
    
    def log_validation(self, data_type: str, result: Dict[str, Any]):
        """记录验证日志"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'data_type': data_type,
            'result': result,
            'log_id': hashlib.md5(str(result).encode()).hexdigest()[:12]
        }
        
        self.validation_logs.append(log_entry)
        
        # 保持日志数量可控
        if len(self.validation_logs) > 1000:
            self.validation_logs = self.validation_logs[-1000:]
        
        return log_entry
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """获取验证统计摘要"""
        if not self.validation_logs:
            return {'total_validations': 0}
        
        total = len(self.validation_logs)
        passed = sum(1 for log in self.validation_logs 
                    if isinstance(log, dict) and log.get('validation_result', {}).get('validation_passed', False))
        
        financial_logs = [log for log in self.validation_logs 
                         if isinstance(log, dict) and log.get('data_type') == 'financial']
        general_logs = [log for log in self.validation_logs 
                       if isinstance(log, dict) and log.get('data_type') == 'general']
        
        return {
            'total_validations': total,
            'passed_validations': passed,
            'failure_rate': (total - passed) / total * 100 if total > 0 else 0,
            'by_type': {
                'financial': len(financial_logs),
                'general': len(general_logs)
            },
            'latest_validation': self.validation_logs[-1] if self.validation_logs else None
        }
    
    def clear_validation_logs(self):
        """清空验证日志"""
        self.validation_logs = []
        logger.info("验证日志已清空")

# 全局数据准确性框架实例
data_accuracy = DataAccuracyFramework()

def ensure_data_accuracy(data_type: str, data_points: List[Dict[str, Any]], 
                        require_validation: bool = True) -> Dict[str, Any]:
    """
    确保数据准确性的装饰器函数
    
    参数:
        data_type: 数据类型 (financial, general, technical)
        data_points: 数据点列表
        require_validation: 是否要求验证通过
    
    返回:
        验证后的数据报告
    """
    logger.info(f"确保{data_type}数据准确性")
    
    # 获取验证结果
    validation_report = data_accuracy.get_data_with_validation(data_type, data_points)
    
    if require_validation and not validation_report['validation_result']:
        logger.warning(f"数据验证失败: {validation_report.get('message', '未知错误')}")
        
        # 对于金融数据，验证失败是严重问题
        if data_type == 'financial':
            raise ValueError(f"金融数据验证失败: {validation_report.get('message', '请检查数据源')}")
    
    return validation_report

# 使用示例
if __name__ == "__main__":
    # 示例：验证金融数据
    sample_financial_data = [
        {'source': 'yahoo', 'price': 27450.25, 'timestamp': '2026-02-11T07:00:00Z'},
        {'source': 'investing', 'price': 27452.80, 'timestamp': '2026-02-11T07:01:00Z'},
        {'source': 'bloomberg', 'price': 27448.90, 'timestamp': '2026-02-11T07:02:00Z'}
    ]
    
    print("📊 金融数据验证示例:")
    result = ensure_data_accuracy('financial', sample_financial_data)
    print(f"验证结果: {result['status']}")
    print(f"置信度: {result['confidence_score']:.1f}%")
    if result['status'] == 'VALIDATED':
        print(f"验证后数据: {result['data']}")
    
    print("\n" + "="*50)
    
    # 示例：验证一般数据
    sample_general_data = [
        {'source': 'wikipedia', 'value': '人工智能', 'timestamp': '2026-02-11T06:00:00Z'},
        {'source': 'encyclopedia', 'value': 'Artificial Intelligence', 'timestamp': '2026-02-11T06:30:00Z'},
        {'source': 'academic', 'value': 'AI', 'timestamp': '2026-02-11T07:00:00Z'}
    ]
    
    print("📚 一般数据验证示例:")
    result = ensure_data_accuracy('general', sample_general_data, require_validation=False)
    print(f"验证结果: {result['status']}")
    print(f"消息: {result['message']}")
    
    print("\n" + "="*50)
    
    # 获取验证统计
    summary = data_accuracy.get_validation_summary()
    print(f"📈 验证统计:")
    print(f"总验证次数: {summary['total_validations']}")
    print(f"失败率: {summary['failure_rate']:.1f}%")