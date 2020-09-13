import pandas as pd



if __name__ == '__main__':
    data = pd.read_csv('D:\ReadingLog\Collective intelligence programming\ch2\ml-latest-small\movies.csv')
    for i in range(0, len(data)):
        print(data.iloc[i]['movieId'])



