import pandas as pd
from sklearn.model_selection import train_test_split
from simpletransformers.classification import ClassificationModel
from sklearn.metrics import f1_score, accuracy_score
from timeit import default_timer as timer



df = pd.read_csv("/Users/sachittarora/Documents/GitHub/level1_post_recommender_20/sachitt_arora/cleanedamazondata.csv")




def findcategories(df):
  categories = []
  for i in df["Category"].unique():
    categories.append(i)

  return categories

categories = findcategories(df)

def f1_multiclass(labels, preds):
    return f1_score(labels, preds, average='micro')


def buildotherdf(df):
  seconddf = pd.DataFrame()
  seconddf['post'] = df['Title'] + ' ' + df['Leading Comment']
  seconddf['category'] = df['Category']
  seconddf['post'] = seconddf['post'].apply(lambda x: str(x))
  seconddf['category'] = seconddf['category'].apply(lambda x: str(x))

  seconddf['category'] = seconddf.apply(lambda x:  categories.index(x['category']),axis=1)

  return seconddf

def main(df):
    seconddf = buildotherdf(df)

    train_df, test_df = train_test_split(seconddf, test_size=0.10)

    train_args ={"reprocess_input_data": True,
                "overwrite_output_dir": True,
                "fp16":False,
                "num_train_epochs": 4}

    model = ClassificationModel(
            "bert", "bert-base-cased",
            num_labels=12,
            args=train_args,
            use_cuda=False
        )
    timetakes(model, train_df)

    model.train_model(train_df)
    result, model_outputs, wrong_predictions = model.eval_model(test_df, f1=f1_multiclass, acc=accuracy_score)
    print(result)


def timetakes(model, train_df):
  starttime = timer()
  model.train_model(train_df)
  elapsedtime = timer() - starttime
  print(elapsedtime)


