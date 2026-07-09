from models import FinalReport


def format_report(report: FinalReport) -> str:
    blocks = []
    for i, project in enumerate(report.projects, start=1):
        signals = "\n".join(f"-{s}" for s in project.growth_signals)
        block = f"""## {i}. {project.repository_name}
- Momentum: {project.momentum_score:.2f}
- Sentiment: {project.sentiment}
- Growth status: {project.growth_status}

Verdict: {project.verdict}

Growth signals:
{signals}
"""
        blocks.append(block)
    projects_text = "\n---\n".join(blocks)

    return f"""# 📡 Breakout Radar Report

**Query:** {report.query}

## Summary 
{report.summary}

{projects_text}
"""
