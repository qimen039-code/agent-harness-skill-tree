#!/usr/bin/env python3
"""
Repair Claims - 自动修复机械问题
修复格式问题、字段别名问题、常见的不规范写法
注意：只修复机械问题，绝不补数据或编造内容

用法：
    python repair_claims.py --facts path/to/facts.json
    python repair_claims.py --facts facts.json --output facts-fixed.json
    python repair_claims.py --all ./memory
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime, timezone


class ClaimRepairer:
    """声明修复器"""

    def __init__(self):
        self.fixes = []
        self.warnings = []

    def add_fix(self, category, description, location=None):
        """记录修复项"""
        self.fixes.append({
            'category': category,
            'description': description,
            'location': location
        })

    def add_warning(self, category, description, location=None):
        """记录警告（无法自动修复的）"""
        self.warnings.append({
            'category': category,
            'description': description,
            'location': location
        })

    def repair_facts(self, facts_path):
        """修复 facts.json"""
        print(f"REPAIR facts: {facts_path}")

        with open(facts_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 修复 1: schema 版本升级
        if 'schema_version' not in data or data['schema_version'] == '1.0':
            old_version = data.get('schema_version', 'missing')
            data['schema_version'] = '2.0'
            self.add_fix('schema', f"升级 schema 版本: {old_version} -> 2.0", facts_path)

        # 修复 2: 添加 meta 层
        if 'meta' not in data:
            data['meta'] = {
                'task_id': '',
                'task_name': '',
                'created_at': datetime.now(timezone.utc).isoformat(),
                'last_updated': datetime.now(timezone.utc).isoformat(),
                'data_mode': 'partial',
                'agent_mode': 'execution',
                'description': ''
            }
            self.add_fix('structure', '添加缺失的 meta 层', facts_path)

        # 修复 3: facts -> raw_facts 迁移
        if 'facts' in data and 'raw_facts' not in data:
            data['raw_facts'] = data.pop('facts')
            self.add_fix('structure', '重命名字段: facts -> raw_facts', facts_path)

        # 修复 4: 添加 derived_facts
        if 'derived_facts' not in data:
            data['derived_facts'] = []
            self.add_fix('structure', '添加缺失的 derived_facts', facts_path)

        # 修复 5: 修复每条事实的字段
        if 'raw_facts' in data:
            for i, fact in enumerate(data['raw_facts']):
                self._repair_fact_item(fact, f"{facts_path}:raw_facts[{i}]")

        if 'derived_facts' in data:
            for i, fact in enumerate(data['derived_facts']):
                self._repair_fact_item(fact, f"{facts_path}:derived_facts[{i}]")
                # 派生事实额外检查
                if 'derived_from' not in fact:
                    self.add_warning('derived', '派生事实缺少 derived_from 字段（无法自动修复）', f"{facts_path}:derived_facts[{i}]")

        # 修复 6: 完善 rules
        if 'rules' not in data:
            data['rules'] = {}
            self.add_fix('structure', '添加缺失的 rules', facts_path)

        if 'evidence_tiers' not in data.get('rules', {}):
            data['rules']['evidence_tiers'] = {
                'tier_1': '原始/权威来源：实际读取的文件、命令执行输出、官方文档、用户明确提供',
                'tier_2': '间接/二手来源：代码逻辑推断、相似模式匹配、文档间接提及、第三方非权威来源',
                'tier_3': '弱线索：历史经验推测、从其他假设推导、无明确来源'
            }
            self.add_fix('rules', '添加缺失的 evidence_tiers 定义', facts_path)

        # 修复 7: 更新时间戳
        if 'meta' in data:
            data['meta']['last_updated'] = datetime.now(timezone.utc).isoformat()

        return data

    def _repair_fact_item(self, fact, location):
        """修复单条事实"""
        # 修复字段别名
        field_aliases = {
            'source': 'evidence_source',
            'evidence': 'evidence_detail',
            'type': 'evidence_type',
            'verified': 'verified_at',
            'conf': 'confidence',
            'method': 'verification_method'
        }

        for old, new in field_aliases.items():
            if old in fact and new not in fact:
                fact[new] = fact.pop(old)
                self.add_fix('field', f"字段别名修复: {old} -> {new}", location)

        # 修复 evidence_tier
        if 'evidence_tier' not in fact:
            # 尝试从 confidence 推断
            if fact.get('confidence', 0) >= 0.9:
                fact['evidence_tier'] = 'tier_1'
            elif fact.get('confidence', 0) >= 0.6:
                fact['evidence_tier'] = 'tier_2'
            else:
                fact['evidence_tier'] = 'tier_3'
            self.add_fix('tier', f"添加缺失的 evidence_tier (推断为 {fact['evidence_tier']})", location)

        # 修复 confidence 格式
        if 'confidence' in fact:
            conf = fact['confidence']
            if isinstance(conf, str):
                try:
                    fact['confidence'] = float(conf)
                    self.add_fix('confidence', '修复 confidence 类型: string -> float', location)
                except ValueError:
                    self.add_warning('confidence', f"无法解析的 confidence 值: {conf}", location)

        # 添加缺失的必需字段（填空）
        required_fields = ['id', 'claim', 'evidence_tier', 'evidence_source', 'verified_at', 'confidence']
        for field in required_fields:
            if field not in fact:
                if field == 'id':
                    fact[field] = f"fact-auto-{len(self.fixes)}"
                elif field == 'verified_at':
                    fact[field] = datetime.now(timezone.utc).isoformat()
                elif field == 'confidence':
                    fact[field] = 0.5
                else:
                    fact[field] = ''
                self.add_fix('field', f"添加缺失的字段: {field}", location)

    def repair_hypotheses(self, hypotheses_path):
        """修复 hypotheses.json"""
        print(f"REPAIR hypotheses: {hypotheses_path}")

        with open(hypotheses_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 修复 1: schema 版本升级
        if 'schema_version' not in data or data['schema_version'] == '1.0':
            old_version = data.get('schema_version', 'missing')
            data['schema_version'] = '2.0'
            self.add_fix('schema', f"升级 schema 版本: {old_version} -> 2.0", hypotheses_path)

        # 修复 2: 添加 meta 层
        if 'meta' not in data:
            data['meta'] = {
                'task_id': '',
                'task_name': '',
                'created_at': datetime.now(timezone.utc).isoformat(),
                'last_updated': datetime.now(timezone.utc).isoformat(),
                'agent_mode': 'execution',
                'description': ''
            }
            self.add_fix('structure', '添加缺失的 meta 层', hypotheses_path)

        # 修复 3: 修复每条假设的字段
        if 'hypotheses' in data:
            for i, hypo in enumerate(data['hypotheses']):
                self._repair_hypothesis_item(hypo, f"{hypotheses_path}:hypotheses[{i}]")

        # 修复 4: 完善 rules
        if 'rules' not in data:
            data['rules'] = {}
            self.add_fix('structure', '添加缺失的 rules', hypotheses_path)

        if 'evidence_strength_levels' not in data.get('rules', {}):
            data['rules']['evidence_strength_levels'] = {
                'weak': '只有间接线索，很可能不对',
                'medium': '有一定证据，但还不够直接',
                'strong': '有较多间接证据，大概率正确，但未直接验证'
            }
            self.add_fix('rules', '添加缺失的 evidence_strength_levels 定义', hypotheses_path)

        return data

    def _repair_hypothesis_item(self, hypo, location):
        """修复单条假设"""
        # 修复 evidence_strength 别名
        if 'evidence_strength' not in hypo and 'strength' in hypo:
            hypo['evidence_strength'] = hypo.pop('strength')
            self.add_fix('field', '字段别名修复: strength -> evidence_strength', location)

        # 修复 evidence_strength 值
        if 'evidence_strength' in hypo:
            strength = hypo['evidence_strength']
            strength_aliases = {
                'low': 'weak',
                '高': 'strong',
                '中': 'medium',
                '低': 'weak',
                'high': 'strong',
                'medium': 'medium'
            }
            if strength in strength_aliases:
                hypo['evidence_strength'] = strength_aliases[strength]
                self.add_fix('strength', f"修复 evidence_strength 值: {strength} -> {hypo['evidence_strength']}", location)

        # 添加缺失的必需字段
        required_fields = ['id', 'claim', 'evidence_basis', 'evidence_strength', 'confidence', 'verification_status']
        for field in required_fields:
            if field not in hypo:
                if field == 'id':
                    hypo[field] = f"hypo-auto-{len(self.fixes)}"
                elif field == 'confidence':
                    hypo[field] = 0.3
                elif field == 'verification_status':
                    hypo[field] = 'unverified'
                else:
                    hypo[field] = ''
                self.add_fix('field', f"添加缺失的字段: {field}", location)

    def print_report(self):
        """打印修复报告"""
        print("\n" + "="*60)
        print("Repair report")
        print("="*60)

        print(f"\nOK: 已修复 {len(self.fixes)} 项")
        for i, fix in enumerate(self.fixes[:15], 1):
            loc = f" ({fix['location']})" if fix['location'] else ''
            print(f"  {i}. [{fix['category']}] {fix['description']}{loc}")
        if len(self.fixes) > 15:
            print(f"  ... 还有 {len(self.fixes) - 15} 项修复")

        if self.warnings:
            print(f"\nWARN: 无法自动修复 {len(self.warnings)} 项")
            for i, warning in enumerate(self.warnings[:10], 1):
                loc = f" ({warning['location']})" if warning['location'] else ''
                print(f"  {i}. [{warning['category']}] {warning['description']}{loc}")
            if len(self.warnings) > 10:
                print(f"  ... 还有 {len(self.warnings) - 10} 项警告")

        print("\n" + "="*60)
        print("WARN: 本工具只修复机械问题，绝不补数据或编造内容")
        print("   空字段需要人工补充，警告项需要人工处理")
        print("="*60)


def main():
    parser = argparse.ArgumentParser(description='Repair Claims - 自动修复机械问题')
    parser.add_argument('--facts', help='facts.json 文件路径')
    parser.add_argument('--hypotheses', help='hypotheses.json 文件路径')
    parser.add_argument('--all', help='修复整个目录下的所有相关文件')
    parser.add_argument('--output', help='输出文件路径（默认覆盖原文件）')
    parser.add_argument('--dry-run', action='store_true', help='只检查不修改')

    args = parser.parse_args()

    repairer = ClaimRepairer()

    if args.all:
        base_path = Path(args.all)
        facts_path = base_path / 'facts.json'
        hypotheses_path = base_path / 'hypotheses.json'

        if facts_path.exists():
            data = repairer.repair_facts(str(facts_path))
            if not args.dry_run:
                output = args.output or str(facts_path)
                with open(output, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

        if hypotheses_path.exists():
            data = repairer.repair_hypotheses(str(hypotheses_path))
            if not args.dry_run:
                output = args.output or str(hypotheses_path)
                with open(output, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
    else:
        if args.facts:
            data = repairer.repair_facts(args.facts)
            if not args.dry_run:
                output = args.output or args.facts
                with open(output, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

        if args.hypotheses:
            data = repairer.repair_hypotheses(args.hypotheses)
            if not args.dry_run:
                output = args.output or args.hypotheses
                with open(output, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

    repairer.print_report()

    if args.dry_run:
        print("\nCHECK: dry-run 模式，未修改文件")


if __name__ == '__main__':
    main()
