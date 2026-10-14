
from datetime import datetime


def write_report(player, scores):
    # Сохраняем отчёт о работе приложения
    player.time_out = datetime.now()

    lines = []
    lines.append("+" + "-" * 41 + "+")
    lines.append(
        f"| {'login':<10} | {'time_in':<19} | {'time_out':<19} |"
    )
    lines.append(
        "|" + "-" * 12 + "|" + "-" * 21 + "|" + "-" * 21 + "|"
    )
    lines.append(
        f"| {player.name:<10} | "
        f"{player.time_in.strftime('%d.%m.%Y %H:%M:%S'):<19} | "
        f"{player.time_out.strftime('%d.%m.%Y %H:%M:%S'):<19} |"
    )
    lines.append("+" + "-" * 41 + "+")
    lines.append("")
    lines.append("Результаты игр:")

    if len(scores) == 0:
        lines.append("  (нет записей)")
    else:
        for r in scores.sorted_by_time():
            lines.append(f"  {r.describe()}")

    with open("report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
