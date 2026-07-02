#!/usr/bin/env python3
"""
Derive Claims - 派生声明计算
从原始事实统一计算派生声明，避免手动计算错误

用法：
    python derive_claims.py --facts path/to/facts.json
    python derive_claims.py --facts facts.json --output facts.json

注意：这是一个框架性实现，具体的派生逻辑需要根据实际领域定制。
      本脚本提供基础的派生计算框架和示例。
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime, timezone


class ClaimDeriver:
    """声明派生计算器"""

    def __init__(self, facts_path):
        self.facts_path = Path(facts_path)
        self.facts = None
        self.derived_count = 0

    def load(self):
        """加载 facts 文件"""
        with open(self.facts_path, 'r', encoding='utf-8') as f:
            self.facts = json.load(f)
        return self

    def derive(self):
        """执行派生计算"""
        if self.facts is None:
            raise ValueError("请先加载 facts 文件")

        # 确保 derived_facts 存在
        if 'derived_facts' not in self.facts:
            self.facts['derived_facts'] = []

        # 清空旧的派生事实（重新计算）
        old_count = len(self.facts['derived_facts'])
        self.facts['derived_facts'] = []

        # 执行各类派生计算
        self._derive_basic_stats()
        self._derive_evidence_summary()
        self._derive_custom_rules()

        # 更新时间戳
        now = datetime.now(timezone.utc).isoformat()
        self.facts['meta']['last_updated'] = now

        # 更新数据模式
        if self.facts['raw_facts']:
            self.facts['meta']['data_mode'] = 'partial'
        if self.facts['derived_facts']:
            self.facts['meta']['data_mode'] = 'complete'

        self.derived_count = len(self.facts['derived_facts'])
        print(f"OK: 派生计算完成，从 {len(self.facts['raw_facts'])} 条原始事实生成 {self.derived_count} 条派生事实")
        print(f"   (旧的 {old_count} 条派生事实已被替换)")

        return self

    def _derive_basic_stats(self):
        """派生基础统计信息"""
        raw_facts = self.facts.get('raw_facts', [])
        if not raw_facts:
            return

        # 统计各 tier 的事实数量
        tier_counts = {'tier_1': 0, 'tier_2': 0, 'tier_3': 0}
        for fact in raw_facts:
            tier = fact.get('evidence_tier', 'tier_3')
            if tier in tier_counts:
                tier_counts[tier] += 1

        # 平均置信度
        confidences = [f.get('confidence', 0) for f in raw_facts]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0

        # 添加派生事实
        self.facts['derived_facts'].append({
            'id': 'derived-stats-tiers',
            'claim': f"事实分布: tier_1={tier_counts['tier_1']}, tier_2={tier_counts['tier_2']}, tier_3={tier_counts['tier_3']}",
            'derived_from': [f['id'] for f in raw_facts],
            'derivation_logic': '统计各证据等级的事实数量',
            'evidence_tier': 'tier_1',
            'evidence_source': '派生计算',
            'verified_at': datetime.now(timezone.utc).isoformat(),
            'verification_method': 'derived_from_raw',
            'confidence': 1.0,
            'tags': ['stats', 'derived']
        })

        self.facts['derived_facts'].append({
            'id': 'derived-stats-confidence',
            'claim': f"事实平均置信度: {round(avg_confidence, 3)}",
            'derived_from': [f['id'] for f in raw_facts],
            'derivation_logic': '计算所有原始事实的置信度平均值',
            'evidence_tier': 'tier_1',
            'evidence_source': '派生计算',
            'verified_at': datetime.now(timezone.utc).isoformat(),
            'verification_method': 'derived_from_raw',
            'confidence': 1.0,
            'tags': ['stats', 'confidence', 'derived']
        })

    def _derive_evidence_summary(self):
        """派生证据摘要"""
        raw_facts = self.facts.get('raw_facts', [])
        if not raw_facts:
            return

        # 统计证据类型
        evidence_types = {}
        for fact in raw_facts:
            etype = fact.get('evidence_type', 'unknown')
            evidence_types[etype] = evidence_types.get(etype, 0) + 1

        # 统计来源
        sources = set()
        for fact in raw_facts:
            src = fact.get('evidence_source', 'unknown')
            sources.add(src)

        self.facts['derived_facts'].append({
            'id': 'derived-evidence-types',
            'claim': f"证据类型分布: {', '.join([f'{k}={v}' for k, v in evidence_types.items()])}",
            'derived_from': [f['id'] for f in raw_facts],
            'derivation_logic': '统计不同证据类型的数量',
            'evidence_tier': 'tier_1',
            'evidence_source': '派生计算',
            'verified_at': datetime.now(timezone.utc).isoformat(),
            'verification_method': 'derived_from_raw',
            'confidence': 1.0,
            'tags': ['evidence', 'stats', 'derived']
        })

        self.facts['derived_facts'].append({
            'id': 'derived-sources-count',
            'claim': f"涉及 {len(sources)} 个不同的证据来源",
            'derived_from': [f['id'] for f in raw_facts],
            'derivation_logic': '统计不重复的证据来源数量',
            'evidence_tier': 'tier_1',
            'evidence_source': '派生计算',
            'verified_at': datetime.now(timezone.utc).isoformat(),
            'verification_method': 'derived_from_raw',
            'confidence': 1.0,
            'tags': ['evidence', 'sources', 'derived']
        })

    def _derive_custom_rules(self):
        """
        自定义派生规则（占位）
        实际使用时，可以根据领域需求在这里添加具体的派生逻辑
        例如：
        - 代码分析：从文件内容派生项目类型、依赖关系等
        - 数据分析：从原始数据派生统计指标、趋势等
        - 研究分析：从多个事实派生结论等
        """
        # 这是一个占位方法，实际使用时请根据具体领域定制
        # 示例：如果有特定的事实组合，可以在这里添加派生逻辑
        pass

    def save(self, output_path=None):
        """保存结果"""
        if output_path is None:
            output_path = self.facts_path
        else:
            output_path = Path(output_path)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.facts, f, indent=2, ensure_ascii=False)

        print(f"OK: 已保存到 {output_path}")
        return output_path


def main():
    parser = argparse.ArgumentParser(description='Derive Claims - 派生声明计算')
    parser.add_argument('--facts', required=True, help='facts.json 文件路径')
    parser.add_argument('--output', help='输出文件路径（默认覆盖原文件）')

    args = parser.parse_args()

    deriver = ClaimDeriver(args.facts)
    deriver.load()
    deriver.derive()

    output = args.output or args.facts
    deriver.save(output)


if __name__ == '__main__':
    main()
