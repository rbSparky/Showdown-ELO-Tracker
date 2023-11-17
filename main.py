import matplotlib.pyplot as plt

with open('elo.txt', 'r') as file:
    elo_data = [int(line.strip()) for line in file.readlines()]

divisions = {
    'pupil': (range(0, 1200), 'green'),
    'specialist': (range(1200, 1400), 'cyan'),
    'expert': (range(1400, 1600), 'blue'),
    'master': (range(1600, 1800), 'orange'),
    'grandmaster': (range(1800, 2101), 'red')
}

max_elo_reached = max(elo_data)
for division, (elo_range, color) in divisions.items():
    plt.text(0.5, elo_range.stop - 50, division.capitalize(), color=color, fontsize=10)
    #if elo_range.stop > max_elo_reached:
    plt.axhspan(elo_range.start, elo_range.stop, color=color, alpha=0.1)
        

categorized_elo = []
current_battle = 1

for elo in elo_data:
    category = None
    for division, (elo_range, _) in divisions.items():
        if elo in elo_range:
            category = division
            break
    categorized_elo.append((current_battle, elo, category))
    current_battle += 1

data_by_division = {division: [] for division in divisions}

for battle, elo, category in categorized_elo:
    if category:
        data_by_division[category].append((battle, elo))

plot_data = []

for division, (elo_range, color) in divisions.items():
    if data_by_division[division]:
        plot_data.extend(data_by_division[division])

plot_data.sort(key=lambda x: x[0])

battles, elos = zip(*plot_data)

plt.plot(battles, elos, color='black', linestyle='--', alpha=0.3)

for division, (elo_range, color) in divisions.items():
    if data_by_division[division]:
        battles_div, elos_div = zip(*data_by_division[division])
        prev_battle = 0
        battle_plotter = []
        elo_plotter = []

        for it in range(1, len(battles_div)):
            if battles_div[it] > battles_div[it - 1] + 1:
                battle_plotter.append(battles_div[prev_battle:it])
                elo_plotter.append(elos_div[prev_battle:it])
                prev_battle = it

        battle_plotter.append(battles_div[prev_battle:len(battles_div)])
        elo_plotter.append(elos_div[prev_battle:len(elos_div)])

        for it in range(0, len(battle_plotter)):
            plt.plot(battle_plotter[it], elo_plotter[it], color=color, marker='o')

for division, (elo_range, color) in divisions.items():
    plt.axhspan(elo_range.start, elo_range.stop, color=color, alpha=0.1)

plt.xlabel('Battles')
plt.ylabel('Elo')
plt.title('Elo Progression in Pokemon Showdown')
plt.grid(True)
plt.ylim(900, 2100)

plt.tight_layout()

plt.show()

