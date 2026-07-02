#!/usr/bin/env python3
"""
Claim Lint - 声明校验工具
检查 facts.json、hypotheses.json 和输出文本是否符合 claim-boundary 规范

用法：
    python lint_claims.py --facts path/to/facts.json
    python lint_claims.py --hypotheses path/to/hypotheses.json
    python lint_claims.py --output path/to/output.md
    python lint_claims.py --facts facts.json --hypotheses hypotheses.json --output output.md --strict
"""

import json
import re
import argparse
import sys
from pathlib import Path
from datetime import datetime


class ClaimLinter:
    """声明校验器"""

    def __init__(self, strict=False):
        self.strict = strict
        self.errors = []
        self.warnings = []
        self.stats = {
            'facts_checked': 0,
            'hypotheses_checked': 0,
            'output_lines_checked': 0,
            'errors': 0,
            'warnings': 0
        }

    def add_error(self, category, message, location=None):
        """添加错误"""
        error = {
            'type': 'error',
            'category': category,
            'message': message,
            'location': location
        }
        self.errors.append(error)
        self.stats['errors'] += 1

    def add_warning(self, category, message, location=None):
        """添加警告"""
        warning = {
            'type': 'warning',
            'category': category,
            'message': message,
            'location': location
        }
        self.warnings.append(warning)
        self.stats['warnings'] += 1

    def lint_facts(self, facts_path):
        """校验 facts.json"""
        print(f"CHECK facts: {facts_path}")

        try:
            with open(facts_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            self.add_error('format', f"无法解析 JSON: {e}", facts_path)
            return

        # 检查 schema 版本
        if 'schema_version' not in data:
            self.add_error('schema', '缺少 schema_version 字段', facts_path)
        else:
            if data['schema_version'] != '2.0':
                self.add_warning('schema', f"schema 版本是 {data['schema_version']}，预期 2.0", facts_path)

        # 检查 meta 层
        if 'meta' not in data:
            self.add_error('structure', '缺少 meta 层', facts_path)
        else:
            meta = data['meta']
            required_meta = ['task_id', 'task_name', 'created_at', 'last_updated']
            for field in required_meta:
                if field not in meta:
                    self.add_warning('meta', f"meta 缺少字段: {field}", facts_path)

        # 检查 raw_facts
        if 'raw_facts' not in data:
            self.add_error('structure', '缺少 raw_facts', facts_path)
        else:
            self._check_fact_list(data['raw_facts'], 'raw_facts', facts_path)

        # 检查 derived_facts
        if 'derived_facts' not in data:
            self.add_warning('structure', '缺少 derived_facts（可选）', facts_path)
        else:
            self._check_fact_list(data['derived_facts'], 'derived_facts', facts_path)
            # 检查派生事实的 derived_from
            for i, fact in enumerate(data['derived_facts']):
                if 'derived_from' not in fact:
                    self.add_error('derived', f"派生事实缺少 derived_from 字段", f"{facts_path}:derived_facts[{i}]")
                if 'derivation_logic' not in fact:
                    self.add_warning('derived', f"派生事实缺少 derivation_logic 字段", f"{facts_path}:derived_facts[{i}]")

        # 检查 rules
        if 'rules' not in data:
            self.add_warning('structure', '缺少 rules（可选）', facts_path)

        print(f"  OK: 检查了 {self.stats['facts_checked']} 条事实")

    def _check_fact_list(self, facts, list_name, facts_path):
        """检查事实列表"""
        for i, fact in enumerate(facts):
            self.stats['facts_checked'] += 1
            location = f"{facts_path}:{list_name}[{i}]"

            # 必需字段
            required_fields = ['id', 'claim', 'evidence_tier', 'evidence_source', 'verified_at', 'confidence']
            for field in required_fields:
                if field not in fact:
                    self.add_error('field', f"事实缺少必需字段: {field}", location)

            # 检查 evidence_tier
            if 'evidence_tier' in fact:
                valid_tiers = ['tier_1', 'tier_2', 'tier_3']
                if fact['evidence_tier'] not in valid_tiers:
                    self.add_error('tier', f"无效的 evidence_tier: {fact['evidence_tier']}，有效值: {valid_tiers}", location)

            # 检查 confidence
            if 'confidence' in fact:
                conf = fact['confidence']
                if not isinstance(conf, (int, float)) or conf < 0 or conf > 1:
                    self.add_error('confidence', f"confidence 必须是 0-1 之间的数字，当前: {conf}", location)

            # 严格模式下检查 evidence_detail
            if self.strict and 'evidence_detail' not in fact:
                self.add_warning('evidence', '严格模式下建议提供 evidence_detail', location)

            # 严格模式下检查 verification_method
            if self.strict and 'verification_method' not in fact:
                self.add_warning('verification', '严格模式下建议提供 verification_method', location)

    def lint_hypotheses(self, hypotheses_path):
        """校验 hypotheses.json"""
        print(f"CHECK hypotheses: {hypotheses_path}")

        try:
            with open(hypotheses_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            self.add_error('format', f"无法解析 JSON: {e}", hypotheses_path)
            return

        # 检查 schema 版本
        if 'schema_version' not in data:
            self.add_error('schema', '缺少 schema_version 字段', hypotheses_path)

        # 检查 meta 层
        if 'meta' not in data:
            self.add_error('structure', '缺少 meta 层', hypotheses_path)

        # 检查 hypotheses 列表
        if 'hypotheses' not in data:
            self.add_error('structure', '缺少 hypotheses 列表', hypotheses_path)
        else:
            for i, hypo in enumerate(data['hypotheses']):
                self.stats['hypotheses_checked'] += 1
                location = f"{hypotheses_path}:hypotheses[{i}]"

                # 必需字段
                required_fields = ['id', 'claim', 'evidence_basis', 'evidence_strength', 'confidence', 'verification_status']
                for field in required_fields:
                    if field not in hypo:
                        self.add_error('field', f"假设缺少必需字段: {field}", location)

                # 检查 evidence_strength
                if 'evidence_strength' in hypo:
                    valid_strengths = ['weak', 'medium', 'strong']
                    if hypo['evidence_strength'] not in valid_strengths:
                        self.add_error('strength', f"无效的 evidence_strength: {hypo['evidence_strength']}，有效值: {valid_strengths}", location)

                # 检查 confidence 不能太高
                if 'confidence' in hypo:
                    conf = hypo['confidence']
                    if conf > 0.6:
                        self.add_warning('confidence', f"假设的 confidence 过高 ({conf})，假设最高不应超过 0.6", location)

                # 检查 verification_steps
                if self.strict and 'verification_steps' not in hypo:
                    self.add_error('verification', '严格模式下假设必须有 verification_steps', location)

                # 检查 alternative_explanations
                if self.strict and 'alternative_explanations' not in hypo:
                    self.add_warning('alternative', '严格模式下建议提供 alternative_explanations', location)

        print(f"  OK: 检查了 {self.stats['hypotheses_checked']} 条假设")

    def lint_output(self, output_path):
        """校验输出文本是否符合输出合约"""
        print(f"CHECK output: {output_path}")

        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.add_error('format', f"无法读取文件: {e}", output_path)
            return

        lines = content.split('\n')
        self.stats['output_lines_checked'] = len(lines)

        # 检查标签使用
        fact_count = len(re.findall(r'🟢', content))
        hypothesis_count = len(re.findall(r'🟡', content))
        unknown_count = len(re.findall(r'🔴', content))

        print(f"  label stats: facts={fact_count}, hypotheses={hypothesis_count}, unknowns={unknown_count}")

        # 检查是否有未标注的声明（简单启发式检查）
        suspicious_patterns = [
            (r'应该是', '可能包含未标注的推测'),
            (r'可能是', '可能包含未标注的推测'),
            (r'大概是', '可能包含未标注的推测'),
            (r'应该没问题', '可能包含未标注的推测'),
        ]

        for i, line in enumerate(lines):
            self.stats['output_lines_checked'] += 1
            # 跳过已标注的行
            if '🟢' in line or '🟡' in line or '🔴' in line:
                continue

            for pattern, message in suspicious_patterns:
                if re.search(pattern, line):
                    self.add_warning('labeling', f"第 {i+1} 行: {message}", output_path)
                    break

        # 检查是否有事实分区
        if '已验证事实' not in content and fact_count > 0:
            self.add_warning('structure', '建议使用"已验证事实"作为分区标题', output_path)

        # 检查是否有假设分区
        if '弱证据假设' not in content and hypothesis_count > 0:
            self.add_warning('structure', '建议使用"弱证据假设"作为分区标题', output_path)

        # 检查是否有未知分区
        if '未知信息' not in content and unknown_count > 0:
            self.add_warning('structure', '建议使用"未知信息"作为分区标题', output_path)

        # 严格模式下的额外检查
        if self.strict:
            # 检查每条事实是否有证据说明
            fact_lines = [line for line in lines if '🟢' in line]
            for i, line in enumerate(fact_lines):
                if '证据' not in line and '来源' not in line:
                    self.add_warning('evidence', f"事实行 {i+1} 可能缺少证据说明", output_path)

            # 检查每条假设是否有 [假设] 标签
            hypo_lines = [line for line in lines if '🟡' in line]
            for i, line in enumerate(hypo_lines):
                if '[假设]' not in line:
                    self.add_warning('labeling', f"假设行 {i+1} 建议加上 [假设] 前缀", output_path)

        print(f"  OK: 检查了 {len(lines)} 行输出")

    def get_compliance_score(self):
        """计算合规分数"""
        total_checks = self.stats['facts_checked'] + self.stats['hypotheses_checked'] + self.stats['output_lines_checked'] / 10
        if total_checks == 0:
            return 0

        error_penalty = self.stats['errors'] * 10
        warning_penalty = self.stats['warnings'] * 3

        score = max(0, 100 - error_penalty - warning_penalty)
        return round(score, 1)

    def print_report(self):
        """打印校验报告"""
        print("\n" + "="*60)
        print("Claim lint report")
        print("="*60)

        print(f"\nStats:")
        print(f"  检查事实数: {self.stats['facts_checked']}")
        print(f"  检查假设数: {self.stats['hypotheses_checked']}")
        print(f"  检查输出行: {self.stats['output_lines_checked']}")
        print(f"  错误数: {self.stats['errors']}")
        print(f"  警告数: {self.stats['warnings']}")

        score = self.get_compliance_score()
        print(f"\nCompliance score: {score}/100")

        if score >= 90:
            print("  OK: 优秀，符合 claim-boundary 规范")
        elif score >= 70:
            print("  WARN: 良好，但有改进空间")
        elif score >= 50:
            print("  WARN: 及格，需要改进")
        else:
            print("  FAIL: 不合格，需要大量改进")

        if self.errors:
            print(f"\nErrors ({len(self.errors)}):")
            for i, error in enumerate(self.errors[:10], 1):
                loc = f" ({error['location']})" if error['location'] else ''
                print(f"  {i}. [{error['category']}] {error['message']}{loc}")
            if len(self.errors) > 10:
                print(f"  ... 还有 {len(self.errors) - 10} 个错误")

        if self.warnings:
            print(f"\nWarnings ({len(self.warnings)}):")
            for i, warning in enumerate(self.warnings[:10], 1):
                loc = f" ({warning['location']})" if warning['location'] else ''
                print(f"  {i}. [{warning['category']}] {warning['message']}{loc}")
            if len(self.warnings) > 10:
                print(f"  ... 还有 {len(self.warnings) - 10} 个警告")

        print("\n" + "="*60)

        return score >= 70  # 70分以上算通过


def main():
    parser = argparse.ArgumentParser(description='Claim Lint - 声明校验工具')
    parser.add_argument('--facts', help='facts.json 文件路径')
    parser.add_argument('--hypotheses', help='hypotheses.json 文件路径')
    parser.add_argument('--output', help='输出文本文件路径')
    parser.add_argument('--strict', action='store_true', help='严格模式')
    parser.add_argument('--all', help='检查整个目录下的所有相关文件')

    args = parser.parse_args()

    linter = ClaimLinter(strict=args.strict)

    if args.all:
        # 检查整个目录
        base_path = Path(args.all)
        facts_path = base_path / 'memory' / 'facts.json'
        hypotheses_path = base_path / 'memory' / 'hypotheses.json'

        if facts_path.exists():
            linter.lint_facts(str(facts_path))
        if hypotheses_path.exists():
            linter.lint_hypotheses(str(hypotheses_path))
    else:
        if args.facts:
            linter.lint_facts(args.facts)
        if args.hypotheses:
            linter.lint_hypotheses(args.hypotheses)
        if args.output:
            linter.lint_output(args.output)

    passed = linter.print_report()

    if not passed and args.strict:
        print("\nFAIL: 严格模式下校验未通过，请修复错误后重试")
        sys.exit(1)

    return passed


if __name__ == '__main__':
    main()
