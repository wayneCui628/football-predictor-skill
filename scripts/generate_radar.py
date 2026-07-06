import argparse
import numpy as np
import matplotlib.pyplot as plt

# Ensure Chinese characters render correctly on Windows
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

def generate_radar_chart(team1, team2, stats1, stats2, output_path):
    # Fixed categories for the radar chart (Bilingual)
    categories = [
        'xG\n(预期进球)', 
        'xGA\n(预期丢球)', 
        'Possession\n(控球率 %)', 
        'Pass Acc\n(传球成功率 %)', 
        'PPDA\n(压迫强度)', 
        'Duel\n(争顶成功率 %)', 
        'SCA\n(创造射门)', 
        'ProgP\n(向前推进)'
    ]
    N = len(categories)

    # What will be the angle of each axis in the plot? (divide the plot / number of variable)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    # Initialize the spider plot
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # If you want the first axis to be on top:
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Draw one axe per variable + add labels
    plt.xticks(angles[:-1], categories, color='grey', size=11)

    # Draw ylabels
    ax.set_rlabel_position(0)
    # We assume normalized stats between 0 and 100 for visual comparison
    # PPDA is inverse (lower is better pressing), so it should be inverted before passing to this script
    plt.yticks([20, 40, 60, 80], ["20", "40", "60", "80"], color="grey", size=7)
    plt.ylim(0, 100)

    # Plot Team 1
    values1 = stats1 + stats1[:1]
    ax.plot(angles, values1, linewidth=2, linestyle='solid', label=team1, color='#1f77b4')
    ax.fill(angles, values1, '#1f77b4', alpha=0.25)

    # Plot Team 2
    values2 = stats2 + stats2[:1]
    ax.plot(angles, values2, linewidth=2, linestyle='solid', label=team2, color='#ff7f0e')
    ax.fill(angles, values2, '#ff7f0e', alpha=0.25)

    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    plt.title(f'Bilingual Advanced Metrics | 高阶数据雷达图: {team1} vs {team2}', size=15, color='black', y=1.1)

    # Save to file
    plt.savefig(output_path, bbox_inches='tight')
    print(f"Radar chart saved successfully to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a radar chart comparing two football teams.")
    parser.add_argument("--team1", type=str, required=True, help="Name of Team 1")
    parser.add_argument("--team2", type=str, required=True, help="Name of Team 2")
    
    # Comma separated stats (8 values)
    parser.add_argument("--stats1", type=str, required=True, help="Comma separated normalized stats for Team 1 (8 values)")
    parser.add_argument("--stats2", type=str, required=True, help="Comma separated normalized stats for Team 2 (8 values)")
    
    parser.add_argument("--output", type=str, default="radar_chart.png", help="Output file path")
    
    args = parser.parse_args()
    
    try:
        s1 = [float(x.strip()) for x in args.stats1.split(',')]
        s2 = [float(x.strip()) for x in args.stats2.split(',')]
        
        if len(s1) != 8 or len(s2) != 8:
            raise ValueError("Exactly 8 comma-separated values are required for stats.")
            
        generate_radar_chart(args.team1, args.team2, s1, s2, args.output)
    except Exception as e:
        print(f"Error generating chart: {e}")
