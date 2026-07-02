#!/usr/bin/env python3
"""
Init Memory - 初始化记忆结构
创建标准的 facts.json 和 hypotheses.json 骨架

用法：
    python init_memory.py --task "任务名称" --output ./memory
    python init_memory.py --task "项目分析" --task-id "proj-001" --output ./work
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime, timezone


def init_memory(task_name, task_id="", output_dir="./memory", description=""):
    """初始化记忆结构"""

    # 确保输出目录存在
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc).isoformat()

    # 创建 facts.json 骨架
    facts = {
        "schema_version": "2.0",
        "meta": {
            "task_id": task_id,
            "task_name": task_name,
            "created_at": now,
            "last_updated": now,
            "data_mode": "empty",
            "agent_mode": "execution",
            "description": description
        },
        "raw_facts": [],
        "derived_facts": [],
        "rules": {
            "only_validated": True,
            "require_evidence_source": True,
            "require_verification_method": True,
            "auto_decay_days": 30,
            "evidence_tiers": {
                "tier_1": "原始/权威来源：实际读取的文件、命令执行输出、官方文档、用户明确提供",
                "tier_2": "间接/二手来源：代码逻辑推断、相似模式匹配、文档间接提及、第三方非权威来源",
                "tier_3": "弱线索：历史经验推测、从其他假设推导、无明确来源"
            }
        }
    }

    # 创建 hypotheses.json 骨架
    hypotheses = {
        "schema_version": "2.0",
        "meta": {
            "task_id": task_id,
            "task_name": task_name,
            "created_at": now,
            "last_updated": now,
            "agent_mode": "execution",
            "description": description
        },
        "hypotheses": [],
        "rules": {
            "cannot_be_used_as_premise": True,
            "require_evidence_basis": True,
            "require_verification_steps": True,
            "require_alternative_explanations": True,
            "auto_decay_days": 7,
            "max_confidence": 0.6,
            "evidence_strength_levels": {
                "weak": "只有间接线索，很可能不对",
                "medium": "有一定证据，但还不够直接",
                "strong": "有较多间接证据，大概率正确，但未直接验证"
            }
        }
    }

    # 写入文件
    facts_path = output_path / "facts.json"
    hypotheses_path = output_path / "hypotheses.json"

    with open(facts_path, 'w', encoding='utf-8') as f:
        json.dump(facts, f, indent=2, ensure_ascii=False)

    with open(hypotheses_path, 'w', encoding='utf-8') as f:
        json.dump(hypotheses, f, indent=2, ensure_ascii=False)

    print("OK: 记忆结构初始化完成")
    print(f"   任务: {task_name}")
    print(f"   任务ID: {task_id or '未设置'}")
    print(f"   输出目录: {output_path.absolute()}")
    print(f"   - facts.json: {facts_path}")
    print(f"   - hypotheses.json: {hypotheses_path}")

    return facts_path, hypotheses_path


def main():
    parser = argparse.ArgumentParser(description='Init Memory - 初始化记忆结构')
    parser.add_argument('--task', required=True, help='任务名称')
    parser.add_argument('--task-id', default='', help='任务ID（可选）')
    parser.add_argument('--output', default='./memory', help='输出目录')
    parser.add_argument('--description', default='', help='任务描述')

    args = parser.parse_args()

    init_memory(
        task_name=args.task,
        task_id=args.task_id,
        output_dir=args.output,
        description=args.description
    )


if __name__ == '__main__':
    main()
