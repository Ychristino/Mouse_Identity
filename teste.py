import generate_heatmap_graph
import pandas as pd

print("teste")

if __name__ == "__main__":
    dataframe = pd.read_csv(f'./data/user/mouse_event/League_of_Legends_mouse_event', sep=';')
    generate_heatmap_graph.generate_heatmap_graph(dataframe).generate()