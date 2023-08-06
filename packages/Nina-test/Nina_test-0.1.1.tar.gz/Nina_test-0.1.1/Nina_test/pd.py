from pandas import DataFrame

def create_csv(file,data,Frame=None):
    df=DataFrame(data)
    if Frame:
        print(df)
    else:
         pass
    df.to_csv(file,index=False)
