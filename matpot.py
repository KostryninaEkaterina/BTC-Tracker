import matplotlib.pyplot as plt


def plot_data(data:dict):
    tmp_zip = list(zip(*data.items()))
    dates, prices = tmp_zip[0], tmp_zip[1]
    offset = 1
    if len(dates) >= 12:
        offset = int(len(dates) / 12)
    plt.plot(dates, prices)
    plt.title('Historical BTC Price')
    plt.xticks(dates[::offset], rotation='vertical')
    plt.grid()
    plt.show()
